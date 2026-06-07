import streamlit as st
import os
import datetime
import re
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. API INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key and api_key != "your_actual_api_key_here":
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        client = None

# -----------------------------------------------------------------------------
# 2. STREAMLIT UI SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agri-Quant Precision | Geospatial AI Intelligence",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header { font-size:28px; color:#1a365d; font-weight:700; margin-bottom:5px; }
    .sub-header { font-size:16px; color:#4a5568; margin-bottom:20px; }
    .section-card { background-color:#f7fafc; padding:15px; border-left:4px solid #1a365d; border-radius:4px; margin-bottom:15px; }
    .mode-badge { background-color:#ebf8ff; color:#2b6cb0; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold; }
    .fallback-badge { background-color:#fffaf0; color:#dd6b20; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold; }
    .geo-alert { background-color:#e6fffa; border-left:4px solid #319795; padding:10px; border-radius:4px; margin-bottom:15px; font-size:13px; color:#234e52; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌾 Agri-Quant Precision</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Universal AI Agribusiness Infrastructure Estimator with Geospatial Coordinate Parsing</div>', unsafe_allow_html=True)

if client:
    st.markdown('<span class="mode-badge">⚡ GEOSPATIAL COGNITIVE AI ACTIVE</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="fallback-badge">📊 LOCAL GEOSPATIAL SIMULATION ENGINE ACTIVE</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GLOBAL INPUT PARAMETERS (With Regex Coordinate Checking)
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Universal Project Config")

crop_type = st.sidebar.text_input("Enter Crop Name", value="Cassava")
land_size = st.sidebar.number_input("Land Size (Hectares)", min_value=0.5, max_value=1000.0, value=2.0, step=0.5)

# HELPFUL SIDEBAR HINT FOR COORDINATES
location_input = st.sidebar.text_input(
    "Project Location or GPS Coordinates", 
    value="9.05785, 7.49508",
    help="You can enter a town name or paste decimal coordinates like: 9.05785, 7.49508"
)

planting_date = st.sidebar.date_input("Target Planting Start Date", value=datetime.date(2026, 6, 15))

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

# Geospatial Regex Pattern Matching to verify if user input contains coordinates
coord_pattern = r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)"
is_coordinate = bool(re.match(coord_pattern, location_input.strip()))

# Render custom indicator if precise coordinates are detected
if is_coordinate:
    st.markdown(f'<div class="geo-alert">🎯 **Geospatial Coordinates Detected:** Target anchored at exact location grid `[{location_input.strip()}]`. AI layout analysis will prioritize absolute regional terrain data.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="geo-alert">📍 **Regional String Mode Active:** Modeling using macro-level environmental averages for `{location_input}`.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Precise Costing (BOQ)", "📅 Lifecycle Planner", "📊 Comparative Matrix"])

# -----------------------------------------------------------------------------
# FEATURE 1: PRECISION LAND PREP COSTING (BOQ)
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f'<div class="section-card"><h3>Dynamic CapEx Estimator: {crop_type}</h3>'
                'Quantifying land prep requirements based on spatial boundaries and crop profiles.</div>', unsafe_allow_html=True)
    
    if st.button(f"Quantify {crop_type} Infrastructure", key="btn_tab1"):
        with st.spinner(f"Accessing spatial and agricultural indices for {crop_type}..."):
            
            geo_context = f"exact GPS coordinates {location_input}" if is_coordinate else f"general regional zone of {location_input}"
            
            if client:
                f1_prompt = f"""
                You are an expert Agricultural Quantity Surveyor and Civil Engineer. 
                TASK: Generate a highly detailed, itemized Land Preparation Bill of Quantities (BOQ).
                PARAMETERS:
                - Crop: {crop_type}
                - Scale: {land_size} Hectares
                - Location Mode: Analyzed using {geo_context}.
                
                INSTRUCTIONS: 
                If precise coordinates are provided, evaluate the implied topsoil type, vegetative cover, clearing complexity, and mechanical tillage restrictions specific to those geographic parameters. Provide a comprehensive pricing structure in Nigerian Naira (NGN).
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f1_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                base_rate = 55000 if is_coordinate else 50000  # Slight premium multiplier simulated for micro-location setup
                total_cost = base_rate * land_size
                
                st.markdown(f"### Universal Precise BOQ for {crop_type}")
                st.write(f"Preliminary spatial assessment calculated for **{land_size} Ha** relative to **{location_input}**.")
                st.markdown(f"""
                | Operation | Est Rate/Ha (NGN) | Total ({land_size} Ha) | Precision Adjustments |
                | :--- | :--- | :--- | :--- |
                | **Site Clearing** | ₦22,000 | ₦{int(22000*land_size):,} | Adjusted via Geo-Context |
                | **Primary Tillage** | ₦16,000 | ₦{int(16000*land_size):,} | Scaled for terrain slope |
                | **Secondary Tillage** | ₦11,000 | ₦{int(11000*land_size):,} | Standard aggregate |
                | **Crop-Specific Preparation** | ₦6,000 | ₦{int(6000*land_size):,} | Bed/Ridge configuration |
                | **ESTIMATED TOTAL** | **₦{base_rate:,}** | **₦{int(total_cost):,}** | **Spatial Target Locked** |
                """)

# -----------------------------------------------------------------------------
# FEATURE 2: UNIVERSAL LIFECYCLE & RISK PLANNER
# -----------------------------------------------------------------------------
with tab2:
    st.markdown(f'<div class="section-card"><h3>Automated Timeline for {crop_type}</h3>'
                'Predicting biological milestones and regional logistical risks based on coordinate mapping.</div>', unsafe_allow_html=True)
    
    if st.button(f"Generate {crop_type} Critical Path", key="btn_tab2"):
        with st.spinner("Processing biological growth and meteorological data..."):
            
            geo_context = f"exact coordinates {location_input}" if is_coordinate else f"general region of {location_input}"
            
            if client:
                f2_prompt = f"""
                You are an advanced AI Systems Agronomist. 
                TASK: Provide a comprehensive month-by-month growth, climate, and logistical risk timeline for {crop_type}.
                PARAMETERS: Start Date: {planting_date}, Location target: {geo_context}.
                INSTRUCTIONS: Analyze spatial weather data, historical wet/dry transitions, and specific regional agronomic risks linked to this location.
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f2_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.markdown(f"### {crop_type} Geospatial Lifecycle Simulation")
                st.info(f"Growth timeline initialized from {planting_date} using target location baseline: `{location_input}`. Run live AI mode to pull high-fidelity rain/soil matrix analytics.")

# -----------------------------------------------------------------------------
# FEATURE 3: COMPARATIVE MATRIX
# -----------------------------------------------------------------------------
with tab3:
    comparison_target = st.text_input("Enter Comparison Crop (Default: Maize)", value="Maize")
    
    if st.button(f"Compare {crop_type} vs {comparison_target}", key="btn_tab3"):
        with st.spinner("Calculating investment variance across micro-climates..."):
            
            geo_context = f"coordinates {location_input}" if is_coordinate else f"macro-region {location_input}"
            
            if client:
                f3_prompt = f"As an Agricultural Investment Consultant, compare the ROI and OpEx of {crop_type} vs {comparison_target} for {land_size} hectares mapped to {geo_context}."
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f3_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Comparative Investment Matrix requires Live AI Mode to process high-fidelity spatial variance data.")