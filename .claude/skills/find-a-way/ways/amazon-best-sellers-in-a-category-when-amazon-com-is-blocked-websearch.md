---
title: Amazon best sellers in a category when amazon.com is blocked (WebSearch badges)
tags: amazon, best-sellers, ranking, price, websearch, blocked, 403, bought-in-past-month, asinsight
saved: 2026-10-31
---

# Amazon best sellers in a category when amazon.com is blocked (WebSearch badges)

## Problem
Need the top-selling items of an Amazon category with prices, but amazon.com is blocked: 'curl: (56) CONNECT tunnel failed, response 403', WebFetch 'getaddrinfo ENOTFOUND www.amazon.com', product_search.py prints 'amazon: REFUSED'. Many listings in search summaries show 'No featured offers available' or 'Click to see price'.

## Solution
1) WebSearch allowed_domains ["amazon.com"] with '<CATEGORY> "bought in past month"' - summaries quote the 'N+ bought in past month' badges, the best available sales signal; rank by them and call the ranking estimated. 2) Phrase the category by function, not a brand-like name (e.g. 'water bottle tracks intake reminder', not 'smart water'), or the results drift to a brand with the same words. 3) For each pick, WebSearch '<BRAND MODEL> price' on amazon.com; take prices from search-page snippets (often coupon-adjusted) and note it. 4) If a listing has no price, use a dated review roundup that quotes the Amazon price range, and label the source. 5) WebSearch with allowed_domains ["asinsight.com"] gives modeled monthly-sales estimates for some keywords (niche keywords may be missing). 6) Ask the owner to allow amazon.com, *.amazon.com, *.media-amazon.com, *.ssl-images-amazon.com for live prices and the official Best Sellers page.

## Tried first (did not work)
camelcamelcamel via WebSearch (allowed_domains camelcamelcamel.com) had no pages for niche smart products; Amazon has no dedicated Best Sellers node for some sub-categories, so 'best seller' searches return general roundups.

## How to check it worked
Each item in the reply has an amazon.com/dp/<ASIN> link, a sales-badge or source note, and a dated price or an explicit 'price not shown'.

## When this does not apply
Exact live price, stock, or Amazon's official Best Sellers rank: those need amazon.com allowed.
