# Chexlow Cross-Store Price Spread Benchmark

Open aggregated pricing benchmark measuring how much identical fashion, beauty, handbags, footwear, and sports apparel items vary across verified online retailers on [Chexlow](https://chexlow.com).

- **Live interactive report**: https://chexlow.com/research/price-spread
- **Hugging Face dataset**: https://huggingface.co/datasets/mkan/chexlow-price-spread-benchmark
- **Live read-only API endpoint** (`GET`, no auth): `https://api.chexlow.com/api/v1/catalog/discovery/price-spread-report?siteDomain=chexlow&minStoreCount=3`
- **Developer docs, OpenAPI & Remote MCP**: https://chexlow.com/developers (`https://chexlow.com/openapi.json`, `https://chexlow.com/mcp`)

<!-- SNAPSHOT_START -->
## Snapshot Summary (`2026-11-26T23:20:00.266Z`)

| Metric | Value |
|---|---|
| Products analyzed (`store_count >= 3`) | **1,732** |
| Outliers excluded (`highest / lowest > 4x`) | **12** |
| Products with cross-store spread | **1,668 (96.3%)** |
| Distinct verified merchants | **29** |
| Distinct brands | **273** |
| Median price spread | **22.3% ($71.06 USD)** |
| Average price spread | **23.6% ($146.46 USD)** |

## Category Breakdown (Top 10 by Product Count)

| Category | Products | Average Spread | Median Spread | Median Savings (USD) |
|---|---:|---:|---:|---:|
| Women's Clothing | 315 | 24.9% | **22.3%** | $105.34 |
| Handbags | 208 | 25.6% | **24.5%** | $181.96 |
| Men's Clothing | 193 | 27.0% | **28.3%** | $112.58 |
| Fashion | 180 | 24.8% | **24.1%** | $87.27 |
| Women's Shoes | 177 | 25.1% | **22.9%** | $103.60 |
| Men's Shoes | 103 | 27.3% | **26.9%** | $78.77 |
| Fragrances | 59 | 32.8% | **33.3%** | $53.35 |
| Skincare | 50 | 11.7% | **3.4%** | $2.54 |
| Moisturizers | 49 | 7.9% | **3.4%** | $2.89 |
| Hair Styling | 28 | 20.2% | **13.5%** | $6.50 |

## Brand Highlights

| Brand | Products | Average Spread | Median Spread | Average Savings (USD) |
|---|---:|---:|---:|---:|
| Pinko | 105 | 23.4% | 22.3% | $98.59 |
| Adidas | 64 | 35.2% | 30.0% | $26.27 |
| Nike | 51 | 19.3% | 18.2% | $23.26 |
| Dolce & Gabbana | 45 | 29.2% | 29.4% | $396.53 |
| Golden Goose | 41 | 24.9% | 21.2% | $178.17 |
| Brunello Cucinelli | 39 | 25.6% | 31.3% | $869.39 |
| Diesel | 29 | 40.0% | 37.1% | $233.93 |
| The North Face | 28 | 14.6% | 10.7% | $23.21 |
| Gucci | 27 | 27.0% | 36.8% | $330.90 |
| Dermalogica | 27 | 6.4% | 4.8% | $4.35 |
| Oribe | 27 | 11.5% | 3.4% | $11.08 |
| New Balance | 26 | 34.2% | 32.9% | $69.19 |
<!-- SNAPSHOT_END -->

## Methodology

1. **Public gate eligibility**: Scans active Chexlow catalog products (`status = active`, `offer_count > 0`, `store_count >= 3`, categorized).
2. **Per-merchant normalization**: Computes each verified merchant's lowest active USD-normalized offer (`MIN(effective_price_usd)`) so multi-size or multi-variant listings from the same store do not inflate store counts or spreads.
3. **Outlier guard**: Excludes items where `highest_store_price_usd / lowest_store_price_usd > 4` (`11` items excluded in this snapshot) to filter extreme variant or feed mismatches.
4. **Spread formula**: `spread_pct = (highest - lowest) / highest * 100`, `savings_usd = highest - lowest`.

## Repository Contents

- `data/snapshot-2026-11-26.json` — Raw public API response captured on `2026-11-26T02:54:21.100Z`.
- `data/summary.csv` — Top-level aggregate metrics (`1` row).
- `data/categories.csv` — Category breakdown (`10` rows).
- `data/brands.csv` — Brand breakdown (`12` rows).
- `data/featured_examples.csv` — Verified multi-store product examples (`8` rows) with live comparison URLs.
- `scripts/fetch_live_report.py` & `scripts/fetch_live_report.sh` — Reproducible scripts to pull the latest live snapshot from the public API.
- `scripts/update_snapshot.py` & `.github/workflows/weekly-snapshot.yml` — Automated weekly snapshot refresher updating CSVs, dated JSON, and summary tables every Monday at `06:00 UTC`.

## Reproduce Live Snapshot

```bash
python3 scripts/fetch_live_report.py > data/latest.json
# or
bash scripts/fetch_live_report.sh
```

## License & Citation

Released under [CC-BY-4.0](LICENSE). Please cite [Chexlow's live report](https://chexlow.com/research/price-spread):

```bibtex
@misc{chexlow2026pricespread,
  title  = {Chexlow Cross-Store Fashion & Beauty Price Spread Benchmark},
  author = {{Chexlow}},
  year   = {2026},
  month  = {11},
  url    = {https://chexlow.com/research/price-spread}
}
```
