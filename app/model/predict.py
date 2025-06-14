import joblib
import pandas as pd

MODEL_PATH = "app/model/model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def make_prediction(model, drug_name, sex, age, indication, route, dosage_form):
    input_df = pd.DataFrame([{
        "drug_name": drug_name.upper(),
        "sex": int(sex),
        "age": float(age),
        "indication": indication.upper(),
        "route": route.upper(),
        "dosage_form": dosage_form.upper()
    }])
    return model.predict_proba(input_df)[0][1]  # Return probability of serious ADR
