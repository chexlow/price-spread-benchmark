#!/usr/bin/env bash
set -euo pipefail

curl -fsSL \
  "https://api.chexlow.com/api/v1/catalog/discovery/price-spread-report?siteDomain=chexlow&minStoreCount=3"
