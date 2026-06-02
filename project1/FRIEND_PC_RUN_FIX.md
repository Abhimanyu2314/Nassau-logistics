# Friend PC Run Fix / Compatibility Notes

If the project works on one PC but not another, it is usually caused by one of these:

1. Different Python version or package versions
2. Browser zoom / laptop screen resolution causing layout overlap
3. Old Streamlit cache
4. Running the wrong ZIP/folder copy

## Recommended clean run

Open CMD inside the project folder and run:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit cache clear
streamlit run app.py
```

## Browser setting
Use Chrome or Edge at 90% or 100% zoom.

## If a map fails
The project now includes a safe fallback table for the Live Logistics Map, so the app will not crash on PCs with Plotly/rendering issues.
