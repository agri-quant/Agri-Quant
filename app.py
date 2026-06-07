import streamlit as st
import os
import datetime
import re
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. UI SETUP & EXECUTIVE THEMING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agri-Quant Elite | Geospatial AI Intelligence",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size:28px; color:#1a365d; font-weight:700; margin-bottom:5px; }
    .sub-header { font-size:16px; color:#4a5568; margin-bottom:20px; }
    .section-card { background-color:#f7fafc; padding:15px; border-left:4px solid #1a365d; border-radius:4px; margin-bottom:15px; }
    .mode-badge { background-color:#ebf8ff; color:#2b6cb0; padding:6px 12px; border-radius:4px; font-size:13px; font-weight:bold; display:inline-block; }
    .fallback-badge { background-color:#fffaf0; color:#dd6b20; padding:6px 12px; border-radius:4px; font-size:13px; font-weight:bold; display:inline-block; }
    .geo-alert { background-color:#e6fffa; border-left:4px solid #319795; padding:10px; border-radius:4px; margin-bottom:15px; font-size:13px; color:#234e52; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌾 Agri-Quant Elite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Universal Dynamic AI Agribusiness Quantity Surveying & Spatial Planning Architecture</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. API KEY ROUTING (Sidebar Credentials Entry)
# -----------------------------------------------------------------------------
st.sidebar.header("🔑 Authentication")

# Try to look for background secret first
bg_api_key = os.getenv("GEMINI_API_KEY")

# Provide an on-screen fallback input field so you can paste it directly if the background fails
user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key", 
    value=bg_api_key if bg_api_key else "",
    type="password",
    help="Paste your AI Studio API key here to activate articulate AI models instantly."
)

# Set final key selector
final_api_key = user_api_key if user_api_key else bg_api_key

client = None
if final_api_key:
    try:
        client = genai.Client(api_key=final_api_key)
    except Exception:
        client = None

# Status Banner Display
if client:
    st.markdown('<span class="mode-badge">⚡ LIVE COGNITIVE AI ACTIVE (FULL DETAILED ANALYSIS)</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="fallback-badge">📊 LOCAL SIMULATION BACKUP ACTIVE (PASTE API KEY IN SIDEBAR FOR LIVE AI)</span>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GLOBAL INPUT PARAMETERS
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Universal Project Config")
crop_type = st.sidebar.text_input("Enter Crop Name", value="Cassava")
land_size_input = st.sidebar.text_input("Preferable Land Size / Scale", value="2.5 Hectares")
location_input = st.sidebar.text_input("Project Location or GPS Coordinates", value="Minna, Niger State")
planting_date = st.sidebar.date_input("Target Planting Start Date", value=datetime.date(2026, 6, 15))

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

# Coordinate Parsing Detection
coord_pattern = r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)"
is_coordinate = bool(re.match(coord_pattern, location_input.strip()))

if is_coordinate:
    st.markdown(f'<div class="geo-alert">🎯 **Geospatial Anchor Confirmed:** Coordinates `[{location_input.strip()}]` mapped for a scope of **{land_size_input}**.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="geo-alert">📍 **Regional Mode Active:** Mapped to regional zone `{location_input}` for a scope of **{land_size_input}**.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Precise Costing (BOQ)", "📅 Lifecycle Planner", "📊 Comparative Matrix"])

# -----------------------------------------------------------------------------
# FEATURE 1: LAND PREP COSTING (BOQ)
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f'<div class="section-card"><h3>Dynamic CapEx Estimator: {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Quantify {crop_type} Infrastructure", key="btn_tab1"):
        with st.spinner(f"Processing calculations..."):
            if client:
                try:
                    f1_prompt = f"""
                    You are an expert Agricultural Quantity Surveyor and Civil Engineer.
                    Generate a highly articulate, institutional-grade Land Preparation Bill of Quantities (BOQ).
                    
                    PARAMETERS:
                    - Crop Target: {crop_type}
                    - Scale: {land_size_input}
                    - Location: {location_input}
                    
                    OUTPUT STRUCTURE:
                    Provide a highly detailed analysis containing an Executive Summary, an Itemized Cost Estimation Table in Nigerian Naira (NGN), Operational Logistics constraints, and professional recommendations. Make it thoroughly articulated and structured.
                    """
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f1_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"API Connection Exception: {e}. Please check your sidebar API Key string.")
            else:
                st.warning("⚠️ Live AI Engine offline. Please provide a valid Gemini API Key in the sidebar input box to unlock full articulate calculations.")

# -----------------------------------------------------------------------------
# FEATURE 2: LIFECYCLE PLANNER
# -----------------------------------------------------------------------------
with tab2:
    st.markdown(f'<div class="section-card"><h3>Automated Timeline for {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Generate {crop_type} Critical Path", key="btn_tab2"):
        with st.spinner("Processing biological milestones..."):
            if client:
                try:
                    f2_prompt = f"Provide a deeply detailed, month-by-month growth, climate mitigation, and logistical supply chain timeline for cultivating {crop_type} starting on {planting_date} at location target {location_input} scaled to {land_size_input}."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f2_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"API Connection Exception: {e}")
            else:
                st.warning("⚠️ Live AI Engine offline. Please provide a valid Gemini API Key in the sidebar input box.")

# -----------------------------------------------------------------------------
# FEATURE 3: COMPARATIVE MATRIX
# -----------------------------------------------------------------------------
with tab3:
    comparison_target = st.text_input("Enter Comparison Crop (Default: Millet)", value="Millet")
    if st.button(f"Compare {crop_type} vs {comparison_target}", key="btn_tab3"):
        with st.spinner("Executing complex financial variance comparative modeling..."):
            if client:
                try:
                    f3_prompt = f"Act as an Agricultural Investment Consultant. Compare the granular ROI, upfront CapEx demands, and labor overhead parameters of {crop_type} vs {comparison_target} for a layout scale of {land_size_input} mapped to geographic zone {location_input}."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f3_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"API Connection Exception: {e}")
            else:
                st.warning("⚠️ Live AI Engine offline. Please provide a valid Gemini API Key in the sidebar input box.")