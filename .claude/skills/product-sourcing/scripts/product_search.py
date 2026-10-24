#!/usr/bin/env python3
"""Search public product listings on supplier and marketplace sites and save the results as a table.

usage: product_search.py "yoga mat" [--site alibaba|aliexpress|amazon|ebay|all] [--out DIR] [--pages 1]

Reads the same public search pages a visitor sees. No account, no login, no purchase,
nothing sent to any seller. Writes <site>.csv and <site>.json (title, price, minimum order,
sold count, supplier or rating, link) and <site>.txt (the page's readable text) so a page the
parser does not understand can still be read. Prints REFUSED when the network policy blocks a site.
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import urllib.parse

try:
    from curl_cffi import requests as http  # looks like a real browser; plain requests get blocked
    IMPERSONATE = {"impersonate": "chrome"}
except ImportError:  # pragma: no cover
    import urllib.request
    http = None
    IMPERSONATE = {}

SITES = {
    "alibaba": "https://www.alibaba.com/trade/search?SearchText={q}&page={p}",
    "aliexpress": "https://www.aliexpress.com/w/wholesale-{qd}.html?page={p}",
    "amazon": "https://www.amazon.com/s?k={q}&page={p}",
    "ebay": "https://www.ebay.com/sch/i.html?_nkw={q}&_pgn={p}",
}


def fetch(url):
    if http is None:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode("utf-8", "replace")
    r = http.get(url, timeout=60, **IMPERSONATE)
    return r.status_code, r.text


def text_of(fragment):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", fragment)
    s = html.unescape(re.sub(r"(?s)<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s).strip()


def page_text(page):
    body = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", page)
    body = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", body))
    return "\n".join(l.strip() for l in body.splitlines() if l.strip())


def first(pattern, s, flags=re.S):
    m = re.search(pattern, s, flags)
    return text_of(m.group(1)) if m else ""


def absolute(u, base):
    if not u:
        return ""
    if u.startswith("//"):
        return "https:" + u
    return urllib.parse.urljoin(base, html.unescape(u))


def parse_alibaba_json(page, base):
    """The full result list is embedded as JSON objects that each carry a productUrl."""
    dec, rows, seen = json.JSONDecoder(), [], set()
    for m in re.finditer(r'"productUrl":', page):
        start = page.rfind('{"badges":', 0, m.start())
        if start < 0 or m.start() - start > 20000:
            continue
        try:
            obj, _ = dec.raw_decode(page, start)
        except ValueError:
            continue
        pid = str(obj.get("productId") or obj.get("id") or "")
        if not obj.get("title") or pid in seen:
            continue
        seen.add(pid)
        rows.append({
            "title": html.unescape(obj.get("title", "")),
            "price": obj.get("price", ""),
            "min_order": (obj.get("moqV2") or obj.get("moq") or "").replace("Min. order:", "").strip(),
            "supplier": obj.get("companyName", ""),
            "country": obj.get("countryCode", ""),
            "supplier_years": obj.get("goldSupplierYears", ""),
            "rating": obj.get("reviewScore", ""),
            "reviews": obj.get("reviewCount", ""),
            "url": absolute(obj.get("productUrl", ""), base),
        })
    return rows


def parse_alibaba(page, base):
    rows = parse_alibaba_json(page, base)
    if rows:
        return rows
    rows = []
    for card in page.split('<div class="fy26-product-card-content">')[1:]:
        card = card[:12000]
        title = first(r'class="searchx-product-e-title"[^>]*>(.*?)</h2>', card)
        if not title:
            continue
        rows.append({
            "title": title,
            "price": first(r'class="searchx-product-price-price-main"[^>]*>(.*?)</div>', card),
            "min_order": first(r'class="searchx-moq"[^>]*>(.*?)</div>', card).replace("Min. order:", "").strip(),
            "sold": first(r'class="searchx-sold-order"[^>]*>(.*?)</div>', card),
            "supplier": first(r'class="searchx-product-e-company"[^>]*>(.*?)</a>', card),
            "notes": "; ".join(text_of(x) for x in re.findall(r'class="searchx-selling-point-text"[^>]*>(.*?)</span>', card))[:200],
            "url": absolute((re.search(r'class="searchx-product-e-title".*?href="([^"]+)"', card, re.S) or [None, ""])[1].split("?")[0], base),
        })
    return rows


def parse_amazon(page, base):
    rows = []
    for card in re.split(r'data-component-type="s-search-result"', page)[1:]:
        card = card[:15000]
        asin = (re.search(r'data-asin="([A-Z0-9]{10})"', card) or [None, ""])[1]
        title = first(r'<h2[^>]*>(.*?)</h2>', card)
        if not title:
            continue
        rows.append({
            "title": title,
            "price": first(r'class="a-offscreen">(.*?)</span>', card),
            "rating": first(r'class="a-icon-alt">(.*?)</span>', card),
            "reviews": first(r'aria-label="([\d,.]+ ratings?)"', card) or first(r's-underline-text">([\d,.]+)</span>', card),
            "url": f"https://www.amazon.com/dp/{asin}" if asin else "",
        })
    return rows


def parse_ebay(page, base):
    rows = []
    for card in re.split(r'<li[^>]+class="[^"]*\bs-(?:item|card)\b', page)[1:]:
        card = card[:10000]
        title = first(r'class="[^"]*s-(?:item|card)__title[^"]*"[^>]*>(.*?)</(?:div|span|h3)>', card)
        if not title or title.lower().startswith("shop on ebay"):
            continue
        rows.append({
            "title": title.replace("New Listing", "").strip(),
            "price": first(r'class="[^"]*s-(?:item|card)__price[^"]*"[^>]*>(.*?)</span>', card),
            "shipping": first(r'class="[^"]*(?:s-item__shipping|s-item__logisticsCost)[^"]*"[^>]*>(.*?)</span>', card),
            "sold": first(r'>([\d,.]+\+? sold)<', card),
            "url": (re.search(r'href="(https://www\.ebay\.com/itm/[^"?]+)', card) or [None, ""])[1],
        })
    return rows


def parse_aliexpress(page, base):
    rows = []
    for m in re.finditer(r'"title":\{"displayTitle":"(.*?)"', page):
        chunk = page[max(0, m.start() - 4000): m.start() + 4000]
        pid = (re.search(r'"productId":"?(\d{8,})', chunk) or [None, ""])[1]
        price = (re.search(r'"formattedPrice":"(.*?)"', chunk) or [None, ""])[1]
        sold = (re.search(r'"tradeDesc":"(.*?)"', chunk) or [None, ""])[1]
        rows.append({"title": json.loads('"%s"' % m.group(1)), "price": price, "sold": sold,
                     "url": f"https://www.aliexpress.com/item/{pid}.html" if pid else ""})
    return rows


PARSERS = {"alibaba": parse_alibaba, "amazon": parse_amazon, "ebay": parse_ebay, "aliexpress": parse_aliexpress}


def save(out, name, rows):
    with open(os.path.join(out, name + ".json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
    if rows:
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(os.path.join(out, name + ".csv"), "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--site", default="all", choices=list(SITES) + ["all"])
    ap.add_argument("--out", default=os.path.join(os.getcwd(), "product-search"))
    ap.add_argument("--pages", type=int, default=1)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    q = urllib.parse.quote_plus(a.query)
    qd = urllib.parse.quote(a.query.strip().replace(" ", "-"))
    for site in (SITES if a.site == "all" else [a.site]):
        rows, texts = [], []
        for p in range(1, a.pages + 1):
            url = SITES[site].format(q=q, qd=qd, p=p)
            try:
                status, page = fetch(url)
            except Exception as e:  # network policy refusals arrive as connection errors
                msg = str(e)
                why = "REFUSED (the cloud network does not allow this site)" if ("403" in msg or "CONNECT" in msg or "tunnel" in msg.lower()) else "ERROR " + msg[:160]
                print(f"{site}: {why}")
                break
            if status != 200:
                print(f"{site}: HTTP {status} (the site may be asking for a captcha; try again later or use the browser tool)")
                break
            texts.append(page_text(page))
            found = PARSERS[site](page, url)
            rows += found
            if not found:
                break
        if texts:
            with open(os.path.join(a.out, site + ".txt"), "w", encoding="utf-8") as fh:
                fh.write("\n\n".join(texts)[:200000])
        save(a.out, site, rows)
        if texts:
            print(f"{site}: {len(rows)} products" + (" (parser found none: read " + site + ".txt)" if not rows else "")
                  + f" -> {os.path.join(a.out, site + '.csv')}")


if __name__ == "__main__":
    main()
