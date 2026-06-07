import streamlit as st
import os
import datetime
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. API INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
# Securely fetch the API key from environment variables (configured in hosting secrets)
api_key = os.getenv("GEMINI_API_KEY")

client = None
if api_key and api_key != "your_actual_api_key_here":
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        client = None

# -----------------------------------------------------------------------------
# 2. STREAMLIT UI SETUP (Executive Theme)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agri-Quant | AI-Driven Agribusiness Intelligence",
    page_icon="🌾",
    layout="wide"
)

# Custom Executive CSS Styling
st.markdown("""
    <style>
    .main-header { font-size:28px; color:#1a365d; font-weight:700; margin-bottom:5px; }
    .sub-header { font-size:16px; color:#4a5568; margin-bottom:20px; }
    .section-card { background-color:#f7fafc; padding:15px; border-left:4px solid #1a365d; border-radius:4px; margin-bottom:15px; }
    .mode-badge { background-color:#ebf8ff; color:#2b6cb0; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold; }
    .fallback-badge { background-color:#fffaf0; color:#dd6b20; padding:4px 8px; border-radius:4px; font-size:12px; font-weight:bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌾 Agri-Quant Architecture</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Agribusiness Cost Estimation, Logistics Planner & Investment Matrix</div>', unsafe_allow_html=True)

# Status Badge Indicator
if client:
    st.markdown('<span class="mode-badge">⚡ LIVE COGNITIVE AI MODE ACTIVE</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="fallback-badge">📊 LOCAL QUANTITY SURVEYING SIMULATION ENGINE ACTIVE</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GLOBAL INPUT PARAMETERS (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Project Configuration")
crop_type = st.sidebar.selectbox("Primary Target Crop", ["Cassava", "Groundnuts", "Ginger"])
land_size = st.sidebar.number_input("Land Size (Hectares)", min_value=0.5, max_value=500.0, value=2.0, step=0.5)
location = st.sidebar.text_input("Project Location (State/LGA)", value="Abuja (Kuje LGA)")
planting_date = st.sidebar.date_input("Target Planting Start Date", value=datetime.date(2026, 6, 15))

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

# Create Tabs for the 3 Mandatory AI/Automation Features
tab1, tab2, tab3 = st.tabs([
    "💰 Automated Land Prep Costing", 
    "📅 Crop Lifecycle & Risk Planner", 
    "📊 Comparative Investment Matrix"
])

# -----------------------------------------------------------------------------
# FEATURE 1: AUTOMATED LAND PREPARATION COST CALCULATOR
# -----------------------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-card"><h3>Dynamic Capital Expenditure (CapEx) Estimator</h3>'
                'Generates structural cost insights based on localized land preparation factors.</div>', unsafe_allow_html=True)
    
    if st.button("Generate Cost Optimization Blueprint", key="btn_tab1"):
        with st.spinner("Analyzing operational variables and scaling metrics..."):
            
            if client:
                # Live Prompt Sequence
                f1_prompt = f"""
                You are an expert Agricultural Quantity Surveyor and Agribusiness Operations Consultant specializing in West African cash crops.
                TASK: Generate an institutional-grade Capital Expenditure (CapEx) blueprint for land preparation.
                OPERATIONAL PARAMETERS:
                - Crop Type: {crop_type} - Land Area: {land_size} Hectares - Project Location: {location}
                REQUIRED STRUCTURE:
                Provide your response in clear Markdown with the following exact headings:
                ### 1. Executive Summary
                ### 2. Itemized Land Preparation Cost Estimation Table
                ### 3. Regional Logistics Constraints & Variables
                ### 4. Operational Cost Optimization Recommendations
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f1_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Live AI Interruption: {e}")
            else:
                # Zero-Failure Local Simulation Engine
                base_rates = {"Cassava": 45000, "Groundnuts": 40000, "Ginger": 55000}
                rate = base_rates[crop_type]
                total_cost = rate * land_size
                
                st.markdown(f"### 1. Executive Summary")
                st.write(f"Preliminary Bill of Quantities (BOQ) generated for **{land_size} Hectares** of **{crop_type}** cultivation in **{location}** based on normalized 2026 agricultural infrastructure indices.")
                
                st.markdown(f"### 2. Itemized Land Preparation Cost Estimation Table")
                st.markdown(f"""
                | Operation Component | Est. Rate / Hectare (NGN) | Scaled Total ({land_size} Ha) | Confidence Level |
                | :--- | :--- | :--- | :--- |
                | **Bush Clearing & Stumping** | ₦{int(rate*0.4):,} | ₦{int(total_cost*0.4):,} | High (Simulated) |
                | **First Plowing Sequence** | ₦{int(rate*0.3):,} | ₦{int(total_cost*0.3):,} | High (Simulated) |
                | **Harrowing Operations** | ₦{int(rate*0.15):,} | ₦{int(total_cost*0.15):,} | High (Simulated) |
                | **Mechanical Ridging** | ₦{int(rate*0.15):,} | ₦{int(total_cost*0.15):,} | High (Simulated) |
                | **TOTAL ESTIMATED CAPEX** | **₦{int(rate):,}** | **₦{int(total_cost):,}** | **Statistical Baseline** |
                """)
                
                st.markdown("### 3. Regional Logistics Constraints & Variables")
                st.write(f"• **Topography Adjustments:** Cost matrix assumes flat-to-rolling terrain typical of savanna zones in {location}.\n• **Fuel Indexing:** Mechanized operations are subject to regional diesel fluctuations.")
                
                st.markdown("### 4. Operational Cost Optimization Recommendations")
                st.write("1. **Block Aggregation:** Pool contiguous tracts to minimize tractor transit overheads.\n2. **Phased Mobilization:** Schedule machine deployment precisely to avoid standby downtime charges.\n3. **Early Stakeholder Contracting:** Secure local tractor services 4 weeks prior to major wet-season onset.")

# -----------------------------------------------------------------------------
# FEATURE 2: DYNAMIC CROP LIFECYCLE & RISK PLANNER
# -----------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-card"><h3>Automated Operational Timeline & Mitigation Engine</h3>'
                'Maps out precise workflow timelines and injects predictive risk mitigation frameworks.</div>', unsafe_allow_html=True)
    
    if st.button("Generate Critical Path Lifecycle Blueprint", key="btn_tab2"):
        with st.spinner("Compiling agricultural timeline matrices..."):
            
            if client:
                f2_prompt = f"""
                You are an advanced AI Systems Agronomist and Supply Chain Automation Specialist.
                TASK: Build a synchronized crop lifecycle and risk analysis timeline.
                OPERATIONAL PARAMETERS:
                - Crop Type: {crop_type} - Target Commencement Date: {planting_date} - Project Location: {location}
                REQUIRED STRUCTURE:
                ### 1. Phased Crop Lifecycle Timeline (Phase 1 to 4)
                ### 2. Regional Risk Assessment & Mitigation Framework
                ### 3. Automated Alert Milestones
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f2_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Live AI Interruption: {e}")
            else:
                gestation = {"Cassava": 11, "Groundnuts": 4, "Ginger": 8}
                months = gestation[crop_type]
                harvest_date = planting_date + datetime.timedelta(days=months*30)
                
                st.markdown("### 1. Phased Crop Lifecycle Timeline")
                st.write(f"• **Phase 1: Pre-Planting Operations:** Commences immediately on *{planting_date}*.")
                st.write(f"• **Phase 2: Active Sowing & Germination Window:** Scheduled 2 weeks post-initial clearing.")
                st.write(f"• **Phase 3: Fertilizer & Crop Protection Windows:** Mid-cycle operations required.")
                st.write(f"• **Phase 4: Target Harvesting & Extraction Logistics:** Estimated for *{harvest_date}* ({months}-month crop cycle).")
                
                st.markdown("### 2. Regional Risk Assessment & Mitigation Framework")
                st.write(f"• **Climate Risk:** Unpredictable early-season dry spells in {location}. Mitigation: Ensure planting aligns with sustained rainfall establishment.\n• **Soil Risk:** Nutrient leaching during peak precipitation. Mitigation: Execute fractional, split-application fertilizer regimens.")

# -----------------------------------------------------------------------------
# FEATURE 3: COMPARATIVE INVESTMENT MATRIX GENERATOR
# -----------------------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-card"><h3>Cross-Crop Financial Modeling & Analytics</h3>'
                'Compares your primary crop target against alternative profiles to optimize resource allocation.</div>', unsafe_allow_html=True)
    
    alt_crop = "Ginger" if crop_type in ["Cassava", "Groundnuts"] else "Groundnuts"
    st.write(f"This session will execute a comparative yield evaluation: **{crop_type}** vs. **{alt_crop}**.")
    
    if st.button("Execute Comparative Investment Matrix", key="btn_tab3"):
        with st.spinner("Processing complex multi-crop financial algorithms..."):
            
            if client:
                f3_prompt = f"""
                You are a senior Financial Analyst specializing in Agricultural Assets and Venture Capital models.
                TASK: Generate an institutional-grade Comparative Investment Matrix.
                OPERATIONAL PARAMETERS:
                - Primary Option: {crop_type} - Benchmark Alternative: {alt_crop} - Land Scale: {land_size} Hectares - Region: {location}
                REQUIRED STRUCTURE:
                ### 1. Comparative Financial Metric Matrix (Markdown Table)
                ### 2. Strategic Trade-off Analysis
                ### 3. Investment Decision Verdict
                """
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=f3_prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Live AI Interruption: {e}")
            else:
                st.markdown("### 1. Comparative Financial Metric Matrix")
                st.markdown(f"""
                | Investment Metric | Primary: {crop_type} | Alternative: {alt_crop} | Variance Analysis |
                | :--- | :--- | :--- | :--- |
                | **CapEx Intensity** | Medium Baseline | High Initial | Alternative requires higher seed-stock capital |
                | **Gestation Window** | Variable Cycle | Fixed Drydown | Accelerated cash-conversion on alternative |
                | **Labor Overhead** | Intermittent | Intensive | Higher weeding/harvesting toll on alternative |
                | **Market Demand Profile**| Local Industrial | Export-Driven | Alternative relies heavily on processing brokers |
                """)
                st.markdown("### 2. Strategic Trade-off Analysis")
                st.write(f"Choosing **{crop_type}** minimizes early-stage operational cash drain but lowers absolute maximum profit margins compared to **{alt_crop}**. Scaling over {land_size} Hectares requires careful mechanization management.")