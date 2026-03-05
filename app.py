import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load dataset of destinations
@st.cache_data
def load_data():
    return pd.read_csv("tourism_dataset_clean_streamlit.csv")

df = load_data()

st.set_page_config(page_title="Cultural Tourism Platform", layout="wide")

# Create tabs layout (no video tab)
tab1, tab2, tab3, tab4 = st.tabs(["Traveler Info", "Recommendations", "Itinerary", "Chatbot"])

# --- Traveler Info Tab ---
with tab1:
    st.header("Traveler Information")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    interests = st.multiselect(
        "Select your interests:",
        ["Culture", "Nature", "Art & Architecture", "History", "Beaches", "Nightlife", "Cuisine", "Wellness"]
    )
    budget = st.number_input("Budget (USD)", min_value=0, value=5000)

# Placeholder for recommendations
recommended = None

# --- Recommendations Tab ---
with tab2:
    st.header("Destination Recommendations")
    if interests:
        # Choose category based on interests (simple logic)
        category = "nature" if "Nature" in interests else "culture"
        # Filter by budget
        candidates = df[df['avg_cost_usd'] <= budget] if budget else df
        # Sort by category score and take top 3
        recommended = candidates.sort_values(by=category, ascending=False).head(3)
        if not recommended.empty:
            st.subheader("Based on your interests, we recommend:")
            for _, row in recommended.iterrows():
                st.write(f"- **{row['Site Name']}** ({row['city']}, {row['country']}) – Score: {row['overall_experience_score']}")
        else:
            st.write("No destinations found matching your criteria.")
    else:
        st.write("Please select at least one interest to get recommendations.")

# --- Itinerary Tab ---
with tab3:
    st.header("Itinerary")
    if recommended is not None and not recommended.empty:
        st.subheader("Your trip itinerary:")
        for i, (_, row) in enumerate(recommended.iterrows(), start=1):
            st.write(f"Day {i}: Visit **{row['Site Name']}** in {row['city']}, {row['country']} (Rating: {row['overall_experience_score']})")
        # Generate PDF with PyFPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for i, (_, row) in enumerate(recommended.iterrows(), start=1):
            text = f"Day {i}: Visit {row['Site Name']} in {row['city']}, {row['country']}."
            pdf.cell(0, 10, txt=text, ln=1)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')  # use dest='S' for bytes:contentReference[oaicite:10]{index=10}
        st.download_button(
            label="Download Itinerary (PDF)",
            data=pdf_bytes,
            file_name="itinerary.pdf",
            mime="application/pdf"
        )
    else:
        st.write("Generate recommendations first to see the itinerary.")

# --- Chatbot Tab ---
with tab4:
    st.header("Multilingual Chatbot")
    st.write("Enter a message and select a language for a placeholder response.")
    lang = st.selectbox("Language", ["English", "Spanish", "French", "German", "Italian"])
    user_msg = st.chat_input("Your message:")
    if user_msg:
        with st.chat_message("user"):
            st.write(user_msg)
        # Placeholder response: echo user message with language note
        response = f"[In {lang}] Echo: {user_msg}"
        with st.chat_message("assistant"):
            st.write(response)  # This uses st.chat_input and st.chat_message as in docs:contentReference[oaicite:11]{index=11}
