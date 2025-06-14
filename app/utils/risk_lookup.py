import requests

def generate_explanation(drug_name, age, sex, indication, route, dosage_form, model="mistral"):
    sex_str = "male" if str(sex) == "1" else "female"

    prompt = f"""
You are a clinical AI assistant. Explain the possible adverse drug reaction (ADR) risks for the following patient:

- Drug: {drug_name}
- Indication: {indication}
- Age: {age}
- Sex: {sex_str}
- Route: {route}
- Dosage form: {dosage_form}

Give a short, 2–3 sentence explanation of potential ADR risks based on known drug patterns, patient factors, and route of administration.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"⚠️ Ollama explanation failed: {str(e)}"
