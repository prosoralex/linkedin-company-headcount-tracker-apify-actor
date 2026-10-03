"""
Run the "LinkedIn Company Headcount Tracker — Employee Growth Alerts" Apify Actor and print its results.

Setup:
    pip install -r requirements.txt
    export APIFY_TOKEN=your_apify_token   # Apify Console > Settings > API & Integrations

This repository only documents the Actor; its source code runs on Apify's infrastructure.
"""
import os
import sys

from apify_client import ApifyClient

ACTOR_ID = "leadsbrary/linkedin-company-headcount-tracker"

RUN_INPUT = {
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


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).")
    client = ApifyClient(token)
    print(f"Starting {ACTOR_ID} ...")
    run = client.actor(ACTOR_ID).call(run_input=RUN_INPUT)
    print(f"Run finished with status: {run['status']}")
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)


if __name__ == "__main__":
    main()
