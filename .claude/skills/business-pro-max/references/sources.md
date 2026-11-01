# Where to look

Sources by purpose. "Login" means it needs the owner's own signed-in Chrome (Claude in Chrome);
the rest are public. Check the dates on everything, because trends move weekly.

## Viral and trending
- TikTok Creative Center (`ads.tiktok.com/business/creativecenter`): top products, top ads,
  trending hashtags and songs, by country. Public; some filters need a login.
- TikTok search ("tiktok made me buy it", "<niche> gadget"), and Instagram reels in the niche
  (the `ig-viral` skill's method). Open any link with `open-social-link`.
- YouTube Shorts search, sorted by upload date plus views.
- Google Trends (`trends.google.com`): rising queries, by country and category.
- Amazon Movers & Shakers and Best Sellers. When amazon.com is blocked, use WebSearch with
  allowed_domains ["amazon.com"] for the "bought in past month" badges.
- AliExpress and Temu "hot" and "best sellers" lists, Etsy trending, Product Hunt, Exploding Topics,
  and Reddit (r/shutupandtakemymoney, r/BuyItForLife, niche subs).

## Cheap sources (suppliers and deals)
- Alibaba (`alibaba.com`): bulk, MOQ, Trade Assurance. Use `product-sourcing` for the search.
- AliExpress (`aliexpress.com`): single units, samples, dropshipping.
- 1688 (`1688.com`): the Chinese domestic price; reference only, buying needs an agent.
- DHgate and Temu: price reference.
- Local marketplaces for underpriced items and arbitrage: Yad2 (`yad2.co.il`), and Facebook
  Marketplace (login). Read only; the owner contacts the seller.
- Liquidation and closeout lots, and local importers' clearance sales (search the niche plus
  "חיסול" / "סגירת מלאי").

## Competitors and their marketing
- Meta Ad Library (`facebook.com/ads/library`): every active ad by page and country, and how long
  it has run. Long-running ads are profitable ones. Public; more filters with a login.
- TikTok Creative Center top ads: the hooks and formats that convert in the niche.
- The competitor's site and social accounts: price, offer, bundles, guarantee, shipping promise.
  Their reviews and comments show unmet needs.
- Google Shopping and Zap (`zap.co.il`) for local prices.
- SimilarWeb-style traffic estimates. These are often paywalled; do not pay without approval.

## Demand and price
- "bought in past month" badges, review counts and review velocity on Amazon
- eBay sold listings
- Google Trends seasonality
- The number of local sellers and their review counts
- Zap price ranges

## Rules and risk in Israel (always use the official, current source)
- Israel Tax Authority, customs (`gov.il`): duty rates, import VAT, personal-import limits
- Standards Institution of Israel (`sii.org.il`), and the import rules for electrical, wireless
  (Ministry of Communications) and health products (Ministry of Health)
- Trademarks: the Israel Patent Office database. For global marks, WIPO Brand Database.

## Domains to allow when the network is Limited
If the environment is not on Full access, these cover the sources above. Each site also needs its
`*.` subdomains:

```
tiktok.com  *.tiktok.com  *.tiktokcdn.com  *.ttwstatic.com
facebook.com  *.facebook.com  *.fbcdn.net
instagram.com  *.instagram.com  *.cdninstagram.com
youtube.com  *.youtube.com  *.ytimg.com  *.googlevideo.com
trends.google.com
amazon.com  *.amazon.com  *.media-amazon.com  *.ssl-images-amazon.com
ebay.com  *.ebay.com  *.ebayimg.com
aliexpress.com  *.aliexpress.com  *.alicdn.com
alibaba.com  *.alibaba.com
1688.com  *.1688.com
temu.com  *.temu.com
etsy.com  *.etsy.com  *.etsystatic.com
reddit.com  *.reddit.com  *.redd.it
producthunt.com  *.producthunt.com
explodingtopics.com
yad2.co.il  *.yad2.co.il
zap.co.il  *.zap.co.il
gov.il  *.gov.il
sii.org.il  *.sii.org.il
```

Full access is one setting instead of this list. It is in the cloud environment menu, under Edit,
then Network access.
