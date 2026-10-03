// Run the "LinkedIn Company Headcount Tracker — Employee Growth Alerts" Apify Actor and print its results.
// Setup: npm install  &&  export APIFY_TOKEN=your_apify_token  &&  node example.mjs
// This repository only documents the Actor; its source code runs on Apify's infrastructure.
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set the APIFY_TOKEN environment variable first (Apify Console > Settings > API & Integrations).');
    process.exit(1);
}

const client = new ApifyClient({ token });

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
console.log(`Run finished with status: ${run.status}`);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(JSON.stringify(items, null, 2));
