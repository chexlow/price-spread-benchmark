#!/usr/bin/env python3
"""Fetch the live Chexlow cross-store price spread report without authentication."""

import json
import sys
import urllib.request

ENDPOINT = (
    "https://api.chexlow.com/api/v1/catalog/discovery/price-spread-report"
    "?siteDomain=chexlow&minStoreCount=3"
)


def main() -> None:
    req = urllib.request.Request(
        ENDPOINT,
        headers={"Accept": "application/json", "User-Agent": "chexlow-price-spread-benchmark/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
