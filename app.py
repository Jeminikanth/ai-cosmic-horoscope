import streamlit as st
import openai
from datetime import datetime

# --- PAGE CONFIGURATION & MOBILE COMPATIBLE DESIGN ---
st.set_page_config(
    page_title="AI Cosmic Horoscope",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for vibrant positive colors, large mobile-friendly fonts, and polished containers
st.markdown("""
    <style>
    /* Gradient Background and vibrant energy */
    .stApp {
        background: linear-gradient(135deg, #1e0b36 0%, #3a1c71 50%, #d76d77 100%);
        color: #ffffff;
    }
    
    /* Global Mobile-Friendly Large Typography */
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #f8f9fa !important;
    }
    
    /* Custom Stylized Inputs */
    input, select, .stDateInput div {
        font-size: 18px !important;
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ffafbd !important;
    }
    
    /* Big Entry Header Style */
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
    
    /* Horoscope Output Box Wrapper */
    .horoscope-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #ffafbd;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
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
    
    /* Footnote styling */
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

# --- APP INTERFACE ---
st.markdown('<div class="entry-header">✨ Discover Your Celestial Path ✨</div>', unsafe_allow_html=True)

# Secure API Key configuration from Streamlit Secrets Management
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.warning("Please configure your OPENAI_API_KEY in the Streamlit deployment settings.")

# User Entry Fields with prominent layout
first_name = st.text_input("Enter First Name:")
second_name = st.text_input("Enter Second Name:")
dob = st.date_input("Date of Birth:", min_value=datetime(1920, 1, 1))
gender = st.selectbox("Gender:", ["Select", "Male", "Female", "Non-binary", "Prefer not to say"])

# Generate Analysis Trigger
if st.button("✨ Reveal My AI Horoscope Analysis ✨", use_container_width=True):
    if first_name.strip() == "" or gender == "Select":
        st.error("Please provide at least your First Name and select a Gender to align the stars.")
    else:
        with st.spinner("Consulting AI celestial patterns..."):
            # Framing prompt instructions for the AI Agent
            prompt = f"""
            Act as an expert, highly advanced, positive AI Vedic and Western Astrologer.
            Generate a personalized horoscope analysis for:
            Name: {first_name} {second_name}
            DOB: {dob.strftime('%B %d, %Y')}
            Gender: {gender}
            
            Provide the output structured exactly with these four elements:
            1. Good days for you: (List specific upcoming favorable days or day types with reasons)
            2. Lucky color: (Suggest a strong vibrant color based on cosmic alignments)
            3. Lucky numbers: (Provide lucky digits or compound numbers)
            4. Habits to avoid & Best AI Suggestion: (Construct constructive advice on habits to break alongside a motivating AI growth strategy)
            
            Keep the tone deeply uplifting, insightful, and vibrant. Do not use markdown titles or headers in your response text; just plain lines or bullet points.
            """
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an uplifting AI Astrologer providing constructive, beautiful, and inspiring horoscope insights."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600,
                    temperature=0.7
                )
                
                ai_result = response.choices[0].message['content']
                
                # Render results inside custom styled responsive box container
                st.markdown(f"""
                <div class="horoscope-box">
                    <div class="horoscope-title">🔮 Your Horoscope for {first_name} {second_name}</div>
                    <div style="font-size: 18px; line-height: 1.6; color: #ffffff; white-space: pre-wrap;">{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Balloons to celebrate positive energy output
                st.balloons()
                
            except Exception as e:
                st.error("The cosmic signals encountered an error. Please verify your API key configuration setup.")

# --- COMPULSORY CELESTIAL FOOTNOTE ---
st.markdown('---')
st.markdown('<div class="footnote">"Final Destination is up to GOD. Wish you all the happiness in Life"</div>', unsafe_allow_html=True)
