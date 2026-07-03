[Uploading README_2.md…]()
# RetailPulse Dashboard

**A self-contained, interactive sales & customer intelligence console** — built with vanilla HTML/CSS/JS and Plotly.js. No build step, no server, no dependencies to install. Open the file and it runs.

![Python](https://img.shields.io/badge/no%20backend-static%20HTML-blue)
![Plotly.js](https://img.shields.io/badge/charts-Plotly.js-3F4F75)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Live demo

[**View the live dashboard**](https://archanavijayan0112-spec.github.io/retailpulse-dashboard/) *(enable GitHub Pages on this repo — see below)*

## What it shows

A single-page analytics console for a 2-year, multi-region e-commerce operation:

- **Live KPI ticker** — scrolling headline metrics (revenue, margin, orders, AOV, top region/category)
- **Revenue forecast** — 90-day projection with an 80% confidence band, plotted against historical actuals
- **Category & regional breakdown** — donut and bar charts of revenue by product category, region, and city
- **RFM customer segmentation** — Champions, At Risk, Lost, and other segments by customer count
- **Cohort retention heatmap** — month-over-month retention rate by signup cohort

All data is pre-computed and embedded directly in the page (`<script id="dashboard-data" type="application/json">`), so there's nothing to fetch and no CORS issues when opened locally.

## Run it locally

No installation needed — just open the file:

```bash
git clone https://github.com/archanavijayan0112-spec/retailpulse-dashboard.git
cd retailpulse-dashboard
open index.html      # macOS
# or just double-click index.html in Finder/Explorer
```

## Deploy to GitHub Pages

1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Source**, select the `main` branch and `/ (root)` folder.
4. Save — your dashboard will be live at `https://<your-username>.github.io/<repo-name>/` within a minute or two.

## Tech stack

| Layer | Choice |
|---|---|
| Charts | [Plotly.js](https://plotly.com/javascript/) (via CDN) |
| Fonts | Space Grotesk, Inter, JetBrains Mono (Google Fonts) |
| Styling | Plain CSS with custom properties, no framework |
| Data | Static JSON embedded in the page — no backend |

## Data note

The dataset behind this dashboard is **synthetic**, generated to reflect realistic e-commerce patterns (seasonality around festive periods, regional variance across Indian cities, customer churn behavior) for portfolio/demonstration purposes. No real customer or transaction data is used.

## License

MIT
