````markdown
# 🧪 ABlytics

**ABlytics** is an experiment analytics platform built to help teams analyze A/B experiments, compare variants, measure conversion performance, and make statistically informed decisions.

It supports **manual A/B analysis** and **Google Analytics 4 (GA4)-based analysis** through a common analytical pipeline.

---

## 🚀 Features

### Manual A/B Testing
Enter Variant A and Variant B data manually and analyze:

- Conversion Rate
- Click-Through Rate
- Bounce Rate
- Revenue
- Users
- Sessions
- Funnel performance
- Statistical significance

### Historical GA4 Comparison

Compare two GA4 date ranges to understand changes in performance.

```text
Period A  →  Period B
````

Useful for before/after analysis when a simultaneous A/B experiment is not available.

### True A/B Experiment

Designed to analyze actual Variant A vs Variant B experiment data from GA4.

> GA4 experiment-level data ingestion is currently under development.

### Statistical Analysis

ABlytics separates metric calculation from statistical analysis so experiment results can be evaluated systematically rather than relying only on raw percentage differences.

### Interactive Dashboard

Results are presented through:

* Metric summaries
* Variant comparisons
* Statistical results
* Funnel analysis
* Experiment verdicts
* Recommendations
* Export options

---

# 🏗️ Architecture

```text
                  ┌──────────────────┐
                  │    Streamlit UI  │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
        Manual A/B                  GA4 Analysis
             │                           │
             │                  ┌────────┴────────┐
             │                  │                 │
             │             Historical         True A/B
             │                  │                 │
             └────────────┬─────┴─────────────────┘
                          │
                   StandardDataset
                          │
                    ┌─────▼─────┐
                    │ Validation│
                    └─────┬─────┘
                          │
                   Analysis Engine
                          │
          ┌───────────────┼───────────────┐
          │               │               │
       Metrics        Comparison        Funnel
          │               │               │
          └───────────────┼───────────────┘
                          │
                  Statistical Analysis
                          │
                    ┌─────▼─────┐
                    │ Dashboard │
                    └───────────┘
```

---

# 📁 Project Structure

```text
ABlytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── analytics/
│   ├── metrics.py
│   ├── comparison.py
│   └── funnel.py
│
├── components/
│   ├── alerts.py
│   ├── buttons.py
│   ├── cards.py
│   ├── footer.py
│   ├── google_connection.py
│   ├── hero.py
│   ├── loaders.py
│   ├── navbar.py
│   └── property_selector.py
│
├── config/
│   ├── constants.py
│   └── settings.py
│
├── core/
│   └── schema.py
│
├── engine/
│   └── analysis_engine.py
│
├── experiments/
│   ├── manual.py
│   ├── historical.py
│   └── true_ab.py
│
├── ga4/
│   ├── auth.py
│   ├── client.py
│   ├── fetcher.py
│   └── parser.py
│
├── pages/
│   ├── home.py
│   ├── configuration.py
│   └── dashboard.py
│
├── stats_engine/
│   └── decision.py
│
├── validation/
│   └── validator.py
│
├── visualization/
│   ├── summary_panel.py
│   ├── verdict_banner.py
│   ├── metric_cards.py
│   ├── comparison_table.py
│   ├── statistics_panel.py
│   ├── recommendation_panel.py
│   ├── funnel_chart.py
│   └── export_panel.py
│
├── tests/
│
└── assets/
    └── style.css
```

---

# 🔄 Analysis Pipeline

Every analysis mode is converted into a common `StandardDataset`.

```text
Input Data
    ↓
StandardDataset
    ↓
Validation
    ↓
Metric Calculation
    ↓
Variant Comparison
    ↓
Funnel Analysis
    ↓
Statistical Analysis
    ↓
Experiment Verdict
    ↓
Dashboard
```

This allows Manual, Historical, and True A/B analysis to use the same downstream analytical engine.

---

# 🧩 Standard Data Model

The core contract is defined in:

```text
core/schema.py
```

### `VariantData`

Stores measurements for an individual variant.

```python
VariantData(
    visitors=...,
    conversions=...,
    impressions=...,
    clicks=...,
    sessions=...,
    bounces=...,
    revenue=...,
    users=...,
    new_users=...,
    session_duration=...
)
```

### `FunnelStep`

Represents one stage of an experiment funnel.

### `StandardDataset`

```python
StandardDataset(
    source=...,
    selected_metrics=...,
    variant_a=...,
    variant_b=...,
    funnel_steps=...
)
```

The common schema prevents each data source from producing a different structure for the analysis engine.

---

# 📊 GA4 Integration

ABlytics uses Google Analytics APIs for GA4-based analysis.

The integration is divided into:

```text
ga4/auth.py
        ↓
Authentication

ga4/client.py
        ↓
GA4 Admin API

ga4/fetcher.py
        ↓
GA4 Data API

ga4/parser.py
        ↓
Standardized application data
```

The application can retrieve available GA4 properties and fetch GA4 reporting data when the connected Google account has sufficient permissions.

---

# 🔐 Security

OAuth credentials and tokens must **never be committed to GitHub**.

The following files are intentionally excluded:

```text
credentials.json
token.json
.env
.streamlit/secrets.toml
```

Example `.gitignore`:

```gitignore
credentials.json
token.json
.env
.streamlit/secrets.toml

venv/
.venv/
__pycache__/
*.py[cod]
```

For deployment, sensitive credentials should be configured through the deployment platform's secret-management system rather than committed to the repository.

---

# 💻 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/Tarun-015/ABlytics.git
cd ABlytics
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 4. Run ABlytics

```powershell
streamlit run app.py
```

The application will open in your browser.

---

# 🧪 Manual A/B Example

Manual analysis does not require a live website or GA4 data.

Example:

```text
Variant A
Visitors:    10,000
Conversions:  500

Variant B
Visitors:    10,000
Conversions:  560
```

ABlytics can then compare the variants and perform statistical analysis rather than simply reporting:

```text
A = 5.0%
B = 5.6%
```

The goal is to determine whether the observed difference provides sufficient statistical evidence for a meaningful experiment decision.

---

# 🌐 GA4 Historical Comparison

Historical comparison uses two date ranges:

```text
Period A
    ↓
GA4

Period B
    ↓
GA4
```

The retrieved data is normalized into:

```text
Variant A ← Period A
Variant B ← Period B
```

This allows the existing analysis pipeline to compare the two periods.

If a GA4 property has no traffic, the returned values can legitimately be:

```text
Sessions      0
Users         0
Conversions   0
```

This is treated as missing/insufficient analytical data rather than fabricated results.

---

#  Current Status

| Feature                      | Status            |
| ---------------------------- | ----------------- |
| Manual A/B Analysis          | ✅ Working         |
| Common Data Model            | ✅ Implemented     |
| Validation Layer             | ✅ Implemented     |
| Metrics Engine               | ✅ Implemented     |
| Statistical Engine           | ✅ Implemented     |
| Dashboard                    | ✅ Implemented     |
| GA4 Authentication           | ✅ Implemented     |
| GA4 Property Selection       | ✅ Implemented     |
| Historical GA4 Comparison    | ✅ Implemented     |
| True GA4 Experiment Fetching | ✅ Implement       |
| Customer-level Google OAuth  | ✅ Implemented     |

---

# 🛣️ Roadmap

Future development includes:

* Complete GA4 True A/B experiment ingestion
* Customer-level Google authentication
* Automatic experiment/property discovery
* More statistical tests
* Power and sample-size analysis
* Confidence intervals
* Better experiment recommendations
* Experiment history
* Database-backed projects
* Automated report generation
* Production authentication
* Multi-user support

---

# 🛠️ Technology Stack

* **Python**
* **Streamlit**
* **Google Analytics 4 APIs**
* **Google OAuth 2.0**
* **NumPy**
* **SciPy**
* **Plotly**
* **OpenPyXL**
* **ReportLab**

---

# 🎯 Design Philosophy

ABlytics is designed around five principles:

**1. One data contract**

All analysis modes normalize data into `StandardDataset`.

**2. Separation of concerns**

The UI, data fetching, validation, analytics, statistics, and visualization layers remain separate.

**3. No fake results**

If the source contains no usable data, ABlytics should report that instead of generating artificial results.

**4. Reusable analysis engine**

Different data sources can use the same metrics and statistical pipeline.

**5. Extensible architecture**

Future sources such as CSV files, databases, or other analytics platforms can be added by mapping their data into the standard schema.

---

# 👨‍💻 Author

**Tarun Chaudhary**

Data Science & Analytics

---

## 📌 Project Status

ABlytics is an **completed deployed project** 
```

**ABlytics: Experiment Analytics, Without the Guesswork.**


