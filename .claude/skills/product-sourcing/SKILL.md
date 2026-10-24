---
name: product-sourcing
description: Research products and suppliers for an online business - search Alibaba, AliExpress, Amazon and eBay listings, compare supplier cost with retail prices, estimate landed cost and margin, and vet suppliers - from public listing pages, with no account, no login and no purchases. Use when the user wants product ideas, suppliers, wholesale prices, "find me a supplier for X", "what does X sell for", "is this product worth selling", dropshipping or private-label research, or in Hebrew "תמצא לי ספק", "כמה זה עולה באליבאבא", "מוצר למכירה", "מחקר מוצר", "דרופשיפינג", "עלות מול מחיר מכירה".
license: MIT
---

# Product sourcing

Written for this repository. It reads the same public search pages any visitor sees and turns them
into tables, then does the business math.

## Safety and limits (always)

- Read only: never log in, never add to cart, never contact a supplier, never pay, never accept terms
  on the user's behalf. Draft supplier messages for the user to send themselves.
- Keep the request rate low (a few searches, one or two pages each). These sites rate-limit and show
  captchas; do not try to get around a captcha, say so and use the browser tool or a later retry.
- Prices, minimum orders and shipping change daily and differ by country. Always date the numbers,
  link the source listing, and call them estimates.

## Search

From this skill's folder, output to a scratchpad folder:

`python3 scripts/product_search.py "<product in English>" --site all --pages 1 --out <dir>`

Use `--site alibaba|aliexpress|amazon|ebay` for one site. Each site writes `<site>.csv` / `.json`
(title, price, minimum order, sold, supplier, country, years, rating, reviews, link) and `<site>.txt`
(the page's readable text). Search in English; translate the user's Hebrew idea first.

- `REFUSED` means the cloud environment's network does not allow that site. Tell the user to add these
  under Network access > Allowed domains (or choose Full access), then open a new session:
  `alibaba.com`, `*.alibaba.com`, `aliexpress.com`, `*.aliexpress.com`, `amazon.com`, `*.amazon.com`,
  `ebay.com`, `*.ebay.com`, plus `*.alicdn.com`, `*.media-amazon.com`, `*.ebayimg.com` for images.
- A site that returns 0 products but a `.txt` file: read the text, or open the search page with the
  Playwright browser tool and read it there. Site layouts change; the Alibaba parser was tested on
  2026-10-24, the other three are written to their known layouts and may need adjusting.

## Analysis

1. **Demand and retail price**: Amazon and eBay prices, ratings, review counts and sold counts show
   what sells and for how much. Many reviews with a mediocre rating can mean an opening for a better
   version.
2. **Supplier cost**: Alibaba (bulk, minimum order, room to customize and brand) and AliExpress (single
   units, good for samples and dropshipping).
3. **Landed cost per unit**: supplier price + shipping to the customer or to Israel + customs and VAT
   where they apply (check the current Israeli import rules for the order value; do not quote a
   threshold from memory) + payment fees + marketplace or platform fees + returns allowance.
4. **Margin**: retail price minus landed cost, as money and as a percent, at three volumes. Flag any
   product under roughly 30% margin after ads as risky, and show the math.
5. **Supplier vetting**: years on the platform, rating and review count, Trade Assurance or verified
   badges, response rate, reorder rate, factory or trading company, sample policy. Recommend ordering
   samples from two or three suppliers before any bulk order.
6. **A short table** of the best 5 options with links, then a plain recommendation, and the risks
   (shipping time, intellectual-property or brand issues, regulated categories, seasonality).

Related skills: `pricing`, `offers`, `launch`, `ads`, `copywriting`, `competitor-profiling`. The
claude.ai connector AutoDS (dropshipping research, needs its own paid account) can add supplier data if
the user connects it.
