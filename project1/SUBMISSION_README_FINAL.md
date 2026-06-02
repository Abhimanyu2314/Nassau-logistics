# Nassau TITAN - Final Submission Build

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   streamlit run app.py
   ```

Windows users can also run `run_project.bat`.

## Main Requirement Pages

- **Dashboard** - overall logistics KPI overview
- **Route Efficiency** - top/bottom factory-to-customer routes, route score, route drill-down
- **Geographic Analysis** - US heatmap, regional bottleneck analysis, route network
- **Ship Mode Analysis** - lead-time comparison, delay comparison, cost-time tradeoff
- **Data Quality** - validation, required field coverage, factory mapping verification, compliance audit
- **Executive Summary** - stakeholder-ready insights and recommendations

## Dataset Upload

The app supports CSV/XLSX input. Required fields are auto-detected using common aliases. Missing optional identifiers are created safely so the dashboard does not break.

## Requirement Satisfaction

See `FINAL_REQUIREMENT_SATISFACTION_REPORT.md` for the full checklist.
