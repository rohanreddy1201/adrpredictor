import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def train_and_save_model(csv_path: str, model_path: str = "app/model/model.pkl"):
    df = pd.read_csv(csv_path)

    # Clean and preprocess
    df = df[df["sex"].isin([1, 2])]
    df = df.dropna(subset=["drug_name", "indication", "reaction", "route", "dosage_form"])

    # Convert age to numeric
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age"] = df["age"].where(df["age_unit"] == 801)  # Only keep age in years
    df = df.dropna(subset=["age"])

    # Select features
    X = df[["drug_name", "sex", "age", "indication", "route", "dosage_form"]]
    y = df["serious"]

    # Define column types
    categorical = ["drug_name", "indication", "route", "dosage_form"]
    numerical = ["age", "sex"]

    # Preprocessing
    preprocessor = ColumnTransformer(transformers=[
        ("num", StandardScaler(), numerical),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])

    # Pipeline
    pipeline = Pipeline([
        ("pre", preprocessor),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    # Save
    joblib.dump(pipeline, model_path)
    print(f"✅ Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model("app/data/flattened_faers.csv")
