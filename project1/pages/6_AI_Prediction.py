import streamlit as st
import pandas as pd
from utils.common import v5_hyper_css, back_to_home_button, back_to_home_button, page_loader, brand_header, animated_download_button, animated_button, setup_page, hero, load_data, empty_guard, run_visible_steps, animated_success, shimmer_loading
setup_page("AI Prediction")
v5_hyper_css()
page_loader("Opening 6 AI Prediction")
brand_header()
hero("AI Delay Prediction Results", "Expected result page: train model only on demand for maximum speed, then predict delay risk for selected route scenario.")
back_to_home_button()
df = load_data(); empty_guard(df)

@st.cache_resource(show_spinner=False)
def train_model(sample_n=3500):
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    use = df[["Factory","Region","State/Province","Ship Mode","Division","Sales","Units","Profit Margin","Delayed"]].dropna().copy()
    if len(use) > sample_n:
        use = use.sample(sample_n, random_state=42)
    X = use.drop(columns=["Delayed"]); y = use["Delayed"].astype(int)
    cat = ["Factory","Region","State/Province","Ship Mode","Division"]
    num = ["Sales","Units","Profit Margin"]
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cat), ("num", "passthrough", num)])
    clf = Pipeline([("prep", prep), ("model", RandomForestClassifier(n_estimators=35, max_depth=8, random_state=42, n_jobs=-1, class_weight="balanced"))])
    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=.2,random_state=42,stratify=y if y.nunique()>1 else None)
    clf.fit(Xtr,ytr)
    acc = accuracy_score(yte, clf.predict(Xte))
    return clf, acc

if "ai_trained" not in st.session_state: st.session_state.ai_trained = False
if animated_button(
    "Train AI model now",
    key="train_ai_model",
    steps=[
        ("Preparing Training Data", "Cleaning and preparing ML features."),
        ("Encoding Features", "Transforming categorical route data."),
        ("Training Random Forest", "Learning delay-risk shipment patterns."),
        ("Validating Model", "Calculating AI prediction accuracy.")
    ],
    success_message="AI model trained successfully"
):
    run_visible_steps([
        ("Preparing Training Data", "Selected factory, region, state, ship mode, division, sales, units, and profit margin."),
        ("Encoding Categories", "Converted route and product attributes into ML-ready features."),
        ("Training Random Forest", "Optimized model is learning delay patterns from the dataset."),
        ("Validating Model", "Accuracy score calculated using a test split.")
    ])
    with st.spinner("Finalizing optimized model..."):
        st.session_state.model, st.session_state.acc = train_model()
        st.session_state.ai_trained = True
    animated_success("AI model trained successfully", "Prediction controls are now available below.")

if not st.session_state.ai_trained:
    st.warning("Model is not trained yet. Click the button above. This keeps app loading super fast.")
    st.stop()

st.success(f"Model ready. Validation accuracy: {st.session_state.acc*100:.1f}%")

c1,c2,c3 = st.columns(3)
factory = c1.selectbox("Factory", sorted(df["Factory"].unique()))
region = c2.selectbox("Region", sorted(df["Region"].unique()))
mode = c3.selectbox("Ship Mode", sorted(df["Ship Mode"].unique()))
c4,c5,c6 = st.columns(3)
state = c4.selectbox("State", sorted(df["State/Province"].unique()))
division = c5.selectbox("Division", sorted(df["Division"].unique()))
units = c6.number_input("Units", min_value=1, max_value=1000, value=int(df["Units"].median()))
sales = st.number_input("Sales", min_value=0.0, value=float(df["Sales"].median()))
pm = float(df["Profit Margin"].median())
scenario = pd.DataFrame([{"Factory":factory,"Region":region,"State/Province":state,"Ship Mode":mode,"Division":division,"Sales":sales,"Units":units,"Profit Margin":pm}])
if animated_button(
    "Predict Delay Risk",
    key="predict_delay_risk",
    steps=[
        ("Reading Scenario", "Collecting shipment prediction parameters."),
        ("Running AI Prediction", "Processing shipment through ML pipeline."),
        ("Calculating Risk", "Generating final delivery risk probability.")
    ],
    success_message="Delay prediction generated"
):
    run_visible_steps([
        ("Reading Scenario", "Factory, destination state, region, ship mode, units, and sales captured."),
        ("Running ML Prediction", "Scenario passed through the trained delay prediction pipeline."),
        ("Calculating Risk Level", "Delay probability converted into Low, Medium, or High risk.")
    ])
    clf = st.session_state.model
    pred = int(clf.predict(scenario)[0])
    if hasattr(clf.named_steps["model"], "predict_proba"):
        probs = clf.predict_proba(scenario)[0]
        classes = list(clf.named_steps["model"].classes_)
        proba = float(probs[classes.index(1)]) if 1 in classes else 0.0
    else:
        proba = float(pred)
    risk = "High Risk" if proba >= .65 else "Medium Risk" if proba >= .35 else "Low Risk"
    st.metric("Predicted Delay Risk", risk, f"{proba*100:.1f}% probability")
