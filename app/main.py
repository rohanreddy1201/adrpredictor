import streamlit as st
from utils.inputs import get_user_input
from model.predict import load_model, make_prediction
from utils.risk_lookup import generate_explanation

st.set_page_config(page_title="ADRPredictor+", layout="centered")

st.title("🧠 ADRPredictor+")
st.markdown("Predict serious Adverse Drug Reactions (ADRs) based on drug + patient profile.")

# Load model
model = load_model()

# Collect input from user
drug_name, sex, age, indication, route, dosage_form = get_user_input()

# Predict button
if st.button("Predict ADR Risk"):
    with st.spinner("Running prediction..."):
        probability = make_prediction(model, drug_name, sex, age, indication, route, dosage_form)
        st.success(f"**Predicted Serious ADR Risk: {probability * 100:.1f}%**")

        if probability > 0.7:
            st.warning("⚠️ High ADR risk predicted.")
        elif probability > 0.4:
            st.info("⚠️ Moderate risk.")
        else:
            st.success("✅ Low risk predicted.")

        # Show input summary
        st.subheader("📋 Patient & Drug Context")
        st.markdown(f"""
        - **Drug:** {drug_name.title()}
        - **Indication:** {indication.title()}
        - **Age:** {int(age)}  
        - **Sex:** {"Male" if sex == "1" else "Female"}
        - **Route:** {route.title()}
        - **Form:** {dosage_form.title()}
        """)

        # Get explanation from Ollama
        st.subheader("🧠 Explanation (via Ollama)")
        with st.spinner("Consulting clinical assistant..."):
            explanation = generate_explanation(
                drug_name, age, sex, indication, route, dosage_form
            )
            st.markdown(f"**{explanation}**")
