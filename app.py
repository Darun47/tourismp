import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from moviepy.editor import TextClip, concatenate_videoclips
import tempfile

st.set_page_config(page_title="AI Cultural Tourism Platform", layout="wide")

# ----------------------------
# LOAD DATA
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("tourism_dataset_clean_streamlit.csv")
    return df

df = load_data()

# ----------------------------
# SIDEBAR INPUT
# ----------------------------

st.sidebar.header("Traveler Preferences")

age = st.sidebar.slider("Age", 10, 80, 25)

interest = st.sidebar.selectbox(
    "Interest",
    ["culture", "adventure", "nature", "beaches", "nightlife", "cuisine"]
)

season = st.sidebar.selectbox(
    "Preferred Season",
    df["Best Season"].dropna().unique()
)

budget = st.sidebar.selectbox(
    "Budget Level",
    df["budget_level"].dropna().unique()
)

duration = st.sidebar.slider("Trip Duration (days)", 1, 10, 3)

# ----------------------------
# RECOMMENDATION ENGINE
# ----------------------------

def recommend_destinations():

    filtered = df[
        (df["Best Season"] == season) &
        (df["budget_level"] == budget)
    ]

    filtered = filtered.sort_values(
        by=[interest, "Tourist Rating"],
        ascending=False
    )

    return filtered.head(5)


# ----------------------------
# ITINERARY GENERATOR
# ----------------------------

def generate_itinerary(destinations):

    itinerary = []

    for i in range(min(duration, len(destinations))):

        row = destinations.iloc[i]

        day_plan = {
            "Day": i+1,
            "City": row["city"],
            "Country": row["country"],
            "Site": row["Site Name"],
            "Type": row["Type"],
            "Season": row["Best Season"]
        }

        itinerary.append(day_plan)

    return itinerary


# ----------------------------
# PDF GENERATOR
# ----------------------------

def create_pdf(itinerary):

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Generated Travel Itinerary", styles["Title"]))
    story.append(Spacer(1, 20))

    for day in itinerary:

        text = f"""
        Day {day['Day']} - {day['City']}, {day['Country']} <br/>
        Visit: {day['Site']} <br/>
        Experience: {day['Type']} <br/>
        Best Season: {day['Season']}
        """

        story.append(Paragraph(text, styles["Normal"]))
        story.append(Spacer(1, 12))

    pdf = SimpleDocTemplate(file.name)
    pdf.build(story)

    return file.name


# ----------------------------
# VIDEO GENERATOR
# ----------------------------

def generate_video(itinerary):

    clips = []

    for day in itinerary:

        text = f"Day {day['Day']} - {day['City']}"

        clip = TextClip(text, fontsize=70, color='white', size=(1280,720))
        clip = clip.set_duration(2)

        clips.append(clip)

    video = concatenate_videoclips(clips)

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    video.write_videofile(file.name, fps=24)

    return file.name


# ----------------------------
# TABS LAYOUT
# ----------------------------

tabs = st.tabs([
    "Home",
    "Itinerary Generator",
    "Smart Recommendations",
    "PDF Backup",
    "Return Trip Video",
    "Chatbot"
])

# ----------------------------
# HOME
# ----------------------------

with tabs[0]:

    st.title("🌍 AI Cultural Tourism Insights Platform")

    st.write("""
    This AI platform generates personalized travel itineraries
    based on traveler preferences, budget, season and interests.
    """)

# ----------------------------
# RECOMMENDATIONS
# ----------------------------

with tabs[2]:

    st.header("Smart Destination Recommendations")

    destinations = recommend_destinations()

    for _, row in destinations.iterrows():

        st.subheader(row["city"] + ", " + row["country"])

        col1, col2 = st.columns(2)

        with col1:

            st.write("Site:", row["Site Name"])
            st.write("Experience:", row["Type"])
            st.write("Rating:", row["Tourist Rating"])

        with col2:

            st.write("Budget:", row["budget_level"])
            st.write("Season:", row["Best Season"])
            st.write("Cost (USD):", row["avg_cost_usd"])

# ----------------------------
# ITINERARY
# ----------------------------

with tabs[1]:

    st.header("Personalized Itinerary")

    destinations = recommend_destinations()

    itinerary = generate_itinerary(destinations)

    for day in itinerary:

        st.card = st.container()

        with st.card:

            st.subheader(f"Day {day['Day']}")

            st.write("City:", day["City"])
            st.write("Site:", day["Site"])
            st.write("Experience:", day["Type"])

# ----------------------------
# PDF DOWNLOAD
# ----------------------------

with tabs[3]:

    st.header("Download Itinerary PDF")

    destinations = recommend_destinations()

    itinerary = generate_itinerary(destinations)

    if st.button("Generate PDF"):

        pdf_file = create_pdf(itinerary)

        with open(pdf_file, "rb") as f:

            st.download_button(
                "Download PDF",
                f,
                file_name="travel_itinerary.pdf"
            )

# ----------------------------
# VIDEO
# ----------------------------

with tabs[4]:

    st.header("Return Trip Video")

    destinations = recommend_destinations()

    itinerary = generate_itinerary(destinations)

    if st.button("Generate Video"):

        video_file = generate_video(itinerary)

        st.video(video_file)

# ----------------------------
# CHATBOT
# ----------------------------

with tabs[5]:

    st.header("Travel Assistant Chatbot")

    user_question = st.text_input("Ask about destinations")

    if user_question:

        st.write("AI Response:")

        st.write(
            "Based on your interests, I recommend visiting cultural "
            "sites in Paris, Kyoto, and Rome during spring."
        )
