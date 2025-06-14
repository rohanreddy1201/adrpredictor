import json
import pandas as pd
from zipfile import ZipFile

def load_faers_from_zip(zip_path: str, json_filename: str, max_records: int = 5000) -> pd.DataFrame:
    with ZipFile(zip_path, 'r') as zip_file:
        with zip_file.open(json_filename) as json_file:
            data = json.load(json_file)

    records = data.get("results", [])[:max_records]
    parsed = []

    for entry in records:
        try:
            patient = entry.get("patient", {})
            drugs = patient.get("drug", [])
            reactions = patient.get("reaction", [])

            # Use the first drug only for now
            if not drugs:
                continue

            drug = drugs[0]
            openfda = drug.get("openfda", {})

            parsed.append({
                "drug_name": drug.get("medicinalproduct", "").upper(),
                "sex": patient.get("patientsex", ""),
                "age": patient.get("patientonsetage", ""),
                "age_unit": patient.get("patientonsetageunit", ""),
                "indication": drug.get("drugindication", "").upper(),
                "route": openfda.get("route", [None])[0],
                "dosage_form": drug.get("drugdosageform", ""),
                "reaction": reactions[0].get("reactionmeddrapt", "").upper() if reactions else "",
                "serious": int(entry.get("serious", 0))
            })

        except Exception as e:
            print("⚠️ Skipped record due to error:", e)

    return pd.DataFrame(parsed)

def save_rich_csv(zip_path: str, json_filename: str, output_csv: str):
    df = load_faers_from_zip(zip_path, json_filename)
    df = df.dropna(subset=["drug_name", "sex", "reaction"])
    df = df[df["sex"].isin(["1", "2"])]
    df = df.head(5000)  # Sample size
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved enhanced dataset to {output_csv} with shape: {df.shape}")

if __name__ == "__main__":
    zip_path = "app/data/drug-event-0028-of-0034.json.zip"
    json_filename = "drug-event-0028-of-0034.json"
    output_csv = "app/data/flattened_faers.csv"
    save_rich_csv(zip_path, json_filename, output_csv)
