---
title: Prices and listings from a blocked store via WebSearch (Amazon example)
tags: amazon, store, price, listing, blocked, 403, websearch, allowed_domains, asin
saved: 2026-10-31
---

# Prices and listings from a blocked store via WebSearch (Amazon example)

## Problem
amazon.com (or another store) is blocked: 'curl: (56) CONNECT tunnel failed, response 403', WebFetch 'getaddrinfo ENOTFOUND www.amazon.com'; Keepa, camelcamelcamel, Walmart, Best Buy, Target are blocked too; product-sourcing prints 'amazon: REFUSED'.

## Solution
1) WebSearch with allowed_domains ["amazon.com"] and the product or category: the summaries carry listing titles, prices, ASINs, dp links and 'bought in past month' hints. Search one product at a time for its price. 2) WebSearch '"<PRODUCT>" <ASIN> price' (no domain filter) for price history (camelcamelcamel low/high/average) and deal posts; recent roundups for 'best selling' rankings. 3) Label prices as a search snapshot with the date, and a ranking as estimated, not Amazon's official Best Sellers. 4) For live data ask the owner to add amazon.com, *.amazon.com, *.media-amazon.com, *.ssl-images-amazon.com under Network access > Allowed domains.

## Tried first (did not work)
curl / curl_cffi / product_search.py / Playwright to amazon.com (all blocked by the allowlist); WebFetch on amazon.com, asinsight.com, camelcamelcamel.com (ENOTFOUND). Third-party readers and relays are closed routes.

## How to check it worked
Each product in the reply has an amazon.com/dp/<ASIN> link and a dated price note.

## When this does not apply
Exact live price, stock or a specific seller's offer: those need the page itself, after the owner allows the domain.
