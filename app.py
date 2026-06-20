import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- PAGE CONFIGURATION & MOBILE COMPATIBLE DESIGN ---
st.set_page_config(
    page_title="AI Cosmic Horoscope",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for vibrant positive colors, large mobile-friendly fonts, and Yellow text output
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e0b36 0%, #3a1c71 50%, #d76d77 100%);
        color: #ffffff;
    }
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #f8f9fa !important;
    }
    input, select, .stDateInput div {
        font-size: 18px !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ffafbd !important;
    }
    .entry-header {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        background: -webkit-linear-gradient(#ffafbd, #ffc3a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .horoscope-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #ffafbd;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        margin-top: 30px;
    }
    .horoscope-title {
        font-size: 28px !important;
        color: #ffc3a0 !important;
        font-weight: bold;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    /* Set the dynamic horoscope AI content text to a bright Yellow color */
    .horoscope-content {
        font-size: 18px; 
        line-height: 1.6; 
        color: #ffff00 !important; 
        white-space: pre-wrap;
        font-weight: 500;
    }
    .footnote {
        text-align: center;
        font-size: 16px !important;
        font-style: italic;
        color: #e0e0e0;
        margin-top: 40px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="entry-header">✨ Discover Your Celestial Path ✨</div>', unsafe_allow_html=True)

# Configure the Gemini API Key from Streamlit Secrets
api_key_found = "GEMINI_API_KEY" in st.secrets
if api_key_found:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ Setup needed: Add your free GEMINI_API_KEY inside your Streamlit Cloud settings.")

# User Input Entry Fields
first_name = st.text_input("Enter First Name:")
second_name = st.text_input("Enter Second Name:")
dob = st.date_input("Date of Birth:", min_value=datetime(1920, 1, 1))
gender = st.selectbox("Gender:", ["Select", "Male", "Female", "Non-binary", "Prefer not to say"])

if st.button("✨ Reveal My AI Horoscope Analysis ✨", use_container_width=True):
    if not api_key_found:
        st.error("Cannot proceed: Missing GEMINI_API_KEY configuration.")
    elif first_name.strip() == "" or gender == "Select":
        st.error("Please provide at least your First Name and select a Gender.")
    else:
        with st.spinner("Consulting free AI cosmic patterns..."):
            prompt = f"""
            You are an uplifting AI Astrologer providing constructive, beautiful, and inspiring horoscope insights.
            Generate a personalized horoscope analysis for:
            Name: {first_name} {second_name}
            DOB: {dob.strftime('%B %d, %Y')}
            Gender: {gender}
            
            Provide the output structured exactly with these four elements:
            1. Good days for you: (List specific upcoming favorable days or day types with reasons)
            2. Lucky color: (Suggest a strong vibrant color based on cosmic alignments)
            3. Lucky numbers: (Provide lucky digits or compound numbers)
            4. Habits to avoid & Best AI Suggestion: (Construct constructive advice on habits to break alongside a motivating AI growth strategy)
            
            Keep the tone deeply uplifting, insightful, and vibrant. Do not use markdown titles or markdown headers (# or ##) in your response text.
            """
            
            try:
                # Call Gemini model
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                ai_result = response.text
                
                # Render results with the custom .horoscope-content class applied
                st.markdown(f"""
                <div class="horoscope-box">
                    <div class="horoscope-title">🔮 Your Horoscope for {first_name} {second_name}</div>
                    <div class="horoscope-content">{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"The cosmic signals encountered an error: {str(e)}")

# --- FOOTNOTE ---
st.markdown('---')
st.markdown('<div class="footnote">"Final Destination is up to GOD. Wish you all the happiness in Life"</div>', unsafe_allow_html=True)
