#!/usr/bin/env python3
"""Refresh data CSVs, dated JSON snapshot, and README tables from the live Chexlow API."""

from __future__ import annotations

import csv
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENDPOINT = (
    "https://api.chexlow.com/api/v1/catalog/discovery/price-spread-report"
    "?siteDomain=chexlow&minStoreCount=3"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
README_PATH = REPO_ROOT / "README.md"

START_MARKER = "<!-- SNAPSHOT_START -->"
END_MARKER = "<!-- SNAPSHOT_END -->"


def fetch_report() -> dict[str, Any]:
    req = urllib.request.Request(
        ENDPOINT,
        headers={
            "Accept": "application/json",
            "User-Agent": "chexlow-price-spread-benchmark/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        payload = json.load(resp)

    summary = payload.get("summary") or {}
    categories = payload.get("categories") or []
    brands = payload.get("brands") or []
    examples = payload.get("featuredExamples") or []

    analyzed = int(summary.get("analyzedProductCount") or 0)
    if analyzed <= 0 or not categories or not brands or not examples:
        raise ValueError(
            f"Incomplete report payload: analyzed={analyzed}, "
            f"categories={len(categories)}, brands={len(brands)}, examples={len(examples)}"
        )

    return payload


def fmt_num(value: Any) -> Any:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def fmt_usd(value: float) -> str:
    if value < 100:
        return f"${value:,.2f}"
    return f"${value:,.2f}"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def render_snapshot_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    categories = payload["categories"][:10]
    brands = payload["brands"]

    observed_at = str(summary["observedAt"])
    analyzed = int(summary["analyzedProductCount"])
    excluded = int(summary["excludedOutlierCount"])
    ratio_guard = fmt_num(summary["maxSpreadRatioGuard"])
    min_stores = int(summary["minStoreCount"])
    with_spread = int(summary["productsWithSpreadCount"])
    spread_share = float(summary["productsWithSpreadSharePct"])
    merchants = int(summary["distinctMerchantCount"])
    brand_count = int(summary["distinctBrandCount"])
    median_pct = float(summary["medianSpreadPct"])
    avg_pct = float(summary["averageSpreadPct"])
    median_usd = float(summary["medianSavingsUsd"])
    avg_usd = float(summary["averageSavingsUsd"])

    lines: list[str] = [
        START_MARKER,
        f"## Snapshot Summary (`{observed_at}`)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Products analyzed (`store_count >= {min_stores}`) | **{analyzed:,}** |",
        f"| Outliers excluded (`highest / lowest > {ratio_guard}x`) | **{excluded:,}** |",
        f"| Products with cross-store spread | **{with_spread:,} ({spread_share:.1f}%)** |",
        f"| Distinct verified merchants | **{merchants:,}** |",
        f"| Distinct brands | **{brand_count:,}** |",
        f"| Median price spread | **{median_pct:.1f}% ({fmt_usd(median_usd)} USD)** |",
        f"| Average price spread | **{avg_pct:.1f}% ({fmt_usd(avg_usd)} USD)** |",
        "",
        "## Category Breakdown (Top 10 by Product Count)",
        "",
        "| Category | Products | Average Spread | Median Spread | Median Savings (USD) |",
        "|---|---:|---:|---:|---:|",
    ]

    for row in categories:
        lines.append(
            f"| {row['name']} | {int(row['productCount']):,} | "
            f"{float(row['averageSpreadPct']):.1f}% | **{float(row['medianSpreadPct']):.1f}%** | "
            f"{fmt_usd(float(row['medianSavingsUsd']))} |"
        )

    lines.extend(
        [
            "",
            "## Brand Highlights",
            "",
            "| Brand | Products | Average Spread | Median Spread | Average Savings (USD) |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    for row in brands:
        lines.append(
            f"| {row['name']} | {int(row['productCount']):,} | "
            f"{float(row['averageSpreadPct']):.1f}% | {float(row['medianSpreadPct']):.1f}% | "
            f"{fmt_usd(float(row['averageSavingsUsd']))} |"
        )

    lines.append(END_MARKER)
    return "\n".join(lines)


def main() -> None:
    payload = fetch_report()
    summary = payload["summary"]

    observed_dt = datetime.fromisoformat(
        str(summary["observedAt"]).replace("Z", "+00:00")
    ).astimezone(timezone.utc)
    date_slug = observed_dt.strftime("%Y-%m-%d")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = DATA_DIR / f"snapshot-{date_slug}.json"
    snapshot_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    write_csv(
        DATA_DIR / "summary.csv",
        [
            "observed_at",
            "site_domain",
            "min_store_count",
            "max_spread_ratio_guard",
            "analyzed_product_count",
            "excluded_outlier_count",
            "products_with_spread_count",
            "products_with_spread_share_pct",
            "distinct_merchant_count",
            "distinct_brand_count",
            "average_spread_pct",
            "median_spread_pct",
            "average_savings_usd",
            "median_savings_usd",
        ],
        [
            {
                "observed_at": summary["observedAt"],
                "site_domain": summary["siteDomain"],
                "min_store_count": summary["minStoreCount"],
                "max_spread_ratio_guard": fmt_num(summary["maxSpreadRatioGuard"]),
                "analyzed_product_count": summary["analyzedProductCount"],
                "excluded_outlier_count": summary["excludedOutlierCount"],
                "products_with_spread_count": summary["productsWithSpreadCount"],
                "products_with_spread_share_pct": fmt_num(
                    summary["productsWithSpreadSharePct"]
                ),
                "distinct_merchant_count": summary["distinctMerchantCount"],
                "distinct_brand_count": summary["distinctBrandCount"],
                "average_spread_pct": fmt_num(summary["averageSpreadPct"]),
                "median_spread_pct": fmt_num(summary["medianSpreadPct"]),
                "average_savings_usd": fmt_num(summary["averageSavingsUsd"]),
                "median_savings_usd": fmt_num(summary["medianSavingsUsd"]),
            }
        ],
    )

    write_csv(
        DATA_DIR / "categories.csv",
        [
            "slug",
            "name",
            "product_count",
            "average_spread_pct",
            "median_spread_pct",
            "average_savings_usd",
            "median_savings_usd",
        ],
        [
            {
                "slug": row["slug"],
                "name": row["name"],
                "product_count": row["productCount"],
                "average_spread_pct": fmt_num(row["averageSpreadPct"]),
                "median_spread_pct": fmt_num(row["medianSpreadPct"]),
                "average_savings_usd": fmt_num(row["averageSavingsUsd"]),
                "median_savings_usd": fmt_num(row["medianSavingsUsd"]),
            }
            for row in payload["categories"]
        ],
    )

    write_csv(
        DATA_DIR / "brands.csv",
        [
            "slug",
            "name",
            "product_count",
            "average_spread_pct",
            "median_spread_pct",
            "average_savings_usd",
        ],
        [
            {
                "slug": row["slug"],
                "name": row["name"],
                "product_count": row["productCount"],
                "average_spread_pct": fmt_num(row["averageSpreadPct"]),
                "median_spread_pct": fmt_num(row["medianSpreadPct"]),
                "average_savings_usd": fmt_num(row["averageSavingsUsd"]),
            }
            for row in payload["brands"]
        ],
    )

    write_csv(
        DATA_DIR / "featured_examples.csv",
        [
            "slug",
            "category_slug",
            "category_name",
            "name",
            "brand_name",
            "store_count",
            "lowest_store_price_usd",
            "highest_store_price_usd",
            "savings_usd",
            "spread_pct",
            "lowest_merchant_name",
            "highest_merchant_name",
            "chexlow_url",
        ],
        [
            {
                "slug": row["slug"],
                "category_slug": row["categorySlug"],
                "category_name": row["categoryName"],
                "name": row["name"],
                "brand_name": row.get("brandName") or "",
                "store_count": row["storeCount"],
                "lowest_store_price_usd": fmt_num(row["lowestStorePriceUsd"]),
                "highest_store_price_usd": fmt_num(row["highestStorePriceUsd"]),
                "savings_usd": fmt_num(row["savingsUsd"]),
                "spread_pct": fmt_num(row["spreadPct"]),
                "lowest_merchant_name": row["lowestMerchantName"],
                "highest_merchant_name": row["highestMerchantName"],
                "chexlow_url": f"https://chexlow.com/compare/{row['categorySlug']}/{row['slug']}",
            }
            for row in payload["featuredExamples"]
        ],
    )

    readme = README_PATH.read_text(encoding="utf-8")
    if START_MARKER not in readme or END_MARKER not in readme:
        raise RuntimeError("README.md is missing SNAPSHOT_START / SNAPSHOT_END markers")
    updated_block = render_snapshot_markdown(payload)
    new_readme = re.sub(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        lambda _: updated_block,
        readme,
        flags=re.DOTALL,
    )
    README_PATH.write_text(new_readme, encoding="utf-8")
    print(
        f"Updated snapshot {date_slug}: analyzed={summary['analyzedProductCount']}, "
        f"categories={len(payload['categories'])}, brands={len(payload['brands'])}, "
        f"examples={len(payload['featuredExamples'])}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error updating snapshot: {exc}", file=sys.stderr)
        sys.exit(1)
