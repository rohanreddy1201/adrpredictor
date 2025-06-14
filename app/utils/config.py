import pandas as pd

DATA_PATH = "app/data/flattened_faers.csv"

def load_unique_values():
    df = pd.read_csv(DATA_PATH)
    drugs = sorted(df["drug_name"].dropna().unique().tolist())
    indications = sorted(df["indication"].dropna().unique().tolist())
    return drugs, indications
