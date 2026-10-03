#!/usr/bin/env bash
# Run the "LinkedIn Company Headcount Tracker — Employee Growth Alerts" Apify Actor synchronously and print the dataset items.
# Usage: export APIFY_TOKEN=your_apify_token && ./run.sh
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN first (Apify Console > Settings > API & Integrations)}"

curl -sS -X POST "https://api.apify.com/v2/acts/leadsbrary~linkedin-company-headcount-tracker/run-sync-get-dataset-items" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "companies": [
    "https://www.linkedin.com/company/apify/",
    "https://www.linkedin.com/company/microsoft/"
  ],
  "historyStoreName": "linkedin-headcount-history",
  "alertThresholdPct": 5,
  "includeHistory": false,
  "maxHistoryPoints": 104,
  "maxResults": 3,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": [
      "RESIDENTIAL"
    ]
  }
}
JSON
