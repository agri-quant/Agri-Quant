import streamlit as st
import os
import datetime
import re
import google.generativeai as genai

# -----------------------------------------------------------------------------
# 1. APPLICATION VIEW INTERFACE CONFIGURATION
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
    .mode-badge { background-color:#e6fffa; color:#234e52; padding:6px 12px; border-radius:4px; font-size:13px; font-weight:bold; display:inline-block; }
    .geo-alert { background-color:#ebf8ff; border-left:4px solid #2b6cb0; padding:10px; border-radius:4px; margin-bottom:15px; font-size:13px; color:#2c5282; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌾 Agri-Quant Elite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Universal Dynamic AI Agribusiness Quantity Surveying & Spatial Planning Architecture</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MASTER PARAMETER INPUT CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.header("🔑 Authentication Setup")

# Interactive Sidebar Key Capture
user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key", 
    value=os.getenv("GEMINI_API_KEY", ""),
    type="password",
    help="Provide your target Google AI Studio developer token string here."
)

st.sidebar.header("📋 Universal Project Config")
crop_type = st.sidebar.text_input("Enter Crop Name", value="Cassava")
land_size_input = st.sidebar.text_input("Preferable Land Size / Scale", value="2.5 Hectares")
location_input = st.sidebar.text_input("Project Location or GPS Coordinates", value="Minna, Niger State")
planting_date = st.sidebar.date_input("Target Planting Start Date", value=datetime.date(2026, 6, 15))

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

# -----------------------------------------------------------------------------
# 3. GEOSPATIAL BOUNDS DETECTOR
# -----------------------------------------------------------------------------
coord_pattern = r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)"
is_coordinate = bool(re.match(coord_pattern, location_input.strip()))

if is_coordinate:
    st.markdown(f'<div class="geo-alert">🎯 **Geospatial Anchor Confirmed:** Coordinate points `[{location_input.strip()}]` calculated for a layout scale of **{land_size_input}**.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="geo-alert">📍 **Regional Mode Active:** Bound to macro environmental zone `{location_input}` for a layout scale of **{land_size_input}**.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Precise Costing (BOQ)", "📅 Lifecycle Planner", "📊 Comparative Matrix"])

# -----------------------------------------------------------------------------
# FEATURE 1: SECURE AI AGRI-QUANT SURVEYOR BOQ
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f'<div class="section-card"><h3>Dynamic CapEx Estimator: {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Quantify {crop_type} Infrastructure", key="btn_tab1"):
        if not user_api_key:
            st.error("🔑 Execution halted. Please input your Gemini API Key directly into the sidebar security module.")
        else:
            with st.spinner(f"Configuring institutional infrastructure analysis matrix for {crop_type}..."):
                try:
                    # Configure the pipeline connection securely
                    genai.configure(api_key=user_api_key.strip())
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    f1_prompt = f"""
                    You are a professional Agricultural Quantity Surveyor and Civil Engineer.
                    Task: Generate a highly articulate, institutional-grade Land Preparation Bill of Quantities (BOQ).
                    
                    Context Parameters:
                    - Farm Crop Target: {crop_type}
                    - Sizing Metrics: {land_size_input}
                    - Regional Spatial Context: {location_input}
                    
                    Output Layout:
                    Provide a thoroughly articulated breakdown including an Executive Summary, a clear Itemized Estimation Cost Table calculated in Nigerian Naira (NGN), operational transport barriers, and optimization guidelines. Make it exhaustive.
                    """
                    response = model.generate_content(f1_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}. Check that your API token is correctly copied from AI Studio without trailing breaks.")

# -----------------------------------------------------------------------------
# FEATURE 2: AUTOMATED EMBEDDED LIFECYCLE SCHEDULER
# -----------------------------------------------------------------------------
with tab2:
    st.markdown(f'<div class="section-card"><h3>Automated Timeline for {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Generate {crop_type} Critical Path", key="btn_tab2"):
        if not user_api_key:
            st.error("🔑 Execution halted. Please input your Gemini API Key into the sidebar context tracker.")
        else:
            with st.spinner("Processing seasonal environmental timelines..."):
                try:
                    genai.configure(api_key=user_api_key.strip())
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    f2_prompt = f"""
                    Provide an articulate, highly detailed month-by-month structural growth sequence, weather risk management plan, and harvesting logistics framework for a {crop_type} estate scaled at {land_size_input} situated at {location_input}. 
                    Base your initialization target point on the date: {planting_date}. Use clear headings and organized list patterns.
                    """
                    response = model.generate_content(f2_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

# -----------------------------------------------------------------------------
# FEATURE 3: FINANCIAL VARIANCE COMPARATIVE ENGINE
# -----------------------------------------------------------------------------
with tab3:
    st.markdown(f'<div class="section-card"><h3>Cross-Crop Comparative Matrix</h3></div>', unsafe_allow_html=True)
    comparison_target = st.text_input("Enter Comparison Crop (Default: Millet)", value="Millet")
    if st.button(f"Compare {crop_type} vs {comparison_target}", key="btn_tab3"):
        if not user_api_key:
            st.error("🔑 Execution halted. Verification token is missing from the sidebar module.")
        else:
            with st.spinner("Executing investment metrics asset comparison..."):
                try:
                    genai.configure(api_key=user_api_key.strip())
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    f3_prompt = f"""
                    Act as an executive Agribusiness Investment Consultant. 
                    Develop a comprehensive comparative risk-return assessment matrix evaluating {crop_type} against {comparison_target} for a dynamic land scale parameters framework of {land_size_input} located in the geographical territory of {location_input}. 
                    Contrast upfront initial capital expenditure (CapEx) metrics, direct manual labor hours, and expected final yield values.
                    """
                    response = model.generate_content(f3_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")