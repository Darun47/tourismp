import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from fpdf import FPDF

st.set_page_config(page_title="AI Cultural Tourism Platform", layout="wide")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("tourism_dataset_clean_streamlit.csv")
    return df

df = load_data()

st.title("🌍 AI Cultural Tourism Insights Platform")

# -----------------------------
# Traveler Input
# -----------------------------
st.sidebar.header("Traveler Preferences")

interest = st.sidebar.selectbox(
    "Select Travel Interest",
    ["culture", "adventure", "nature", "beaches"]
)

season = st.sidebar.selectbox(
    "Preferred Season",
    df["Best Season"].dropna().unique()
)

budget = st.sidebar.selectbox(
    "Budget Level",
    df["budget_level"].dropna().unique()
)

duration = st.sidebar.slider("Trip Duration (Days)", 1, 7, 3)

# -----------------------------
# Recommendation Engine
# -----------------------------
filtered = df[
    (df["Best Season"] == season) &
    (df["budget_level"] == budget)
]

filtered = filtered.sort_values(by=[interest, "Tourist Rating"], ascending=False)

recommendations = filtered.head(duration)

# -----------------------------
# Display Recommendations
# -----------------------------
st.header("Recommended Destinations")

for _, row in recommendations.iterrows():

    st.subheader(f"{row['Site Name']} — {row['city']}, {row['country']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Experience Type:", row["Type"])
        st.write("Tourist Rating:", row["Tourist Rating"])
        st.write("Best Season:", row["Best Season"])

    with col2:
        st.write("Budget Level:", row["budget_level"])
        st.write("Average Cost:", row["avg_cost_usd"], "USD")
        st.write("Climate:", row["climate_classification"])

# -----------------------------
# Map Visualization
# -----------------------------
st.header("Destination Map")

# create base map
m = folium.Map(location=[20,0], zoom_start=2)

for _, row in recommendations.iterrows():

    # simple random location fallback if lat/long not available
    lat = row.get("latitude", None)
    lon = row.get("longitude", None)

    if pd.notna(lat) and pd.notna(lon):

        folium.Marker(
            [lat, lon],
            tooltip=row["Site Name"],
            popup=row["city"]
        ).add_to(m)

st_folium(m, width=700)

# -----------------------------
# Itinerary Generator
# -----------------------------
st.header("Generated Travel Itinerary")

itinerary_text = []

for i, (_, row) in enumerate(recommendations.iterrows()):

    day_plan = f"Day {i+1}: Visit {row['Site Name']} in {row['city']}, {row['country']}"

    st.write(day_plan)

    itinerary_text.append(day_plan)

# -----------------------------
# PDF Generator
# -----------------------------
def create_pdf(text_list):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,txt="AI Generated Travel Itinerary",ln=True)

    for line in text_list:
        pdf.cell(200,10,txt=line,ln=True)

    return pdf.output(dest="S").encode("latin-1")

st.header("Download Itinerary")

if st.button("Generate PDF"):

    pdf_data = create_pdf(itinerary_text)

    st.download_button(
        label="Download Itinerary PDF",
        data=pdf_data,
        file_name="travel_itinerary.pdf",
        mime="application/pdf"
    )
