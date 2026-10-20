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
    page_title="Agri-Quant | Geospatial AI, BOQ & Land Clearing Evidence Portal",
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

KNOWN_COORDINATES = {
    "Minna, Niger State": (9.6139, 6.5569),
    "Ibadan, Oyo State": (7.3775, 3.9470),
    "Makurdi, Benue State": (7.7322, 8.5391),
    "Kano, Kano State": (12.0022, 8.5920),
    "Abeokuta, Ogun State": (7.1475, 3.3619),
    "Enugu, Enugu State": (6.4584, 7.5464),
    "Kaduna, Kaduna State": (10.5105, 7.4165),
    "Zaria, Kaduna State": (11.0855, 7.7199),
    "Asaba, Delta State": (6.1989, 6.7337),
    "Lafia, Nasarawa State": (8.4938, 8.5153),
}

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & AUTHENTICATION
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
    
    crop_options = ["Cassava", "Maize (Corn)", "Soybeans", "Rice (Paddy)", "Sorghum", "Yam", "Oil Palm", "Sesame", "Cowpea (Beans)", "Custom Crop"]
    crop_selection = st.selectbox("Primary Cultivation Crop", crop_options, index=0)
    
    if crop_selection == "Custom Crop":
        crop_type = st.text_input("Specify Crop Name", value="Ginger")
    else:
        crop_type = crop_selection

    land_size = st.number_input(
        "Cultivation Area Scale (Hectares)",
        min_value=0.25,
        max_value=10000.0,
        value=5.0,
        step=0.5,
        help="Standard institutional unit: 1 Hectare = 10,000 sq.m (~2.47 Acres)"
    )

    location_choice = st.selectbox(
        "Agro-Ecological Hub / State",
        options=list(KNOWN_COORDINATES.keys()) + ["Custom Location / GPS"]
    )

    if location_choice == "Custom Location / GPS":
        location_input = st.text_input("Enter Address or Coordinates (lat, lon)", value="9.0820, 8.6753")
    else:
        location_input = location_choice

    planting_date = st.date_input("Target Planting Anchor Date", value=datetime.date(2026, 6, 15))
    mechanization_level = st.select_slider(
        "Farm Mechanization Standard",
        options=["Semi-Manual (Ox/Hand Labor)", "Standard Mechanized (2-Pass)", "Full Precision Tech (GPS Guidance)"],
        value="Standard Mechanized (2-Pass)"
    )

    st.markdown("---")
    st.caption("Designed for: **Federal Ministry of Agriculture & Food Security (FMAFS)**")
    st.caption("Architecture Lead: **Muhammad Alfa Kure**")

is_ai_live = bool(final_key and len(final_key) > 15)

def get_gemini_client():
    if is_ai_live:
        return genai.Client(api_key=final_key)
    return None

# -----------------------------------------------------------------------------
# 4. TOP HERO BAR & GEOSPATIAL RESOLUTION
# -----------------------------------------------------------------------------
coord_pattern = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
matched_coord = re.match(coord_pattern, location_input.strip())

if matched_coord:
    lat = float(location_input.split(",")[0].strip())
    lon = float(location_input.split(",")[1].strip())
    geo_status = f"🎯 Direct GPS Coordinates Anchor: [{lat:.4f}, {lon:.4f}]"
elif location_input in KNOWN_COORDINATES:
    lat, lon = KNOWN_COORDINATES[location_input]
    geo_status = f"📍 Regional Anchor: {location_input} [Centroid: {lat:.4f}, {lon:.4f}]"
else:
    lat, lon = 9.0820, 8.6753
    geo_status = f"🌐 Custom Boundary Reference: {location_input}"

st.markdown(f"""
    <div class="hero-banner">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
                <h1 class="hero-title">🌾 Agri-Quant Architecture</h1>
                <p class="hero-subtitle">Institutional Quantity Surveying, Geospatial Auditing & Land Clearing Evidence Clearance Portal</p>
            </div>
            <div>
                {f'<span class="status-pill status-live">⚡ LIVE MULTIMODAL AI (Gemini 2.5 Flash)</span>' if is_ai_live else '<span class="status-pill status-offline">📊 OFFLINE QUANT ENGINE ACTIVE</span>'}
            </div>
        </div>
        <div style="margin-top:14px; font-size:13px; color:#cbd5e1; display:flex; align-items:center; gap:8px;">
            <span>{geo_status}</span> &nbsp;|&nbsp; <span>Scope: <b>{land_size:.2f} Hectares</b></span> &nbsp;|&nbsp; <span>Target Crop: <b>{crop_type}</b></span>
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. PARAMETRIC QS ENGINE
# -----------------------------------------------------------------------------
def compute_parametric_boq(crop: str, hectares: float, mech_tier: str) -> pd.DataFrame:
    mech_multiplier = 0.85 if "Semi-Manual" in mech_tier else (1.35 if "Full Precision" in mech_tier else 1.0)

    crop_seed_rate_ha = {
        "Cassava": 45000, "Maize (Corn)": 38000, "Soybeans": 42000,
        "Rice (Paddy)": 50000, "Yam": 140000, "Oil Palm": 120000,
        "Sorghum": 28000, "Sesame": 30000, "Cowpea (Beans)": 35000
    }.get(crop, 40000)

    rows = [
        {"Category": "Land Preparation", "Work Item": "Site Delineation, Perimeter Pegging & Bush Clearing", "Unit": "Ha", "Rate_NGN": 75000 * mech_multiplier},
        {"Category": "Land Preparation", "Work Item": "Heavy De-Stumping & Primary Mechanized Disc Ploughing", "Unit": "Ha", "Rate_NGN": 65000 * mech_multiplier},
        {"Category": "Land Preparation", "Work Item": "Secondary Cross-Harrowing & Soil Tilth Pulverization", "Unit": "Ha", "Rate_NGN": 45000 * mech_multiplier},
        {"Category": "Land Preparation", "Work Item": "Mechanical Ridging & Contour Bed Formation", "Unit": "Ha", "Rate_NGN": 40000 * mech_multiplier},
        {"Category": "Inputs & Planting", "Work Item": f"Certified Seed / Stem Stock ({crop} Foundation Material)", "Unit": "Ha", "Rate_NGN": crop_seed_rate_ha},
        {"Category": "Inputs & Planting", "Work Item": "Pre-Emergence Chemical Barrier (Selective Herbicide)", "Unit": "Ha", "Rate_NGN": 24000},
        {"Category": "Inputs & Planting", "Work Item": "Basal Inorganic Fertilizer (NPK Blend)", "Unit": "Ha", "Rate_NGN": 98000},
        {"Category": "Inputs & Planting", "Work Item": "Post-Planting Top Dressing (Granular Urea / Bio-Stimulant)", "Unit": "Ha", "Rate_NGN": 52000},
        {"Category": "Labor & Agronomics", "Work Item": "Precision Planting Labor (Spacing & Density Compliance)", "Unit": "Ha", "Rate_NGN": 35000},
        {"Category": "Labor & Agronomics", "Work Item": "First & Second Hand-Weeding / Canopy Maintenance", "Unit": "Ha", "Rate_NGN": 40000},
        {"Category": "Labor & Agronomics", "Work Item": "Integrated Pest Management (IPM) & Foliar Fungicide", "Unit": "Ha", "Rate_NGN": 28000},
        {"Category": "Labor & Agronomics", "Work Item": "Agricultural Extension, Spatial Tracking & Soil Sampling", "Unit": "Ha", "Rate_NGN": 15000},
        {"Category": "Harvest Logistics", "Work Item": "Field Harvest, Aggregation Labor & Farm-Gate Weighing", "Unit": "Ha", "Rate_NGN": 45000},
        {"Category": "Harvest Logistics", "Work Item": "Post-Harvest Bagging, Crating & Short-Haul Transit", "Unit": "Ha", "Rate_NGN": 30000},
    ]

    df = pd.DataFrame(rows)
    df["Quantity"] = hectares
    df["Total_Cost_NGN"] = (df["Rate_NGN"] * df["Quantity"]).round(2)
    return df

# Baseline calculations
boq_df = compute_parametric_boq(crop_type, land_size, mechanization_level)
subtotal = boq_df["Total_Cost_NGN"].sum()
contingency = subtotal * 0.075
grand_total = subtotal + contingency

# Land prep specific subtotal for validation
land_prep_subtotal = boq_df[boq_df["Category"] == "Land Preparation"]["Total_Cost_NGN"].sum()

# -----------------------------------------------------------------------------
# 6. APPLICATION NAVIGATION TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💰 Precise Costing (BOQ)", 
    "📅 Lifecycle & Critical Path", 
    "📊 Comparative Matrix",
    "📡 Farm-Gate & Telemetry",
    "🚜 Land Clearing & Physical Evidence",  # <-- NEW MINISTRY EVIDENCE HUB
    "🏛️ FMAFS Forensic Subsidy Auditor"
])

# =============================================================================
# TAB 1: DYNAMIC QUANTITY SURVEYING (BOQ STUDIO)
# =============================================================================
with tab1:
    st.subheader(f"Institutional Bill of Quantities (BOQ): {crop_type}")
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
            height=380
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
        
        with st.expander("📍 Geospatial Farmland Visualizer", expanded=True):
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=9)

# =============================================================================
# TAB 2: LIFECYCLE & CRITICAL PATH PLANNER
# =============================================================================
with tab2:
    st.subheader(f"Agrometeorological Lifecycle & Critical Path: {crop_type}")
    phases = [
        {"Phase": "Stage 0: Pre-Planting", "Days": "Day -30 to -1", "Focus": "Soil sampling, heavy clearing, destumping, lime conditioning & drainage."},
        {"Phase": "Stage 1: Establishment", "Days": "Day 0 to +21", "Focus": f"Certified {crop_type} planting, pre-emergence herbicide barrier within 48h."},
        {"Phase": "Stage 2: Vegetative Growth", "Days": "Day 22 to +60", "Focus": "First split-dose NPK application, gap filling, manual rogueing."},
        {"Phase": "Stage 3: Reproductive / Bulking", "Days": "Day 61 to +120", "Focus": "Top-dressing with Urea/MOP, scouting for armyworms, mid-season moisture audit."},
        {"Phase": "Stage 4: Maturation & Harvest", "Days": "Day 121 to Terminal", "Focus": "Maturity dry-matter testing, mechanized harvesting, bagging & aggregation."}
    ]
    st.table(pd.DataFrame(phases))

# =============================================================================
# TAB 3: COMPARATIVE MATRIX & CROPPING ARBITRAGE
# =============================================================================
with tab3:
    st.subheader("Cross-Crop Financial & Investment Arbitrage")
    comp_crop = st.selectbox("Benchmark Alternate Crop", [c for c in crop_options if c != crop_type and c != "Custom Crop"], index=0)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        expected_yield = st.number_input(f"Expected {crop_type} Yield (Tonnes/Ha)", value=18.0, step=1.0)
    with col_c2:
        expected_price = st.number_input(f"Farm-Gate Price for {crop_type} (NGN/Tonne)", value=95000, step=5000)

    primary_cost = grand_total
    comp_boq = compute_parametric_boq(comp_crop, land_size, mechanization_level)
    comp_cost = comp_boq["Total_Cost_NGN"].sum() * 1.075

    primary_gross_rev = expected_yield * expected_price * land_size
    primary_net_profit = primary_gross_rev - primary_cost
    primary_roi = (primary_net_profit / primary_cost) * 100 if primary_cost > 0 else 0

    col_v1, col_v2, col_v3 = st.columns(3)
    col_v1.metric(f"{crop_type} Gross Revenue", f"₦{primary_gross_rev:,.2f}")
    col_v2.metric(f"{crop_type} Net Margin", f"₦{primary_net_profit:,.2f}", f"{primary_roi:.1f}% ROI")
    col_v3.metric(f"{comp_crop} Estimated CapEx", f"₦{comp_cost:,.2f}")

# =============================================================================
# TAB 4: FARM-GATE & USSD TELEMETRY INGESTION HUB
# =============================================================================
with tab4:
    st.subheader("📡 Hyper-Local Farm-Gate Cost Index & USSD Telemetry")
    sample_ussd_data = pd.DataFrame([
        {"Ward / Market": "Mokwa Central Market", "State": "Niger", "Reported Item": "Disc Ploughing (Per Ha)", "Official Gov Rate": 55000, "Ground-Truth Farm-Gate": 68000, "Discrepancy": "+23.6%"},
        {"Ward / Market": "Bodija Grain Hub", "State": "Oyo", "Reported Item": "NPK 20-10-10 (50kg)", "Official Gov Rate": 32000, "Ground-Truth Farm-Gate": 41500, "Discrepancy": "+29.7%"},
        {"Ward / Market": "Dawanau International", "State": "Kano", "Reported Item": "Maize Seed (10kg)", "Official Gov Rate": 18000, "Ground-Truth Farm-Gate": 21000, "Discrepancy": "+16.6%"},
        {"Ward / Market": "Gboko Agri-Market", "State": "Benue", "Reported Item": "Cassava Stems (50 Bundles)", "Official Gov Rate": 35000, "Ground-Truth Farm-Gate": 48000, "Discrepancy": "+37.1%"},
    ])
    st.dataframe(sample_ussd_data, use_container_width=True)

# =============================================================================
# TAB 5: LAND CLEARING & PHYSICAL EVIDENCE CLEARANCE HUB (NEW)
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
        diesel_logged = st.number_input("Total Diesel Consumed (Litres)", min_value=0.0, value=float(land_size * 115), step=50.0, help="Standard heavy clearing in Nigeria consumes 90-130 Litres per Hectare")
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
    
    # Pre-Audit Diesel Telematics Diagnostic
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
                
                # Prepare multimodal content parts
                content_parts = []
                
                evidence_prompt = f"""
                You are the Chief Agricultural Field Inspector and Forensic Land Auditor for the Federal Ministry of Agriculture and Food Security (FMAFS) Nigeria.
                Perform a formal physical evidence audit to approve or reject the Tranche-1 (Land Clearing) subsidy disbursement for this farm:

                **Applicant & Site Profile:**
                - Farm Reference: {location_input}
                - Scope Claimed: {land_size} Hectares of {crop_type}
                - Clearing Contractor: {clearing_contractor}
                - Machinery Claimed: {', '.join(machinery_used)}
                - Logged Diesel Burn: {diesel_logged} Litres ({diesel_burn_rate:.1f} L/Ha)
                - Invoiced Land Prep Amount: ₦{clearing_invoice_amount:,.2f}
                - Ministry QS Baseline Land Prep Budget: ₦{land_prep_subtotal:,.2f}

                **Images Attached:**
                {"- Both Pre-clearing and Post-clearing images provided." if (pre_file and post_file) else ("- Post-clearing image provided." if post_file else "- No direct photographic images attached (performing telemetry & documentary audit).")}

                **Your Mandatory Forensic Checklist:**
                1. **Visual Soil Disturbance & Canopy Analysis**:
                   - Look for signs of mechanical disc furrows, pulverized tilth, windrowed brush piles, or removed tree roots.
                   - Detect if the image appears to be an unworked savanna, unplowed grassland, or fake/unrelated photo.
                2. **Engineering Plausibility Test**:
                   - Compare the {diesel_logged} Litres of fuel logged against the {land_size} Hectares claimed. Is this physically sufficient for primary mechanical clearing and secondary tillage?
                3. **Financial Discrepancy Assessment**:
                   - Compare claimed ₦{clearing_invoice_amount:,.2f} against the benchmark ₦{land_prep_subtotal:,.2f}.
                4. **Formal Ministerial Action Verdict**:
                   - **Clearance Verdict**: [APPROVED FOR TRANCHE-1 DISBURSEMENT / CONDITIONAL APPROVAL SUBJECT TO BEACON PEGGING / REJECTED - GHOST CLEARING DETECTED]
                   - Recommended Disbursable Amount (in NGN).
                   - Auditor Signature Block.

                Deliver your response in an official ministerial audit memorandum format.
                """
                
                content_parts.append(evidence_prompt)

                # Attach uploaded images directly to Gemini multimodal context
                if post_file:
                    post_img_bytes = post_file.getvalue()
                    content_parts.append(types.Part.from_bytes(data=post_img_bytes, mime_type=post_file.type))
                if pre_file:
                    pre_img_bytes = pre_file.getvalue()
                    content_parts.append(types.Part.from_bytes(data=pre_img_bytes, mime_type=pre_file.type))

                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=content_parts,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.session_state.evidence_audit_result = response.text
                except Exception as e:
                    st.error(f"Multimodal AI Error: {e}")
        else:
            # Deterministic Fallback Report
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
            
            *(Note: Provide Gemini API Key to enable AI computer-vision photo inspection).*
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
        claimed_ha = st.number_input("Claimed Land Size (Hectares)", min_value=0.5, value=15.0, step=1.0)
    with col_in2:
        audit_crop = st.text_input("Claimed Target Crop", value=crop_type)
        claimed_grant_amount = st.number_input("Requested Facility / Disbursement (NGN)", min_value=100000, value=8500000, step=250000)

    benchmark_cost_per_ha = 420000
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
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.markdown(response.text)
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
        Agri-Quant Architecture &copy; 2026 &nbsp;|&nbsp; Certified Agricultural Quantity Surveying & Spatial Telemetry System &nbsp;|&nbsp; Powered by Google Gemini 2.5 Flash
    </div>
    """,
    unsafe_allow_html=True
)
