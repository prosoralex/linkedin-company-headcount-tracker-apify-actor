# LinkedIn Company Headcount Tracker — Employee Growth Alerts — Apify Actor usage guide

[![Run on Apify](https://img.shields.io/badge/Apify-Run%20this%20Actor-24C1E0)](https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara)
[![Try Apify free](https://img.shields.io/badge/Apify-Try%20it%20free-24C1E0)](https://console.apify.com/sign-up?fpr=aupara)

Track LinkedIn company headcount over time. Returns employee count, size range, followers, growth % and change since your previous run, with alerts. Schedule it and export JSON, CSV or Excel. From $1.0 per 1,000 results.

> **This repository does not contain the Actor's source code.** The Actor is closed-source and
> runs on Apify's infrastructure. This repo is documentation plus ready-to-run client examples
> (curl, Python, JavaScript) that call the hosted Actor with **your own** Apify API token.

**Run it on Apify →** [https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara](https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara)

## What it does

**LinkedIn Company Headcount Tracker** reads the public LinkedIn company page for each company you list and returns its employee count, size range, follower count, industry, headquarters and website. It also remembers every check. On each new run it adds the change since the previous check: employee delta, growth %, monthly-normalised growth, follower delta, a `trend` label and an `alert` flag.

Run it on a schedule (weekly is typical) and you get a headcount time series for any set of companies, without logging in to LinkedIn.

## Use cases

- Weekly scheduled run over a list of target accounts: export headcount delta and % growth to Google Sheets/CRM via integrations.
- Flag companies whose headcount grew or shrank more than X % since the last check as sales or investment signals (webhook/Slack on alert rows).
- Track competitors' or portfolio companies' headcount curve over months using the stored history.
- One-off enrichment of a company list with current LinkedIn employee count and follower count (first run = baseline).


## Input

| Field | Type | Required | Description |
|---|---|---|---|
| `companies` | array | yes | LinkedIn company page URLs (https://www.linkedin.com/company/apify/) or bare slugs (apify). Other URL types (profiles, jobs, search) get a free error row. |
| `historyStoreName` | string | no | Named key-value store that keeps every past check. Use the same name on each scheduled run to get deltas; change it to start a separate tracking list. |
| `alertThresholdPct` | number | no | A row gets alert=true when the employee count changed by at least this many percent since the previous check. |
| `includeHistory` | boolean | no | Add the stored history (date, employee count, followers) to each row. |
| `maxHistoryPoints` | integer | no | Checks kept per company in the store; the oldest are dropped. 104 is about two years of weekly runs. |
| `maxResults` | integer | no | Maximum number of companies processed in this run (also protects your spending). Only rows with status ok are charged. |
| `proxyConfiguration` | object | no | LinkedIn blocks most direct and datacenter traffic; residential proxy is the default and recommended. |

The full input form (with defaults and validation) is on the [Actor page](https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara).


## Output (sample item)

Sample trimmed for readability (long texts and lists are shortened) — a real run returns the complete data.

```json
{
  "companySlug": "apify",
  "companyUrl": "https://www.linkedin.com/company/apify/",
  "inputValue": "https://www.linkedin.com/company/apify/",
  "status": "ok",
  "companyName": "Apify",
  "employeeCount": 272,
  "companySizeRange": "201-500 employees",
  "followerCount": 39865,
  "industry": "Technology, Information and Internet",
  "headquarters": "Prague",
  "website": "https://apify.com/",
  "checkedAt": "2026-10-03T16:39:30.647Z",
  "previousEmployeeCount": 272,
  "previousCheckedAt": "2026-10-03T16:19:05.765Z",
  "daysSincePrevious": 0.01,
  "employeeDelta": 0,
  "employeeGrowthPct": 0,
  "employeeGrowthPctMonthly": null,
  "followerDelta": 3,
  "firstCheckedAt": "2026-10-03T16:16:20.084Z",
  "employeeGrowthPctSinceFirst": 0,
  "trend": "stable",
  "alert": false,
  "historyPoints": 3,
  "error": null
}
```

## Pricing

Pay only for results: about **$1.50 per 1,000 results** on the Apify Free plan, down to **$1.00 per 1,000** on paid Apify plans.

Apify platform usage (compute and residential proxy traffic) is billed by Apify on top of the per-result price — about **$0.29 per 1,000 results** in our measured test runs (estimate, varies with input). Tip: keep only the output formats and options you need to reduce it.

Prices can change — the [Actor page](https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara) always shows the current pricing.

## Quick start

You need an Apify account and an API token (Apify Console → **Settings → API & Integrations**).
Never commit your token: export it as the `APIFY_TOKEN` environment variable.

### cURL

```bash
curl -X POST "https://api.apify.com/v2/acts/leadsbrary~linkedin-company-headcount-tracker/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
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
```

### Python (`apify-client`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "companies": [
        "https://www.linkedin.com/company/apify/",
        "https://www.linkedin.com/company/microsoft/"
    ],
    "historyStoreName": "linkedin-headcount-history",
    "alertThresholdPct": 5,
    "includeHistory": False,
    "maxHistoryPoints": 104,
    "maxResults": 3,
    "proxyConfiguration": {
        "useApifyProxy": True,
        "apifyProxyGroups": [
            "RESIDENTIAL"
        ]
    }
}

run = client.actor("leadsbrary/linkedin-company-headcount-tracker").call(run_input=run_input)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### JavaScript (`apify-client`)

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const runInput = {
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
};

const run = await client.actor('leadsbrary/linkedin-company-headcount-tracker').call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

Runnable versions live in [`examples/`](./examples).

## Troubleshooting

- **401 / "User was not found or authentication token is not valid"** — check that `APIFY_TOKEN` is set and copied completely.
- **The run finished but the dataset is empty** — widen your search input or check the run log on the Apify Console.
- **Run stops early** — you may have reached the maximum cost per run you set in Apify; raise it in the run options.
- **Need something else?** Open an issue in this repository or use the Issues tab on the Actor page.

## Don't have an Apify account yet?

[Sign up here](https://console.apify.com/sign-up?fpr=aupara) — new accounts get $5 of free platform usage every month, enough to try most Actors without paying upfront.
Browse the full [Apify Store](https://apify.com/store?fpr=aupara) or [all Actors from this developer](https://apify.com/leadsbrary?fpr=aupara).

## Links

- Actor page: [https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara](https://apify.com/leadsbrary/linkedin-company-headcount-tracker?fpr=aupara)
- All Actors from this developer: [https://apify.com/leadsbrary?fpr=aupara](https://apify.com/leadsbrary?fpr=aupara)
- Apify API reference: [https://docs.apify.com/api/v2](https://docs.apify.com/api/v2)

## Keywords

linkedin company headcount tracker, linkedin employee count tracker, linkedin headcount growth, company headcount monitor, linkedin hiring growth signal, company employee count monitor, linkedin company employee count, headcount growth rate, linkedin follower count tracker, company growth signals, account based prospecting signals, linkedin company scraper, headcount change alert

#linkedin #headcount #companydata #hiringsignals #leadgeneration #salesintelligence #marketresearch #firmographics #monitoring #apify

## License

The example code in this repository is released under the MIT License — see [LICENSE](./LICENSE).
It does not cover the Actor itself, which remains closed-source and is operated by its developer on Apify.
