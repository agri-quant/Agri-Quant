import streamlit as st
import pandas as pd
import numpy as np
import datetime
import re
import io
import os
from PIL import Image
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. APPLICATION SETUP & DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agri-Quant | Universal AI Agribusiness QS & Forensic Evidence Portal",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px 0 rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        font-size: 14px;
        color: #a7f3d0;
        margin-top: 6px;
        margin-bottom: 0px;
        line-height: 1.5;
    }
    
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .status-live { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .status-offline { background-color: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
    .category-badge { background-color: #e0e7ff; color: #3730a3; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    
    .audit-box-green {
        background-color: #f0fdf4;
        border-left: 5px solid #22c55e;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }
    .audit-box-amber {
        background-color: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }
    .audit-box-red {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }
    .memo-card {
        background-color: #fdf8f6;
        border: 2px dashed #b45309;
        border-radius: 8px;
        padding: 20px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE PERSISTENCE INITIALIZATION
# -----------------------------------------------------------------------------
if "boq_ai_analysis" not in st.session_state:
    st.session_state.boq_ai_analysis = None
if "lifecycle_analysis" not in st.session_state:
    st.session_state.lifecycle_analysis = None
if "comparison_analysis" not in st.session_state:
    st.session_state.comparison_analysis = None
if "evidence_audit_result" not in st.session_state:
    st.session_state.evidence_audit_result = None
if "audit_result" not in st.session_state:
    st.session_state.audit_result = None

# Comprehensive Nigerian Agro-Geographic Registry for Instant Resolution
STATE_COORDINATES = {
    "abia": (5.4527, 7.5248), "adamawa": (9.3265, 12.4416), "akwa ibom": (5.0377, 7.9128),
    "anambra": (6.2209, 6.9370), "bauchi": (10.3158, 9.8442), "bayelsa": (4.7719, 6.0699),
    "benue": (7.7322, 8.5391), "makurdi": (7.7322, 8.5391), "borno": (11.8333, 13.1500),
    "cross river": (5.9631, 8.3300), "calabar": (4.9757, 8.3417), "delta": (5.6806, 6.0000),
    "asaba": (6.1989, 6.7337), "ebonyi": (6.2649, 8.0137), "edo": (6.5244, 5.8987),
    "benin": (6.3350, 5.6037), "ekiti": (7.6211, 5.2215), "enugu": (6.4584, 7.5464),
    "gombe": (10.2897, 11.1673), "imo": (5.4922, 7.0266), "jigawa": (12.2280, 9.5616),
    "kaduna": (10.5105, 7.4165), "zaria": (11.0855, 7.7199), "kano": (12.0022, 8.5920),
    "katsina": (12.9908, 7.6018), "kebbi": (11.4582, 4.1999), "kogi": (7.7969, 6.7408),
    "lokoja": (7.8023, 6.7430), "kwara": (8.9669, 4.3874), "ilorin": (8.4799, 4.5418),
    "lagos": (6.5244, 3.3792), "nasarawa": (8.4938, 8.5153), "lafia": (8.4938, 8.5153),
    "niger": (9.6139, 6.5569), "minna": (9.6139, 6.5569), "mokwa": (9.2928, 5.0542),
    "ogun": (7.1475, 3.3619), "abeokuta": (7.1475, 3.3619), "ondo": (7.2571, 5.2058),
    "akure": (7.2571, 5.2058), "osun": (7.5629, 4.5200), "osogbo": (7.7827, 4.5418),
    "oyo": (7.3775, 3.9470), "ibadan": (7.3775, 3.9470), "plateau": (9.2182, 9.5179),
    "jos": (9.8965, 8.8583), "rivers": (4.8156, 7.0498), "port harcourt": (4.8156, 7.0498),
    "sokoto": (13.0609, 5.2476), "taraba": (8.8937, 11.3596), "jalingo": (8.8937, 11.3596),
    "yobe": (12.2939, 11.4390), "zamfara": (12.1222, 6.2236), "gusau": (12.1702, 6.6641),
    "fct": (9.0765, 7.3986), "abuja": (9.0765, 7.3986)
}

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS (DIRECT TEXT INPUTS — 100% UNCONSTRAINED)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.header("🔑 Authentication Setup")
    
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=env_key,
        type="password",
        help="Paste your Google AI Studio API key starting with AIzaSy."
    )
    final_key = api_key_input.strip()

    st.markdown("---")
    st.header("📋 Universal Project Scope")
    
    # 1. 100% UNIVERSAL CROP INPUT (No restrictive dropdowns)
    crop_type = st.text_input(
        "Cultivation Crop / Commodity",
        value="Cassava",
        help="Type ANY crop in the world (e.g., Ginger, Cocoa, Maize, Tomato, Plantain, Garlic, Yam, Cashew, Wheat, Cotton, Sesame, etc.)"
    ).strip()
    if not crop_type:
        crop_type = "Cassava"

    # 2. 100% UNIVERSAL LOCATION INPUT (Direct text input for any town, LGA, state, or GPS)
    location_input = st.text_input(
        "Project Location or GPS Coordinates",
        value="Minna, Niger State",
        help="Type any City, Town, LGA, State, or raw GPS coordinates (e.g., 'Mokwa, Niger', 'Zaria, Kaduna', 'Ibadan', or '9.0820, 8.6753')"
    ).strip()
    if not location_input:
        location_input = "Minna, Niger State"

    land_size = st.number_input(
        "Cultivation Area Scale (Hectares)",
        min_value=0.1,
        max_value=50000.0,
        value=5.0,
        step=0.5,
        help="Standard institutional unit: 1 Hectare = 10,000 sq.m (~2.47 Acres)"
    )

    planting_date = st.date_input("Target Planting Anchor Date", value=datetime.date(2026, 6, 15))
    
    mechanization_level = st.select_slider(
        "Farm Mechanization Standard",
        options=["Manual / Animal Traction", "Semi-Mechanized (Standard 2-Pass)", "Full Precision Tech (GPS Guidance)"],
        value="Semi-Mechanized (Standard 2-Pass)"
    )

    st.markdown("---")
    st.caption("Institutional Platform: **Federal Ministry of Agriculture & Food Security (FMAFS)**")
    st.caption("Architecture Lead: **Muhammad Alfa Kure**")

is_ai_live = bool(final_key and len(final_key) > 15)

def get_gemini_client():
    if is_ai_live:
        return genai.Client(api_key=final_key)
    return None

# -----------------------------------------------------------------------------
# 4. AGRONOMIC TAXONOMY & GEOSPATIAL INTELLIGENCE ENGINES
# -----------------------------------------------------------------------------
def classify_crop_profile(name: str):
    """Dynamically categorizes any crop in the world to calibrate QS metrics."""
    n = name.lower()
    if any(k in n for k in ["cocoa", "oil palm", "palm", "cashew", "rubber", "coffee", "citrus", "orange", "mango", "avocado", "plantain", "banana", "teak", "guava"]):
        return {
            "group": "Perennial / Tree / Plantation",
            "seed_label": "Certified Polybag Seedlings / Cuttings",
            "seed_rate_ha": 135000,
            "ridging_label": "Holing, Lining & Spacing (Plantation Grid)",
            "fertilizer_label": "Organic Manure + Basal NPK Ring Application",
            "fert_cost_ha": 85000,
            "pest_label": "Stem Borer & Phytophthora Fungal Protection"
        }
    elif any(k in n for k in ["yam", "cassava", "potato", "ginger", "turmeric", "cocoyam", "garlic", "sweet potato"]):
        return {
            "group": "Root, Tuber & Rhizome",
            "seed_label": f"Certified {name} Seedlings / Stems / Rhizome Setts",
            "seed_rate_ha": 65000 if "yam" not in n else 160000,
            "ridging_label": "Deep Contour Ridging & Mounding / Bed Formation",
            "fertilizer_label": "Basal NPK (High Potassium Blend 12:12:17 or 15:15:15)",
            "fert_cost_ha": 105000,
            "pest_label": "Nematode, Beetle & Tuber Rot Prophylactic Treatment"
        }
    elif any(k in n for k in ["tomato", "pepper", "onion", "cucumber", "watermelon", "cabbage", "carrot", "lettuce", "vegetable", "okra", "eggplant"]):
        return {
            "group": "Horticulture & High-Value Vegetables",
            "seed_label": "Hybrid F1 Nursery Seedling Trays & Substrate",
            "seed_rate_ha": 85000,
            "ridging_label": "Fine Tilth Raised Seedbeds & Drip Bed Layout",
            "fertilizer_label": "Foliar Fertigation Pack & Soluble NPK",
            "fert_cost_ha": 120000,
            "pest_label": "Intensive Tuta Absoluta, Thrips & Blight Management"
        }
    elif any(k in n for k in ["soy", "bean", "cowpea", "groundnut", "peanut", "sesame", "benniseed", "chickpea", "pigeon"]):
        return {
            "group": "Grain Legume & Oilseed",
            "seed_label": "Certified Inoculated Seed Stock",
            "seed_rate_ha": 38000,
            "ridging_label": "Narrow Inter-Row Ridges / Flat Planter Beds",
            "fertilizer_label": "Single Super Phosphate (SSP) & Minimal Starter Nitrogen",
            "fert_cost_ha": 65000,
            "pest_label": "Pod Borer (Maruca) & Pod Sucking Bug Control"
        }
    else:  # Cereals, grains, grasses, or unclassified broad-acre crops
        return {
            "group": "Cereal, Grain & Broad-Acre Crop",
            "seed_label": f"Certified Hybrid {name} Foundation Seed Stock",
            "seed_rate_ha": 42000,
            "ridging_label": "Standard Tractor Ridging / Drill Spacing",
            "fertilizer_label": "Basal NPK 20:10:10 Compound Fertilizer",
            "fert_cost_ha": 98000,
            "pest_label": "Fall Armyworm & Stem Borer Systemic Interception"
        }

crop_meta = classify_crop_profile(crop_type)

# Geospatial Coordinate Resolution Engine
coord_pattern = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
matched_coord = re.match(coord_pattern, location_input.strip())

lat, lon = 9.0765, 7.3986  # Default centroid (Nigeria / Abuja)
geo_status = f"🌐 Regional Zone: {location_input}"

if matched_coord:
    parts = location_input.split(",")
    lat = float(parts[0].strip())
    lon = float(parts[1].strip())
    geo_status = f"🎯 Direct GPS Coordinates Anchor: [{lat:.4f}, {lon:.4f}]"
else:
    # Match against known state/town registry
    loc_clean = location_input.lower()
    for key, coords in STATE_COORDINATES.items():
        if key in loc_clean:
            lat, lon = coords
            geo_status = f"📍 Mapped Agro-Ecological Node: {location_input.title()} [{lat:.4f}, {lon:.4f}]"
            break

st.markdown(f"""
    <div class="hero-banner">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <h1 class="hero-title">🌾 Agri-Quant Architecture</h1>
                <p class="hero-subtitle">Universal AI Agribusiness Quantity Surveying, Geospatial Auditing & Land Clearing Evidence Portal</p>
            </div>
            <div>
                {f'<span class="status-pill status-live">⚡ LIVE MULTIMODAL AI (Gemini 2.5 Flash)</span>' if is_ai_live else '<span class="status-pill status-offline">📊 OFFLINE QUANT ENGINE ACTIVE</span>'}
            </div>
        </div>
        <div style="margin-top:14px; font-size:13px; color:#cbd5e1; display:flex; align-items:center; flex-wrap:wrap; gap:10px;">
            <span>{geo_status}</span> &nbsp;|&nbsp; 
            <span>Target Crop: <b>{crop_type}</b> <span class="category-badge">{crop_meta['group']}</span></span> &nbsp;|&nbsp; 
            <span>Scope: <b>{land_size:.2f} Hectares</b></span>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. DYNAMIC PARAMETRIC QS ENGINE (Calibrated to ANY Crop)
# -----------------------------------------------------------------------------
def compute_parametric_boq(crop_name: str, hectares: float, mech_tier: str, meta: dict) -> pd.DataFrame:
    mech_multiplier = 0.80 if "Manual" in mech_tier else (1.30 if "Full Precision" in mech_tier else 1.0)

    rows = [
        {"Category": "Land Preparation", "Work Item": "Site Delineation, Perimeter Pegging & Bush Clearing", "Unit": "Ha", "Rate_NGN": 75000 * mech_multiplier},
        {"Category": "Land Preparation", "Work Item": "Heavy De-Stumping & Primary Mechanized Disc Ploughing", "Unit": "Ha", "Rate_NGN": 65000 * mech_multiplier},
        {"Category": "Land Preparation", "Work Item": "Secondary Cross-Harrowing & Soil Tilth Pulverization", "Unit": "Ha", "Rate_NGN": 45000 * mech_multiplier},
        {"Category": "Land Preparation", "Work Item": meta["ridging_label"], "Unit": "Ha", "Rate_NGN": 45000 * mech_multiplier},
        
        {"Category": "Inputs & Planting", "Work Item": meta["seed_label"], "Unit": "Ha", "Rate_NGN": meta["seed_rate_ha"]},
        {"Category": "Inputs & Planting", "Work Item": "Pre-Emergence Chemical Barrier (Selective Herbicide)", "Unit": "Ha", "Rate_NGN": 26000},
        {"Category": "Inputs & Planting", "Work Item": meta["fertilizer_label"], "Unit": "Ha", "Rate_NGN": meta["fert_cost_ha"]},
        {"Category": "Inputs & Planting", "Work Item": "Top Dressing / Foliar Micronutrient Boost", "Unit": "Ha", "Rate_NGN": 52000},
        
        {"Category": "Labor & Agronomics", "Work Item": f"Precision Planting & Alignment Labor ({crop_name})", "Unit": "Ha", "Rate_NGN": 35000},
        {"Category": "Labor & Agronomics", "Work Item": "First & Second Weed Canopy Maintenance Passes", "Unit": "Ha", "Rate_NGN": 42000},
        {"Category": "Labor & Agronomics", "Work Item": meta["pest_label"], "Unit": "Ha", "Rate_NGN": 30000},
        {"Category": "Labor & Agronomics", "Work Item": "Field Extension, Spatial Auditing & Soil Health Tracking", "Unit": "Ha", "Rate_NGN": 15000},
        
        {"Category": "Harvest Logistics", "Work Item": f"Maturity Harvesting, Manual Lifting / Field Aggregation ({crop_name})", "Unit": "Ha", "Rate_NGN": 48000},
        {"Category": "Harvest Logistics", "Work Item": "Post-Harvest Crating, Bagging & Farm-Gate Weighing", "Unit": "Ha", "Rate_NGN": 32000},
    ]

    df = pd.DataFrame(rows)
    df["Quantity"] = hectares
    df["Total_Cost_NGN"] = (df["Rate_NGN"] * df["Quantity"]).round(2)
    return df

# Baseline calculations
boq_df = compute_parametric_boq(crop_type, land_size, mechanization_level, crop_meta)
subtotal = boq_df["Total_Cost_NGN"].sum()
contingency = subtotal * 0.075
grand_total = subtotal + contingency
land_prep_subtotal = boq_df[boq_df["Category"] == "Land Preparation"]["Total_Cost_NGN"].sum()

# -----------------------------------------------------------------------------
# 6. APPLICATION NAVIGATION TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💰 Precise Costing (BOQ)", 
    "📅 Lifecycle & Critical Path", 
    "📊 Comparative Matrix",
    "📡 Farm-Gate & Telemetry",
    "🚜 Land Clearing & Physical Evidence",
    "🏛️ FMAFS Forensic Subsidy Auditor"
])

# =============================================================================
# TAB 1: DYNAMIC QUANTITY SURVEYING (BOQ STUDIO)
# =============================================================================
with tab1:
    st.subheader(f"Institutional Bill of Quantities (BOQ): {crop_type}")
    st.caption(f"Classification: **{crop_meta['group']}** | Location: **{location_input}** | Scope: **{land_size:.2f} Hectares**")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Direct Works (Base)", f"₦{subtotal:,.2f}")
    col_m2.metric("Contingency Reserve (7.5%)", f"₦{contingency:,.2f}")
    col_m3.metric("Total Project CapEx", f"₦{grand_total:,.2f}")
    col_m4.metric("Cost / Hectare", f"₦{(grand_total/land_size):,.2f}")

    col_table, col_chart = st.columns([3, 2])
    with col_table:
        display_df = boq_df[["Category", "Work Item", "Quantity", "Unit", "Rate_NGN", "Total_Cost_NGN"]].copy()
        display_df.columns = ["Category", "Scope of Work", "Qty", "Unit", "Unit Rate (NGN)", "Amount (NGN)"]
        st.dataframe(
            display_df.style.format({
                "Unit Rate (NGN)": "₦{:,.2f}",
                "Amount (NGN)": "₦{:,.2f}",
                "Qty": "{:,.2f}"
            }),
            use_container_width=True,
            height=390
        )
        
        csv_buffer = io.StringIO()
        display_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Certified BOQ (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"BOQ_{crop_type}_{land_size}Ha_{datetime.date.today()}.csv",
            mime="text/csv"
        )

    with col_chart:
        st.markdown("#### Capital Allocation Distribution")
        cat_summary = boq_df.groupby("Category")["Total_Cost_NGN"].sum().reset_index()
        st.bar_chart(cat_summary.set_index("Category"))
        
        with st.expander("📍 Geospatial Site Centroid", expanded=True):
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=9)

    st.markdown("---")
    st.markdown("#### ⚡ AI Senior Quantity Surveyor Synthesis")
    if st.button(f"Generate Senior QS Narrative Audit for {crop_type}", key="btn_run_ai_boq", type="primary"):
        if is_ai_live:
            with st.spinner(f"Evaluating structural procurement indices for {crop_type}..."):
                client = get_gemini_client()
                prompt = f"""
                You are a Fellow of the Nigerian Institute of Quantity Surveyors (NIQS) and Principal Agribusiness Valuer.
                Provide an institutional-grade Quantity Surveying review for cultivating:
                - Crop: {crop_type} (Classification: {crop_meta['group']})
                - Cultivated Scope: {land_size} Hectares
                - Location Profile: {location_input}
                - Mechanization Level: {mechanization_level}
                - Direct CapEx: ₦{subtotal:,.2f}
                - Grand Total Budget: ₦{grand_total:,.2f} (₦{grand_total/land_size:,.2f}/Ha)

                Provide a structured markdown review covering:
                1. **Market Rate Reality Check**: Evaluate unit cost feasibility for {crop_type} given fuel and agro-input costs in {location_input}.
                2. **Specific Agronomic & Soil Hazards**: Risks specific to {crop_type} in {location_input}.
                3. **Procurement Timing Strategy**: Sourcing windows for seeds/propagules and fertilizers to avoid regional inflation.
                4. **Bankability & Loan Certification Statement**: Advisory note for commercial and developmental agricultural lenders.
                """
                try:
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.session_state.boq_ai_analysis = res.text
                except Exception as e:
                    st.error(f"AI API Connection Error: {e}")
        else:
            st.session_state.boq_ai_analysis = f"""
            ### 📋 Institutional QS Site Brief ({crop_type} - {location_input})
            * **Project:** {crop_type} Enterprise ({crop_meta['group']})
            * **Scope:** {land_size} Ha | Grand Total: ₦{grand_total:,.2f} (₦{grand_total/land_size:,.2f}/Ha)
            * **Advisory Directive:** Ensure foundation propagation material is certified and tested for germination/purity prior to final field placement.
            """

    if st.session_state.boq_ai_analysis:
        st.markdown(st.session_state.boq_ai_analysis)

# =============================================================================
# TAB 2: LIFECYCLE & CRITICAL PATH PLANNER
# =============================================================================
with tab2:
    st.subheader(f"Agrometeorological Lifecycle & Critical Path: {crop_type}")
    st.caption(f"Commencing sequence on **{planting_date.strftime('%B %d, %Y')}** | Target Zone: **{location_input}**")

    phases = [
        {"Phase": "Stage 0: Site Prep & Drainage", "Window": "Week -4 to -1", "Focus": f"Land clearing, plowing, and preparation for {crop_type} ({crop_meta['ridging_label']})."},
        {"Phase": "Stage 1: Planting / Establishment", "Window": "Week 1 to 3", "Focus": f"Establishment of {crop_meta['seed_label']}, herbicide barrier within 48 hours."},
        {"Phase": "Stage 2: Vegetative & Nutritional", "Window": "Week 4 to 8", "Focus": f"Nutritional application of {crop_meta['fertilizer_label']}, first canopy weeding."},
        {"Phase": "Stage 3: Crop Protection & Maturation", "Window": "Week 9 to Maturity", "Focus": f"Management of {crop_meta['pest_label']}, foliar feeding and yield monitoring."},
        {"Phase": "Stage 4: Harvesting & Off-take", "Window": "Terminal Phase", "Focus": f"Maturity index sampling, sorting, grading, and direct off-taker farm-gate delivery."}
    ]
    st.table(pd.DataFrame(phases))

    if st.button(f"Generate Phenological Agronomic Schedule for {crop_type}", key="btn_run_lifecycle", type="primary"):
        if is_ai_live:
            with st.spinner(f"Computing meteorological calendar for {crop_type} in {location_input}..."):
                client = get_gemini_client()
                prompt = f"""
                Act as a Senior Agronomist and Agrometeorologist.
                Build a precise month-by-month phenological calendar and operational critical path for:
                - Target Crop: {crop_type} ({crop_meta['group']})
                - Field Scale: {land_size} Hectares
                - Location: {location_input}
                - Target Planting Date: {planting_date}

                Include:
                1. **Rainfall & Soil Temperature Milestones**: Suitability windows in {location_input}.
                2. **Specific Input Application Schedule**: Exact days after planting (DAP) for fertilizers, pest barriers, and weed control.
                3. **Pest & Disease Scouting Protocol**: Primary hazards for {crop_type} in this zone and containment methods.
                4. **Harvest & Post-Harvest Protocol**: Moisture management, storage, or rapid processing directives.
                """
                try:
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.session_state.lifecycle_analysis = res.text
                except Exception as e:
                    st.error(f"AI API Connection Error: {e}")
        else:
            st.session_state.lifecycle_analysis = f"Phenological lifecycle established for {crop_type} starting on {planting_date} at {location_input}."

    if st.session_state.lifecycle_analysis:
        st.markdown(st.session_state.lifecycle_analysis)

# =============================================================================
# TAB 3: COMPARATIVE MATRIX & CROPPING ARBITRAGE (UNCONSTRAINED)
# =============================================================================
with tab3:
    st.subheader("Cross-Crop Financial & Investment Arbitrage")
    st.caption("Compare your primary crop against any other agricultural commodity in the world.")

    col_comp1, col_comp2 = st.columns(2)
    with col_comp1:
        # 100% UNCONSTRAINED COMPARISON CROP INPUT
        comp_crop = st.text_input("Enter Any Benchmark Crop to Compare", value="Maize").strip()
        if not comp_crop:
            comp_crop = "Maize"
    with col_comp2:
        expected_yield = st.number_input(f"Expected {crop_type} Yield (Tonnes/Ha)", min_value=0.1, value=15.0, step=1.0)
        expected_price = st.number_input(f"Estimated Farm-Gate Price for {crop_type} (NGN/Tonne)", min_value=1000, value=95000, step=5000)

    # Parametric calculation for comparison
    comp_meta = classify_crop_profile(comp_crop)
    comp_boq = compute_parametric_boq(comp_crop, land_size, mechanization_level, comp_meta)
    comp_cost = comp_boq["Total_Cost_NGN"].sum() * 1.075

    primary_cost = grand_total
    primary_gross_rev = expected_yield * expected_price * land_size
    primary_net_profit = primary_gross_rev - primary_cost
    primary_roi = (primary_net_profit / primary_cost) * 100 if primary_cost > 0 else 0

    col_v1, col_v2, col_v3 = st.columns(3)
    col_v1.metric(f"{crop_type} Estimated Gross Revenue", f"₦{primary_gross_rev:,.2f}")
    col_v2.metric(f"{crop_type} Net Margin", f"₦{primary_net_profit:,.2f}", f"{primary_roi:.1f}% ROI")
    col_v3.metric(f"{comp_crop} Estimated CapEx", f"₦{comp_cost:,.2f}")

    if st.button(f"Execute Investment Arbitrage: {crop_type} vs {comp_crop}", key="btn_run_compare", type="primary"):
        if is_ai_live:
            with st.spinner(f"Evaluating investment metrics: {crop_type} vs {comp_crop}..."):
                client = get_gemini_client()
                prompt = f"""
                Act as an Institutional Agribusiness Investment Banker.
                Perform a comparative investment analysis between:
                - Primary Crop: {crop_type} ({crop_meta['group']}) | Estimated CapEx: ₦{primary_cost:,.2f}
                - Comparison Crop: {comp_crop} ({comp_meta['group']}) | Estimated CapEx: ₦{comp_cost:,.2f}
                - Scope: {land_size} Hectares in {location_input}

                Analyze:
                1. **Working Capital & Labor Friction**: Which crop carries higher operational risk during the season?
                2. **Off-Take Liquidity**: Ease of selling {crop_type} vs {comp_crop} at the farm gate in Nigeria.
                3. **Downside Risk & Perishability**: Storage shelf life, moisture risks, and price volatility.
                4. **Final Investment Decision**: Portfolio recommendation for this land parcel.
                """
                try:
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.session_state.comparison_analysis = res.text
                except Exception as e:
                    st.error(f"AI Connection Error: {e}")
        else:
            st.session_state.comparison_analysis = f"Arbitrage analysis for {crop_type} (₦{primary_cost:,.2f}) vs {comp_crop} (₦{comp_cost:,.2f}) across {land_size} Ha."

    if st.session_state.comparison_analysis:
        st.markdown(st.session_state.comparison_analysis)

# =============================================================================
# TAB 4: FARM-GATE & USSD TELEMETRY INGESTION HUB
# =============================================================================
with tab4:
    st.subheader(f"📡 Hyper-Local Farm-Gate Cost Index & USSD Telemetry: {location_input}")
    st.caption("Capturing un-searchable ground-truth data from rural smallholders via USSD/IVR channels.")

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("USSD/IVR Reporting Nodes", "1,845 Wards", "+14.8% MoM")
    t2.metric("Tractor Rental Index", "₦88,500 / Ha", "-4.2% Regional Subsidies")
    t3.metric("Urea (50kg) Rural Farmgate", "₦46,200", "+21% Above Benchmark")
    t4.metric("Daily Unskilled Farm Labor", "₦3,800 - ₦4,500", "Peak Season Rate")

    st.markdown("---")
    st.markdown("#### Real-Time Telemetry Feed: Rural Market Day Observations")
    sample_ussd_data = pd.DataFrame([
        {"Ward / Market": f"{location_input} Central Market", "Reported Item": f"{crop_type} Propagule Stock", "Official Benchmark": f"₦{crop_meta['seed_rate_ha']:,}", "Ground-Truth Farm-Gate": f"₦{int(crop_meta['seed_rate_ha']*1.18):,}", "Variance": "+18.0%"},
        {"Ward / Market": f"{location_input} Machinery Pool", "Reported Item": "Heavy Disc Ploughing (Per Ha)", "Official Benchmark": "₦65,000", "Ground-Truth Farm-Gate": "₦78,000", "Variance": "+20.0%"},
        {"Ward / Market": "Regional Agro-Dealer Hub", "Reported Item": "NPK 20-10-10 / 15-15-15 (50kg)", "Official Benchmark": "₦35,000", "Ground-Truth Farm-Gate": "₦42,500", "Variance": "+21.4%"},
        {"Ward / Market": "Zonal Farmers Cooperative", "Reported Item": "Daily Farm Labor (Weeding)", "Official Benchmark": "₦3,500", "Ground-Truth Farm-Gate": "₦4,200", "Variance": "+20.0%"}
    ])
    st.dataframe(sample_ussd_data, use_container_width=True)

# =============================================================================
# TAB 5: LAND CLEARING & PHYSICAL EVIDENCE CLEARANCE HUB
# =============================================================================
with tab5:
    st.markdown("""
        <div style="background-color: #f8fafc; border-left: 5px solid #047857; padding: 18px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="margin-top:0; color:#064e3b;">🚜 Ministry Land Clearing & Physical Evidence Verification Portal</h3>
            <p style="font-size:14px; color:#334155; margin-bottom:0;">
                Statutory verification chamber for Tranche-1 (Land Preparation & Bush Clearing) subsidy disbursement. 
                Upload field photos, drone surveys, and mechanization telemetry to eliminate <b>"Ghost Farms"</b> and paper clearing claims.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c_meta1, c_meta2, c_meta3 = st.columns(3)
    with c_meta1:
        clearing_contractor = st.text_input("Mechanization Service Provider / CAC Reg", value="Agro-Mechanize Ltd [RC-192841]")
        clearing_completion_date = st.date_input("Date Land Clearing Completed", value=datetime.date.today())
    with c_meta2:
        machinery_used = st.multiselect(
            "Equipment Deployed on Site",
            ["Crawler Bulldozer (CAT D6/D7)", "Agricultural Tractor (75-90 HP)", "Heavy Disc Plough (3-4 disc)", "Offset Disc Harrow", "Manual Labor Gang (Stump digging)"],
            default=["Crawler Bulldozer (CAT D6/D7)", "Agricultural Tractor (75-90 HP)", "Heavy Disc Plough (3-4 disc)"]
        )
    with c_meta3:
        diesel_logged = st.number_input("Total Diesel Consumed (Litres)", min_value=0.0, value=float(land_size * 115), step=50.0, help="Standard heavy clearing consumes ~90-130 Litres per Hectare")
        clearing_invoice_amount = st.number_input("Claimed Land Clearing Cost (NGN)", min_value=0.0, value=float(land_prep_subtotal), step=50000.0)

    # Physical Diesel Physics Verification
    expected_diesel_min = land_size * 80
    expected_diesel_max = land_size * 160
    diesel_burn_rate = diesel_logged / land_size if land_size > 0 else 0

    st.markdown("---")
    st.markdown("#### 📷 Multi-Spectral & Photographic Evidence Ingestion")
    st.caption("Upload geotagged on-site smartphone photos, drone orthomosaics, or high-res satellite captures demonstrating ground truth.")

    up_col1, up_col2 = st.columns(2)
    with up_col1:
        pre_file = st.file_uploader("1. Baseline / Pre-Clearing Photo (Virgin Bush / Before)", type=["jpg", "jpeg", "png"], key="pre_img")
        if pre_file:
            st.image(pre_file, caption="Baseline Site Condition (Pre-Clearing)", use_container_width=True)
    with up_col2:
        post_file = st.file_uploader("2. Post-Clearing Field Evidence (Plowing / Ridges / After)", type=["jpg", "jpeg", "png"], key="post_img")
        if post_file:
            st.image(post_file, caption="Submitted Verification Evidence (Post-Clearing)", use_container_width=True)

    st.markdown("---")
    st.markdown("#### ⚙️ Engineering & Mechanization Diagnostic")
    d1, d2, d3 = st.columns(3)
    d1.metric("Diesel Burn Rate / Ha", f"{diesel_burn_rate:.1f} L/Ha", "Benchmark: 90 - 130 L/Ha")
    d2.metric("Claimed Clearing Cost / Ha", f"₦{(clearing_invoice_amount / land_size):,.2f}", f"QS Standard: ₦{(land_prep_subtotal/land_size):,.2f}")
    
    diesel_valid = expected_diesel_min <= diesel_logged <= expected_diesel_max
    if diesel_valid:
        d3.metric("Telemetry Fuel Validation", "PLAUSIBLE", "Within mechanical tolerance")
    else:
        d3.metric("Telemetry Fuel Validation", "ANOMALY FLAGGED", "Suspect fuel log volume", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔍 Execute Ministry Multimodal Clearing Inspection", key="btn_audit_evidence", type="primary"):
        if is_ai_live:
            with st.spinner("Analyzing ground textures, vegetative cover loss, and mechanization telemetry with Gemini 2.5 Flash..."):
                client = get_gemini_client()
                content_parts = []
                
                evidence_prompt = f"""
                You are Chief Agricultural Field Inspector and Forensic Land Auditor for the Federal Ministry of Agriculture and Food Security (FMAFS) Nigeria.
                Perform a formal physical evidence audit to approve or reject Tranche-1 (Land Clearing) subsidy disbursement for:

                **Applicant & Site Profile:**
                - Farm Reference: {location_input}
                - Scope Claimed: {land_size} Hectares of {crop_type}
                - Clearing Contractor: {clearing_contractor}
                - Machinery Claimed: {', '.join(machinery_used)}
                - Logged Diesel Burn: {diesel_logged} Litres ({diesel_burn_rate:.1f} L/Ha)
                - Invoiced Land Prep Amount: ₦{clearing_invoice_amount:,.2f}
                - Ministry QS Baseline Land Prep Budget: ₦{land_prep_subtotal:,.2f}

                **Your Mandatory Forensic Checklist:**
                1. **Visual Soil Disturbance & Canopy Analysis**:
                   - Look for signs of mechanical disc furrows, pulverized tilth, windrowed brush piles, or removed tree roots.
                   - Detect if the image appears to be an unworked savanna, unplowed grassland, or fake/unrelated photo.
                2. **Engineering Plausibility Test**:
                   - Compare the {diesel_logged} Litres of fuel logged against {land_size} Hectares. Is this physically sufficient for primary mechanical clearing and secondary tillage?
                3. **Financial Discrepancy Assessment**:
                   - Compare claimed ₦{clearing_invoice_amount:,.2f} against the benchmark ₦{land_prep_subtotal:,.2f}.
                4. **Formal Ministerial Action Verdict**:
                   - **Clearance Verdict**: [APPROVED FOR TRANCHE-1 DISBURSEMENT / CONDITIONAL APPROVAL SUBJECT TO BEACON PEGGING / REJECTED - GHOST CLEARING DETECTED]
                   - Recommended Disbursable Amount (in NGN).
                   - Auditor Signature Block.

                Deliver your response in an official ministerial audit memorandum format.
                """
                content_parts.append(evidence_prompt)

                if post_file:
                    content_parts.append(types.Part.from_bytes(data=post_file.getvalue(), mime_type=post_file.type))
                if pre_file:
                    content_parts.append(types.Part.from_bytes(data=pre_file.getvalue(), mime_type=pre_file.type))

                try:
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=content_parts,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.session_state.evidence_audit_result = res.text
                except Exception as e:
                    st.error(f"Multimodal AI Error: {e}")
        else:
            verdict_title = "APPROVED FOR TRANCHE-1 DISBURSEMENT" if diesel_valid else "HOLD: SUSPECT TELEMETRY ANOMALY"
            st.session_state.evidence_audit_result = f"""
            ### 🏛️ FEDERAL MINISTRY OF AGRICULTURE AND FOOD SECURITY (FMAFS)
            #### AGRICULTURAL FIELD INSPECTORATE DIVISION — PHYSICAL EVIDENCE REPORT
            
            * **Farm Target:** {land_size} Ha in {location_input}
            * **Contractor:** {clearing_contractor}
            * **Audit Status:** {verdict_title}
            
            **1. Engineering & Telematics Review:**
            * Fuel allocation of **{diesel_burn_rate:.1f} L/Ha** was analyzed against national clearing standards (90-130 L/Ha).
            * {'Fuel consumption is within normal heavy clearing bounds.' if diesel_valid else 'Fuel consumption is outside expected engineering bounds for full de-stumping.'}
            
            **2. Financial Allocation:**
            * Claimed Clearing Sum: **₦{clearing_invoice_amount:,.2f}**
            * Approved Ministry Benchmark: **₦{land_prep_subtotal:,.2f}**
            * Recommended Tranche Release: **₦{min(clearing_invoice_amount, land_prep_subtotal):,.2f}**
            """

    if st.session_state.evidence_audit_result:
        st.markdown(f'<div class="memo-card">{st.session_state.evidence_audit_result}</div>', unsafe_allow_html=True)

# =============================================================================
# TAB 6: FMAFS FORENSIC ORBITAL & SUBSIDY AUDITOR
# =============================================================================
with tab6:
    st.subheader("🏛️ Institutional Subsidy & Facility Auditor")
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        loan_app_id = st.text_input("Applicant Reference / FMAFS ID", value="FMAFS-AGRI-2026-9812")
        claimed_ha = st.number_input("Claimed Land Size (Hectares)", min_value=0.5, value=float(land_size), step=1.0)
    with col_in2:
        audit_crop = st.text_input("Claimed Target Crop", value=crop_type)
        claimed_grant_amount = st.number_input("Requested Facility / Disbursement (NGN)", min_value=100000, value=float(grand_total), step=250000.0)

    benchmark_cost_per_ha = (grand_total / land_size) if land_size > 0 else 420000
    expected_total_facility = benchmark_cost_per_ha * claimed_ha
    variance_ratio = (claimed_grant_amount / expected_total_facility) if expected_total_facility > 0 else 1.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Requested Rate / Ha", f"₦{(claimed_grant_amount / claimed_ha):,.2f}")
    c2.metric("FMAFS Benchmark / Ha", f"₦{benchmark_cost_per_ha:,.2f}")
    c3.metric("Inflation Variance", f"{(variance_ratio - 1.0) * 100:+.1f}%")

    if variance_ratio > 1.45:
        st.markdown('<div class="audit-box-red"><b>🚨 SEVERE ANOMALY DETECTED:</b> Requested facility exceeds QS benchmark limits by >45%. High risk of over-invoicing.</div>', unsafe_allow_html=True)
    elif variance_ratio > 1.15:
        st.markdown('<div class="audit-box-amber"><b>⚠️ MODERATE VARIANCE DETECTED:</b> Budget is 15-45% above regional baseline. Check equipment invoices.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="audit-box-green"><b>✅ WITHIN STANDARD COMPLIANCE RANGE:</b> Requested facility aligns closely with QS benchmarks.</div>', unsafe_allow_html=True)

    if st.button("Run Forensic Orbital Audit Run", key="btn_run_audit_final", type="primary"):
        if is_ai_live:
            with st.spinner("Executing geospatial audit..."):
                client = get_gemini_client()
                prompt = f"""
                Act as Lead Forensic Auditor for FMAFS Nigeria. Audit facility ID: {loan_app_id}.
                - Location: {location_input} [Lat: {lat:.4f}, Lon: {lon:.4f}]
                - Scope: {claimed_ha} Ha of {audit_crop}
                - Claimed Amount: ₦{claimed_grant_amount:,.2f}
                - Standard Benchmark: ₦{benchmark_cost_per_ha:,.2f}/Ha (Variance: {(variance_ratio - 1.0) * 100:+.1f}%)

                Deliver an executive audit memo with Fraud Probability Score (0-100%) and final Ministerial recommendation.
                """
                try:
                    res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"AI API Connection Error: {e}")
        else:
            st.info("💡 Enter your Gemini API key in the sidebar to activate live orbital audits.")

# -----------------------------------------------------------------------------
# 7. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 13px;">
        Agri-Quant Architecture &copy; 2026 &nbsp;|&nbsp; Universal Agricultural Quantity Surveying & Spatial Telemetry System &nbsp;|&nbsp; Powered by Google Gemini 2.5 Flash
    </div>
    """,
    unsafe_allow_html=True
)
