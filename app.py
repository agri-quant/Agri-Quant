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
    page_title="Agri-Quant Elite | Geospatial AI Intelligence",
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

st.markdown('<div class="main-header">🌾 Agri-Quant Elite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Universal Dynamic AI Agribusiness Quantity Surveying & Spatial Planning Architecture</div>', unsafe_allow_html=True)

if client:
    st.markdown('<span class="mode-badge">⚡ GEOSPATIAL COGNITIVE AI ACTIVE</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="fallback-badge">📊 LOCAL QUANTITY SURVEYING SIMULATION ENGINE ACTIVE</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GLOBAL INPUT PARAMETERS (Fully Dynamic Fields)
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Universal Project Config")

# Universal Crop Input
crop_type = st.sidebar.text_input("Enter Crop Name", value="Cassava")

# UPDATED: Flexible Land Size Text Input to support any unit preferences
land_size_input = st.sidebar.text_input(
    "Preferable Land Size / Scale", 
    value="2.5 Hectares",
    help="Type any preferable size or scale format, e.g., '5 Hectares', '10 Acres', '24 Plots', or '0.75 Ha'"
)

# Universal Location/Coordinate Input
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

# Render dynamic visual feedback indicator based on location mode
if is_coordinate:
    st.markdown(f'<div class="geo-alert">🎯 **Geospatial Anchor Confirmed:** Mapped to coordinates `[{location_input.strip()}]` for a scope of **{land_size_input}**. AI layout analysis will prioritize absolute micro-terrain constraints.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="geo-alert">📍 **Regional Mode Active:** Mapped to regional zone `{location_input}` for a scope of **{land_size_input}**. AI modeling using macro-level environmental metrics.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Precise Costing (BOQ)", "📅 Lifecycle Planner", "📊 Comparative Matrix"])

# -----------------------------------------------------------------------------
# FEATURE 1: UNIVERSAL LAND PREP COSTING (BOQ)
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f'<div class="section-card"><h3>Dynamic CapEx Estimator: {crop_type}</h3>'
                f'Quantifying agricultural infrastructure requirements scaled to your exact parameters.</div>', unsafe_allow_html=True)
    
    if st.button(f"Quantify {crop_type} Infrastructure", key="btn_tab1"):
        with st.spinner(f"Accessing spatial and construction indices for {crop_type}..."):
            
            geo_context = f"exact GPS coordinates {location_input}" if is_coordinate else f"general regional zone of {location_input}"
            
            if client:
                f1_prompt = f"""
                You are an expert Agricultural Quantity Surveyor, Logistics Consultant, and Civil Engineer. 
                
                TASK: Generate an institutional-grade, highly itemized Land Preparation Bill of Quantities (BOQ) and cost blueprint.
                
                PARAMETERS:
                - Crop Target: {crop_type}
                - Mapped Land Dimension/Scale: {land_size_input}
                - Geographical Placement: Evaluated using {geo_context}.
                
                INSTRUCTIONS: 
                Analyze the input scale statement '{land_size_input}'. Standardize it to calculate clearing boundaries. If precise coordinates are provided, evaluate implied topsoil conditions, localized clearing complexity, and mechanical tillage restrictions native to those precise bounds. Provide a clean, structured financial breakdown table in Nigerian Naira (NGN).
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f1_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                # Universal Offline Simulation Fallback
                st.markdown(f"### Universal Precise BOQ for {crop_type}")
                st.write(f"Preliminary structural budget calculated for a project scale of **{land_size_input}** located at **{location_input}**.")
                st.markdown(f"""
                | Operational Component | Base Metric Allocation | Dynamic Allocation Scope | Target Precision Mode |
                | :--- | :--- | :--- | :--- |
                | **Site Bush Clearing** | Baseline Rate | Scaled to: {land_size_input} | Coordinates Responsive |
                | **Primary Mechanical Tillage** | Standard Plowing | Scaled to: {land_size_input} | Slope-Factor Optimized |
                | **Secondary Harrowing Run** | Fine Aggregates | Scaled to: {land_size_input} | Soil-Texture Adaptive |
                | **Crop Bedding / Ridging** | {crop_type} Custom Spec | Scaled to: {land_size_input} | Structural Target Mapped |
                """)
                st.info("💡 Run live AI mode by activating your API Key to populate raw real-time Naira values for this non-standardized dimension configuration.")

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
                You are an advanced AI Systems Agronomist and Developmental Logistics Officer. 
                
                TASK: Provide a comprehensive month-by-month growth, weather risk, and supply chain timeline for cultivating {crop_type}.
                
                PARAMETERS: 
                - Crop: {crop_type}
                - Scaled Scope: {land_size_input}
                - Target Commencement Date: {planting_date}
                - Location Target: Mapped to {geo_context}.
                
                INSTRUCTIONS: Analyze regional precipitation cycles, localized soil attributes, harvest extraction times, and storage/transit logistics adjustments required for a field operation sizing of '{land_size_input}'.
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f2_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.markdown(f"### {crop_type} Geospatial Lifecycle Simulation")
                st.info(f"Critical path sequence mapped from template start date {planting_date} for a field size of **{land_size_input}**. Run live AI mode to execute deep seasonal meteorological analytics.")

# -----------------------------------------------------------------------------
# FEATURE 3: COMPARATIVE MATRIX
# -----------------------------------------------------------------------------
with tab3:
    comparison_target = st.text_input("Enter Comparison Crop (Default: Maize)", value="Maize")
    
    if st.button(f"Compare {crop_type} vs {comparison_target}", key="btn_tab3"):
        with st.spinner("Calculating investment variance across micro-climates..."):
            
            geo_context = f"coordinates {location_input}" if is_coordinate else f"macro-region {location_input}"
            
            if client:
                f3_prompt = f"""
                You are a Senior Financial Analyst specializing in Agricultural Assets.
                
                TASK: Compare the risk-return profiles, initial capital expenditures, and yield outputs of two crops.
                
                PARAMETERS:
                - Primary Candidate: {crop_type}
                - Comparison Target: {comparison_target}
                - Project Scope Size: {land_size_input}
                - Location Baseline: Mapped to {geo_context}.
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f3_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Comparative Investment Matrix requires Live AI Mode to process high-fidelity spatial variance data.")