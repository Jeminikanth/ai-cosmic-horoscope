import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- PAGE CONFIGURATION & MOBILE COMPATIBLE DESIGN ---
st.set_page_config(
    page_title="AI Sky Horoscope",
    page_icon="☁️",
    layout="centered"
)

# Custom CSS for Sky Blue background, CSS cloud graphics, and Dark Grey text formatting
st.markdown("""
    <style>
    /* Sky Blue Background representing a clear, bright atmosphere */
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #B0E0E6 100%);
        color: #333333 !important;
    }
    
    /* Force all standard text, headers, and form labels to Dark Grey */
    html, body, [data-testid="stWidgetLabel"] p, .stMarkdown, p, span {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #333333 !important;
    }
    
    /* Clean inputs styled to match the airy environment */
    input, select, .stDateInput div {
        font-size: 18px !important;
        background-color: rgba(255, 255, 255, 0.6) !important;
        color: #333333 !important;
        border-radius: 10px !important;
        border: 1px solid #4A90E2 !important;
    }
    
    /* Main App Header */
    .entry-header {
        font-size: 34px;
        font-weight: bold;
        text-align: center;
        color: #2C3E50 !important;
        margin-bottom: 5px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }
    
    /* --- CSS CLOUD GRAPHICS LAYOUT --- */
    .cloud-container {
        position: relative;
        height: 60px;
        width: 100%;
        overflow: hidden;
        margin-bottom: 25px;
    }
    .cloud {
        background: #ffffff;
        background: linear-gradient(top, #ffffff 5%, #f1f1f1 100%);
        border-radius: 100px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        position: absolute;
        margin: auto;
        left: 0; right: 0;
    }
    .cloud:after, .cloud:before {
        background: #ffffff;
        content: '';
        position: absolute;
        zIndex: -1;
    }
    .cloud { width: 120px; height: 40px; top: 10px; }
    .cloud:after { width: 40px; height: 40px; top: -20px; left: 15px; border-radius: 40px; }
    .cloud:before { width: 60px; height: 60px; top: -30px; right: 15px; border-radius: 60px; }
    
    /* Horoscope Output Box (Styled like a large distinct cloud panel) */
    .horoscope-box {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 25px;
        border: 2px solid #ffffff;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        margin-top: 30px;
    }
    
    .horoscope-title {
        font-size: 26px !important;
        color: #2C3E50 !important;
        font-weight: bold;
        text-align: center;
        border-bottom: 2px solid #87CEEB;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    /* Output text explicitly formatted in Dark Grey */
    .horoscope-content {
        font-size: 18px; 
        line-height: 1.6; 
        color: #333333 !important; 
        white-space: pre-wrap;
        font-weight: 500;
    }
    
    /* Footnote display alignment */
    .footnote {
        text-align: center;
        font-size: 16px !important;
        font-style: italic;
        color: #4A5568 !important;
        margin-top: 40px;
        padding: 10px;
    }
    
    /* Style custom submit button */
    .stButton>button {
        background-color: #4A90E2 !important;
        color: white !important;
        font-size: 18px !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App Header and Cloud Graphic Section
st.markdown('<div class="entry-header">✨ Discover Your Celestial Path ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="cloud-container"><div class="cloud"></div></div>', unsafe_allow_html=True)

# Configure the Gemini API Key from Streamlit Secrets safely
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
        with st.spinner("Consulting free AI cloud patterns..."):
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
                # Updated directly to 'gemini-1.5-flash-002' to fix the 404 API version endpoint error
                model = genai.GenerativeModel('gemini-1.5-flash-002')
                response = model.generate_content(prompt)
                
                ai_result = response.text
                
                # Render results inside custom styled cloud-container panel using Dark Grey font
                st.markdown(f"""
                <div class="horoscope-box">
                    <div class="horoscope-title">🔮 Your Horoscope for {first_name} {second_name}</div>
                    <div class="horoscope-content">{ai_result}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"The signals encountered an error: {str(e)}")

# --- MANDATORY FOOTNOTE ---
st.markdown('---')
st.markdown('<div class="footnote">"Final Destination is up to GOD. Wish you all the happiness in Life"</div>', unsafe_allow_html=True)
