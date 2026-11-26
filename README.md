# Chexlow Cross-Store Price Spread Benchmark

Open aggregated pricing benchmark measuring how much identical fashion, beauty, handbags, footwear, and sports apparel items vary across verified online retailers on [Chexlow](https://chexlow.com).

- **Live interactive report**: https://chexlow.com/research/price-spread
- **Hugging Face dataset**: https://huggingface.co/datasets/mkan/chexlow-price-spread-benchmark
- **Live read-only API endpoint** (`GET`, no auth): `https://api.chexlow.com/api/v1/catalog/discovery/price-spread-report?siteDomain=chexlow&minStoreCount=3`
- **Developer docs, OpenAPI & Remote MCP**: https://chexlow.com/developers (`https://chexlow.com/openapi.json`, `https://chexlow.com/mcp`)

## Snapshot Summary (`2026-11-26T02:54:21.100Z`)

| Metric | Value |
|---|---|
| Products analyzed (`store_count >= 3`) | **1,749** |
| Outliers excluded (`highest / lowest > 4x`) | **11** |
| Products with cross-store spread | **1,684 (96.3%)** |
| Distinct verified merchants | **30** |
| Distinct brands | **273** |
| Median price spread | **22.3% ($72.37 USD)** |
| Average price spread | **23.6% ($147.20 USD)** |

## Category Breakdown (Top 10 by Product Count)

| Category | Products | Average Spread | Median Spread | Median Savings (USD) |
|---|---:|---:|---:|---:|
| Women's Clothing | 314 | 25.1% | 22.3% | $108.37 |
| Handbags | 207 | 25.7% | 24.8% | $179.77 |
| Men's Clothing | 203 | 26.4% | 25.2% | $107.85 |
| Fashion | 185 | 24.9% | 23.4% | $87.91 |
| Women's Shoes | 179 | 25.5% | 22.8% | $100.40 |
| Men's Shoes | 109 | 27.1% | 26.9% | $77.78 |
| Fragrances | 57 | 32.8% | **33.3%** | $53.64 |
| Skincare | 50 | 11.7% | **3.4%** | $2.54 |
| Moisturizers | 49 | 8.0% | **3.4%** | $2.89 |
| Hair Styling | 28 | 20.2% | 13.5% | $6.50 |

## Brand Highlights

| Brand | Products | Average Spread | Median Spread | Average Savings (USD) |
|---|---:|---:|---:|---:|
| Pinko | 102 | 24.0% | 22.9% | $102.67 |
| Adidas | 65 | 34.7% | 30.0% | $25.72 |
| Nike | 48 | 18.1% | 17.5% | $22.31 |
| Dolce & Gabbana | 46 | 29.3% | 29.8% | $392.18 |
| Brunello Cucinelli | 42 | 25.5% | 31.5% | $862.34 |
| Golden Goose | 40 | 24.8% | 21.2% | $177.26 |
| Diesel | 32 | 39.7% | 36.8% | $231.44 |
| The North Face | 30 | 14.8% | 12.0% | $22.90 |
| Gucci | 27 | 27.1% | 36.8% | $332.34 |
| New Balance | 27 | 36.7% | 33.6% | $73.57 |
| Dermalogica | 27 | 6.8% | 4.8% | $4.68 |
| Oribe | 27 | 11.5% | 3.4% | $11.08 |

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
