---
title: A store site returns nothing or blocks plain HTTP clients
tags: scraping, store, alibaba, curl_cffi, json, bot, product
saved: 2026-10-31
---

# A store site returns nothing or blocks plain HTTP clients

## Problem
requests/urllib get an empty page, a 403 from the site itself, or a page without the listings, while the site works in a browser.

## Solution
Use curl_cffi with impersonate='chrome' (installed in the cloud) at a low request rate, then read the JSON embedded in the page (search for productUrl, __NEXT_DATA__, application/ld+json) instead of parsing HTML. product-sourcing's product_search.py does this for Alibaba, AliExpress, Amazon and eBay. If you get a captcha or a login wall, stop: use another source or ask the owner.

## When this does not apply
Sites whose terms forbid automated access, or anything behind a login.
