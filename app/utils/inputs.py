import streamlit as st
import pandas as pd

def load_unique_values():
    df = pd.read_csv("app/data/flattened_faers.csv")
    return {
        "drug_names": sorted(df["drug_name"].dropna().unique().tolist()),
        "indications": sorted(df["indication"].dropna().unique().tolist()),
        "routes": sorted(df["route"].dropna().unique().tolist()),
        "dosage_forms": sorted(df["dosage_form"].dropna().unique().tolist()),
    }

def get_user_input():
    options = load_unique_values()

    drug_name = st.selectbox("Drug Name", options["drug_names"])
    indication = st.selectbox("Indication", options["indications"])
    route = st.selectbox("Route of Administration", options["routes"])
    dosage_form = st.selectbox("Dosage Form", options["dosage_forms"])

    sex = st.radio("Sex", ["1 - Male", "2 - Female"])
    sex = sex.split(" ")[0]  # Just the number

    age = st.slider("Age", min_value=0, max_value=120, value=50)

    return drug_name, sex, age, indication, route, dosage_form
