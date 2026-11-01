#!/usr/bin/env python3
"""Unit economics and an opportunity score for one product or deal, so no margin is guessed.

usage:
  biz.py score --name "Neck fan" --price 149 --unit-cost 28 --shipping 12 --duty-pct 12 --vat-pct 18 \
               --fees-pct 4 --cac 35 --returns-pct 5 --demand 4 --competition 3 --ease 4 --risk 2
               [--vat-registered] [--fixed-monthly 300] [--json]

All money is in one currency (ILS by default). The ratings are 1-5:
  demand       1 = little proof of buyers   ... 5 = strong, proven demand
  competition  1 = few sellers              ... 5 = crowded
  ease         1 = hard (licences, bulky)   ... 5 = easy to ship and sell
  risk         1 = low                      ... 5 = high (rules, returns, trademarks, fads)
Import VAT is a cost unless --vat-registered (then it is reclaimed and the sale price includes VAT).
Duty is charged on product + shipping; import VAT on product + shipping + duty. Check the current
customs and VAT rules for the order value: do not rely on these defaults.
Pure arithmetic: no network, no files.
"""
import argparse
import json
import sys


def score(a):
    cif = a.unit_cost + a.shipping
    duty = cif * a.duty_pct / 100
    import_vat = (cif + duty) * a.vat_pct / 100
    landed = cif + duty + (0 if a.vat_registered else import_vat)
    revenue = a.price / (1 + a.vat_pct / 100) if a.vat_registered else a.price
    fees = a.price * a.fees_pct / 100
    returns = a.price * a.returns_pct / 100
    contribution = revenue - landed - fees - returns          # before ads
    profit = contribution - a.cac
    margin = profit / revenue * 100 if revenue else 0
    be_roas = a.price / contribution if contribution > 0 else float("inf")
    max_cac = contribution                                     # the most an ad can cost per sale
    vols = {n: round(profit * n - a.fixed_monthly, 2) for n in (50, 200, 1000)}

    pts_margin = max(0.0, min(40.0, margin / 50 * 40))
    pts = (pts_margin + (a.demand - 1) / 4 * 20 + (5 - a.competition) / 4 * 15
           + (a.ease - 1) / 4 * 10 + (5 - a.risk) / 4 * 15)
    flags = []
    if margin < 30:
        flags.append("margin under 30% after ads: weak")
    if be_roas > 3:
        flags.append("break-even ROAS above 3: ads must work very well")
    if profit <= 0:
        flags.append("loses money per sale at these costs")
    if a.price < 3 * landed:
        flags.append("price is under 3x landed cost: little room for ads and returns")
    if a.demand <= 2:
        flags.append("weak demand proof: test before stocking")
    if a.risk >= 4:
        flags.append("high risk: check rules, trademarks and returns first")
    return {
        "name": a.name, "price": a.price, "landed_cost": round(landed, 2),
        "duty": round(duty, 2), "import_vat": round(import_vat, 2), "vat_reclaimed": a.vat_registered,
        "net_revenue": round(revenue, 2), "fees": round(fees, 2), "returns_allowance": round(returns, 2),
        "contribution_before_ads": round(contribution, 2), "ad_cost_per_sale": a.cac,
        "profit_per_sale": round(profit, 2), "margin_pct": round(margin, 1),
        "break_even_roas": round(be_roas, 2) if be_roas != float("inf") else None,
        "max_ad_cost_per_sale": round(max_cac, 2), "fixed_monthly": a.fixed_monthly,
        "profit_at_sales": vols, "score": round(pts), "flags": flags,
    }


def show(r, cur):
    def m(x):
        return f"{x:,.2f} {cur}"
    print(f"== {r['name']}  |  score {r['score']}/100")
    print(f"price {m(r['price'])}   landed cost {m(r['landed_cost'])}"
          f"  (duty {m(r['duty'])}, import VAT {m(r['import_vat'])}{' reclaimed' if r['vat_reclaimed'] else ''})")
    print(f"net revenue {m(r['net_revenue'])}   fees {m(r['fees'])}   returns {m(r['returns_allowance'])}")
    print(f"before ads {m(r['contribution_before_ads'])}   ads {m(r['ad_cost_per_sale'])}"
          f"   PROFIT/SALE {m(r['profit_per_sale'])}   margin {r['margin_pct']}%")
    roas = r["break_even_roas"]
    print(f"break-even ROAS {roas if roas is not None else 'never'}   max ad cost per sale {m(r['max_ad_cost_per_sale'])}")
    print("profit (minus fixed " + m(r["fixed_monthly"]) + "): "
          + "   ".join(f"{n} sales {m(v)}" for n, v in r["profit_at_sales"].items()))
    for f in r["flags"]:
        print("  ! " + f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score")
    s.add_argument("--name", default="item")
    s.add_argument("--price", type=float, required=True, help="retail price the customer pays")
    s.add_argument("--unit-cost", type=float, required=True, help="supplier price per unit")
    s.add_argument("--shipping", type=float, default=0, help="shipping per unit to you or to the customer")
    s.add_argument("--duty-pct", type=float, default=0)
    s.add_argument("--vat-pct", type=float, default=18)
    s.add_argument("--vat-registered", action="store_true")
    s.add_argument("--fees-pct", type=float, default=4, help="platform + payment fees, percent of price")
    s.add_argument("--cac", type=float, default=0, help="ad / acquisition cost per sale")
    s.add_argument("--returns-pct", type=float, default=5)
    s.add_argument("--fixed-monthly", type=float, default=0)
    for k in ("demand", "competition", "ease", "risk"):
        s.add_argument(f"--{k}", type=int, default=3, choices=range(1, 6))
    s.add_argument("--currency", default="ILS")
    s.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.price <= 0 or a.unit_cost < 0:
        sys.exit("price must be positive and unit cost not negative")
    r = score(a)
    print(json.dumps(r, ensure_ascii=False, indent=1)) if a.json else show(r, a.currency)


if __name__ == "__main__":
    main()
