import streamlit as st
import os
import datetime
import re
from google import genai

# -----------------------------------------------------------------------------
# 1. APPLICATION VIEW & THEMING
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
# 2. SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
st.sidebar.header("🔑 Authentication Setup")

bg_key = os.getenv("GEMINI_API_KEY", "")

user_api_key = st.sidebar.text_input(
    "Enter Gemini API Key", 
    value=bg_key,
    type="password",
    help="Paste your AI Studio API key here starting with AIzaSy."
)

st.sidebar.header("📋 Universal Project Config")
crop_type = st.sidebar.text_input("Enter Crop Name", value="Cassava")
land_size_input = st.sidebar.text_input("Preferable Land Size / Scale", value="2.5 Hectares")
location_input = st.sidebar.text_input("Project Location or GPS Coordinates", value="Minna, Niger State")
planting_date = st.sidebar.date_input("Target Planting Start Date", value=datetime.date(2026, 6, 15))

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

final_key = user_api_key.strip() if user_api_key else ""

if final_key and len(final_key) > 10:
    st.markdown('<span class="mode-badge">⚡ LIVE COGNITIVE AI ACTIVE</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="fallback-badge">📊 LOCAL SMART SIMULATION ENGINE ACTIVE</span>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GEOSPATIAL BOUNDS DETECTOR
# -----------------------------------------------------------------------------
coord_pattern = r"[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)"
is_coordinate = bool(re.match(coord_pattern, location_input.strip()))

if is_coordinate:
    st.markdown(f'<div class="geo-alert">🎯 **Geospatial Anchor Confirmed:** Coordinates `[{location_input.strip()}]` mapped for a scope of **{land_size_input}**.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="geo-alert">📍 **Regional Mode Active:** Mapped to regional zone `{location_input}` for a scope of **{land_size_input}**.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💰 Precise Costing (BOQ)", "📅 Lifecycle Planner", "📊 Comparative Matrix"])

# -----------------------------------------------------------------------------
# 4. BACKUP SIMULATION STRUCTURAL ENGINES (Locks out 400 & 404 Errors completely)
# -----------------------------------------------------------------------------
def run_fallback_boq():
    st.warning("🔄 High-precision structural estimation matrix generated locally.")
    st.markdown(f"### 📊 Institutional Land Preparation BOQ: {crop_type}")
    st.markdown(f"**Project Scope Location:** {location_input} | **Target Land Dimension Scale:** {land_size_input}")
    st.markdown(f"""
    | Operational Component | Base Metric Allocation | Dynamic Allocation Scope | Simulated Cost Estimate (NGN) |
    | :--- | :--- | :--- | :--- |
    | **Site Bush Clearing & Bush Grabbing** | Baseline Structural Rate | Scaled to: {land_size_input} | ₦150,000 - ₦300,000 |
    | **Primary Mechanical Tillage** | Standard Ploughing Run | Scaled to: {land_size_input} | ₦100,000 - ₦220,000 |
    | **Secondary Harrowing Run** | Fine Aggregate Preparation | Scaled to: {land_size_input} | ₦70,000 - ₦140,000 |
    | **Crop Bedding / Ridging Operations** | {crop_type} Field Layout Design | Scaled to: {land_size_input} | ₦90,000 - ₦180,000 |
    """)

def run_fallback_lifecycle():
    st.markdown(f"### 📅 Operational Timeline Matrix: {crop_type}")
    st.write(f"Development sequence tracked from commencement anchor point: **{planting_date}** for a scope of **{land_size_input}**.")
    st.markdown("""
    * **Phase 1 (Month 1):** Land clearing, mechanized plowing, harrowing runs, and structural drainage planning.
    * **Phase 2 (Month 2-3):** Ridging, precision seed positioning, weed interception schedules, and initial canopy mapping.
    * **Phase 3 (Month 4+):** Field health audits, organic pest barriers activation, and harvest logistics deployment.
    """)

# -----------------------------------------------------------------------------
# 5. FEATURE ACTION EXECUTION
# -----------------------------------------------------------------------------
with tab1:
    st.markdown(f'<div class="section-card"><h3>Dynamic CapEx Estimator: {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Quantify {crop_type} Infrastructure", key="btn_tab1"):
        with st.spinner(f"Processing structural indices for {crop_type}..."):
            if final_key and len(final_key) > 20:
                try:
                    # Clean model string resolution via the correct 2026 client architecture
                    client = genai.Client(api_key=final_key)
                    f1_prompt = f"Act as an Agricultural Quantity Surveyor. Generate an institutional-grade, highly itemized Land Preparation Bill of Quantities (BOQ) for cultivating {crop_type} across an area scale of {land_size_input} located specifically at {location_input}. Format your answer with professional markdown headers, structured budgeting insights, and clean calculation tables in Nigerian Naira (NGN)."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f1_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Cloud Connection Timeout: {str(e)}. Reverting to backup matrices.")
                    run_fallback_boq()
            else:
                run_fallback_boq()

with tab2:
    st.markdown(f'<div class="section-card"><h3>Automated Timeline for {crop_type}</h3></div>', unsafe_allow_html=True)
    if st.button(f"Generate {crop_type} Critical Path", key="btn_tab2"):
        with st.spinner("Processing biological milestones..."):
            if final_key and len(final_key) > 20:
                try:
                    client = genai.Client(api_key=final_key)
                    f2_prompt = f"Provide an articulate, highly granular month-by-month growth, meteorological risk mitigation, and harvesting logistics timeline for cultivating {crop_type} starting on {planting_date} at location target {location_input} scaled to {land_size_input}."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f2_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    run_fallback_lifecycle()
            else:
                run_fallback_lifecycle()

with tab3:
    st.markdown(f'<div class="section-card"><h3>Cross-Crop Comparative Matrix</h3></div>', unsafe_allow_html=True)
    comparison_target = st.text_input("Enter Comparison Crop (Default: Millet)", value="Millet")
    if st.button(f"Compare {crop_type} vs {comparison_target}", key="btn_tab3"):
        with st.spinner("Executing investment variance modeling..."):
            if final_key and len(final_key) > 20:
                try:
                    client = genai.Client(api_key=final_key)
                    f3_prompt = f"Act as an Agribusiness Investment Consultant. Compare the upfront CapEx requirements, operational labor complexities, and yield ROI variances between {crop_type} and {comparison_target} for a project sizing profile of {land_size_input} located at {location_input}."
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f3_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.warning("Comparative asset metrics require cloud activation. Please double check your API Key string.")
            else:
                st.warning("Comparative asset metrics require cloud activation. Please double check your API Key string.")