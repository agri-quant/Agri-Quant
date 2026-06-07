import streamlit as st
import os
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. API INITIALIZATION & CONFIGURATION
# -----------------------------------------------------------------------------
# Securely fetch the API key from environment variables (configured in hosting secrets)
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
    st.warning("⚠️ GEMINI_API_KEY environment variable not found. Please set it to enable AI features.")

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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌾 Agri-Quant Architecture</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Agribusiness Cost Estimation, Logistics Planner & Investment Matrix</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. GLOBAL INPUT PARAMETERS (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Project Configuration")
crop_type = st.sidebar.selectbox("Primary Target Crop", ["Cassava", "Groundnuts", "Ginger"])
land_size = st.sidebar.number_input("Land Size (Hectares)", min_value=0.5, max_value=500.0, value=2.0, step=0.5)
location = st.sidebar.text_input("Project Location (State/LGA)", value="Abuja (Kuje LGA)")
planting_date = st.sidebar.date_input("Target Planting Start Date")

st.sidebar.markdown("---")
st.sidebar.info("**Developer Profile:**\nMuhammad Alfa Kure\n*AI Operations Consultant*")

# Check if client initialized before rendering application logic
if client:
    
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
                
                # Context-Aware Prompt Design utilizing your exact consultant framework
                f1_prompt = f"""
                You are an expert Agricultural Quantity Surveyor and Agribusiness Operations Consultant specializing in West African cash crops.
                
                TASK: Generate an institutional-grade Capital Expenditure (CapEx) blueprint for land preparation.
                
                OPERATIONAL PARAMETERS:
                - Crop Type: {crop_type}
                - Land Area: {land_size} Hectares
                - Project Location: {location}
                
                REQUIRED STRUCTURE:
                Provide your response in clear Markdown with the following exact headings:
                ### 1. Executive Summary
                ### 2. Itemized Land Preparation Cost Estimation Table
                   (Include columns: Operation [Clearing, Plowing, Harrowing, Ridging], Estimated Cost Range per Hectare in Nigerian Naira (NGN), Scaled Cost for {land_size} Hectares, and AI Cost-Confidence Level).
                ### 3. Regional Logistics Constraints & Variables
                ### 4. Operational Cost Optimization Recommendations (List exactly 3 actionable strategies)
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f1_prompt,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {e}")

    # -----------------------------------------------------------------------------
    # FEATURE 2: DYNAMIC CROP LIFECYCLE & RISK PLANNER
    # -----------------------------------------------------------------------------
    with tab2:
        st.markdown('<div class="section-card"><h3>Automated Operational Timeline & Mitigation Engine</h3>'
                    'Maps out precise workflow timelines and injects predictive risk mitigation frameworks.</div>', unsafe_allow_html=True)
        
        if st.button("Generate Critical Path Lifecycle Blueprint", key="btn_tab2"):
            with st.spinner("Compiling agricultural timeline matrices..."):
                
                f2_prompt = f"""
                You are an advanced AI Systems Agronomist and Supply Chain Automation Specialist.
                
                TASK: Build a synchronized crop lifecycle and risk analysis timeline.
                
                OPERATIONAL PARAMETERS:
                - Crop Type: {crop_type}
                - Target Commencement Date: {planting_date}
                - Project Location: {location}
                
                REQUIRED STRUCTURE:
                Provide your response in clear Markdown with the following exact headings:
                ### 1. Phased Crop Lifecycle Timeline
                   (Break down the critical milestones into: Phase 1: Land Prep & Pre-planting, Phase 2: Planting & Vegetative Growth, Phase 3: Input/Fertilizer Windows, Phase 4: Harvesting & Logistics). Assign specific calendar months/weeks starting from {planting_date}.
                ### 2. Regional Risk Assessment & Mitigation Framework
                   (Identify specific regional risks such as localized rainfall patterns for {location}, soil factors, and pest patterns).
                ### 3. Automated Alert Milestones (Key triggers for logistical management)
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f2_prompt,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {e}")

    # -----------------------------------------------------------------------------
    # FEATURE 3: COMPARATIVE INVESTMENT MATRIX GENERATOR
    # -----------------------------------------------------------------------------
    with tab3:
        st.markdown('<div class="section-card"><h3>Cross-Crop Financial Modeling & Analytics</h3>'
                    'Compares your primary crop target against alternative profiles to optimize resource allocation.</div>', unsafe_allow_html=True)
        
        # Dynamically set alternative crop for analytical comparison
        alt_crop = "Ginger" if crop_type in ["Cassava", "Groundnuts"] else "Groundnuts"
        
        st.write(f"This session will execute a comparative yield and financial risk evaluation: **{crop_type}** vs. **{alt_crop}**.")
        
        if st.button("Execute Comparative Investment Matrix", key="btn_tab3"):
            with st.spinner("Processing complex multi-crop financial algorithms..."):
                
                f3_prompt = f"""
                You are a senior Financial Analyst specializing in Agricultural Assets and Venture Capital models.
                
                TASK: Generate an institutional-grade Comparative Investment Matrix.
                
                OPERATIONAL PARAMETERS:
                - Primary Option: {crop_type}
                - Benchmark Alternative: {alt_crop}
                - Land Scale: {land_size} Hectares
                - Region: {location}
                
                REQUIRED STRUCTURE:
                Provide your response in clear Markdown with the following exact headings:
                ### 1. Comparative Financial Metric Matrix
                   (Provide a clean markdown table comparing: Initial Capital Requirements, Gestation/ROI Timelines, Labor Intensity Level, Local Market Demand, and Average Profitability Margin per Hectare).
                ### 2. Strategic Trade-off Analysis
                ### 3. Investment Decision Verdict
                   (Provide an explicit, data-driven recommendation for an investor operating with {land_size} hectares in {location}).
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f3_prompt,
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Execution Error: {e}")
else:
    st.info("💡 To run the live application successfully, ensure you paste your API token into the system backend or setup file.")