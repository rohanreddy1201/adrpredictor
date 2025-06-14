import shap
import pandas as pd
import joblib

MODEL_PATH = "app/model/model.pkl"

def explain_prediction(drug_name: str, sex: str, indication: str):
    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame([{
        "drug_name": drug_name.upper(),
        "sex": sex.upper(),
        "indication": indication.upper()
    }])

    preprocessor = model.named_steps["pre"]
    clf = model.named_steps["clf"]

    # Transform and convert to dense format
    X_transformed = preprocessor.transform(input_df)
    if hasattr(X_transformed, "toarray"):
        X_transformed = X_transformed.toarray()

    # Get proper feature names from the OneHotEncoder
    ohe = preprocessor.named_transformers_['cat']
    feature_names = ohe.get_feature_names_out(["drug_name", "sex", "indication"])

    # Build SHAP explainer
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_transformed, check_additivity=False)

    return shap_values, explainer, X_transformed, feature_names
