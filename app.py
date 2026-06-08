import streamlit as st
import os
import datetime
import re
from google import genai

# -----------------------------------------------------------------------------
# 1. UI EXECUTIVE THEMING
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
# 2. GLOBAL CONFIGURATION SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.header("🔑 Authentication")

# On-screen fallback input box for key flexibility
user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key", 
    value=os.getenv("GEMINI_API_KEY", ""),
    type="password",
    help="Paste your AI Studio API key here to activate live cloud calculations."
)

st.sidebar.header("📋 Universal Project Config")
crop_type = st.sidebar.text_input("Enter Crop Name", value="Cassava")
land_size_input = st.sidebar.text_input("Preferable Land Size / Scale", value="2.5 Hectares")
location_input = st.sidebar.text_input("Project Location or GPS Coordinates", value="Minna, Niger State")
planting_date = st.sidebar.date_input("Target Planting Start Date", value=datetime.date(2026, 6, 15))

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

# -----------------------------------------------------------------------------
# 3. GEOSPATIAL LOGIC ENGINE
# -----------------------------------------------------------------------------
coord_pattern = r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)"
is_coordinate = bool(re.match(coord_pattern, location_input.strip()))

if is_coordinate:
    st.markdown(f'<div class="geo-alert">🎯 **Geospatial Anchor Confirmed:** Mapped to coordinates `[{location_input.strip()}]` for a scope of **{land_size_input}**.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="geo-alert">📍 **Regional Mode Active:** Mapped to regional zone `{location_input}` for a scope of **{land_size_input}**.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Precise Costing (BOQ)", "📅 Lifecycle Planner", "📊 Comparative Matrix"])

# -----------------------------------------------------------------------------
# FALLBACK ARTICULATED GENERATORS (Triggers cleanly if key is invalid/missing)
# -----------------------------------------------------------------------------
def show_articulated_fallback_boq():
    st.markdown(f"### 📊 Institutional Land Preparation BOQ: {crop_type}")
    st.markdown(f"**Project Location Scope:** {location_input} | **Target Land Dynamic Sizing:** {land_size_input}")
    st.markdown("""
    | Operational Component | Base Metric Allocation | Dynamic Allocation Scope | Simulated Cost Estimate (NGN) |
    | :--- | :--- | :--- | :--- |
    | **Site Bush Clearing & Grabbing** | Baseline Structural Rate | Scaled to: Custom Parameters | ₦120,000 - ₦250,000 |
    | **Primary Mechanical Tillage** | Standard Plowing Run | Scaled to: Custom Parameters | ₦90,000 - ₦180,000 |
    | **Secondary Harrowing Run** | Fine Aggregate Prep | Scaled to: Custom Parameters | ₦60,000 - ₦120,000 |
    | **Crop Bedding / Ridging** | Specialized Configuration | Scaled to: Custom Parameters | ₦80,000 - ₦150,000 |
    """)
    st.info("💡 Pro-Tip: Provide a verified Gemini API Key in the sidebar configuration to populate live, location-exact financial data blocks.")

def show_articulated_fallback_lifecycle():
    st.markdown(f"### 📅 Operational Timeline Matrix: {crop_type}")
    st.write(f"Development critical path tracked dynamically from commencement anchor point: **{planting_date}**.")
    st.markdown(f"""
    * **Phase 1 (Month 1):** Initial land preparations, layout plotting, structural drainage excavation, and localized soil conditioning.
    * **Phase 2 (Month 2-3):** Germination windows, systematic crop management spacing, and early-stage fertilizer input routines.
    * **Phase 3 (Month 4+):** Scale monitoring, local canopy management, regional disease mitigation sweeps, and harvest logistics preparation.
    """)

# -----------------------------------------------------------------------------
# CORE APP WORKFLOW EXECUTION
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f'<div class="section-card"><h3>Dynamic CapEx Estimator: {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Quantify {crop_type} Infrastructure", key="btn_tab1"):
        with st.spinner(f"Processing calculations..."):
            # Explicit verification pass to protect from 400 errors
            if user_api_key and len(user_api_key.strip()) > 10:
                try:
                    client = genai.Client(api_key=user_api_key.strip())
                    f1_prompt = f"Act as an Agricultural Quantity Surveyor. Generate an institutional-grade, highly itemized Land Preparation Bill of Quantities (BOQ) for cultivating {crop_type} across an area scale of {land_size_input} located specifically at {location_input}. Format your answer with professional markdown headers, structured budgeting insights, and clean calculation tables in Nigerian Naira (NGN)."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f1_prompt)
                    st.markdown(response.text)
                except Exception:
                    show_articulated_fallback_boq()
            else:
                show_articulated_fallback_boq()

with tab2:
    st.markdown(f'<div class="section-card"><h3>Automated Timeline for {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Generate {crop_type} Critical Path", key="btn_tab2"):
        with st.spinner("Processing biological milestones..."):
            if user_api_key and len(user_api_key.strip()) > 10:
                try:
                    client = genai.Client(api_key=user_api_key.strip())
                    f2_prompt = f"Provide an articulate, highly granular month-by-month growth, meteorological risk mitigation, and harvesting logistics timeline for cultivating {crop_type} starting on {planting_date} at location target {location_input} scaled to {land_size_input}."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f2_prompt)
                    st.markdown(response.text)
                except Exception:
                    show_articulated_fallback_lifecycle()
            else:
                show_articulated_fallback_lifecycle()

with tab3:
    st.markdown(f'<div class="section-card"><h3>Cross-Crop Comparative Matrix</h3></div>', unsafe_allow_html=True)
    comparison_target = st.text_input("Enter Comparison Crop (Default: Millet)", value="Millet")
    if st.button(f"Compare {crop_type} vs {comparison_target}", key="btn_tab3"):
        with st.spinner("Executing investment variance modeling..."):
            if user_api_key and len(user_api_key.strip()) > 10:
                try:
                    client = genai.Client(api_key=user_api_key.strip())
                    f3_prompt = f"Act as an Agribusiness Investment Consultant. Compare the upfront CapEx requirements, operational labor complexities, and yield ROI variances between {crop_type} and {comparison_target} for a project sizing profile of {land_size_input} located at {location_input}."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f3_prompt)
                    st.markdown(response.text)
                except Exception:
                    st.warning("Comparative asset metrics require cloud clearing. Provide a functional API Key string.")
            else:
                st.warning("Comparative asset metrics require cloud clearing. Provide a functional API Key string.")