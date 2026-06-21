import streamlit as st
import pandas as pd
import db  # Naka-link sa iyong db.py module
import os
import subprocess
from openpyxl import load_workbook

# Import natin ang nakaraang module para sa Excel Downloader Engine
import preview_module  

def render_preview_pow_module():
    st.markdown("## 📋 PREVIEW SAVED PROGRAM OF WORK (POW)")
    st.caption("Pamahalaan, i-edit, o burahin ang mga naka-save na structural projects sa database system.")

    # SIGURADUHING MAY STATE TRACKING SA MGA INPUT ROWS
    if "editing_pow_id" not in st.session_state:
        st.session_state.editing_pow_id = None

    # ==========================================================================
    # KALIWA/ITAAS: PROJECT SELECTOR & ACTION GATEWAY
    # ==========================================================================
    projects = db.get_project_list()
    
    if not projects:
        st.info("🗹 Walang mahanap na aktibong proyekto sa database. Gumawa muna ng bago.")
        return

    # I-map ang projects para sa malinis na interface array
    project_options = {f"ID: {p[0]} | {p[1]}": {"id": p[0], "name": p[1], "location": p[2]} for p in projects}
    selected_label = st.selectbox("🎯 Pumili ng Proyekto sa Listahan:", options=list(project_options.keys()))
    
    current_proj = project_options[selected_label]
    pow_id = current_proj["id"]
    project_name = current_proj["name"]
    location = current_proj["location"]

    # Ipakita ang aktibong Lokasyon
    st.markdown(f"**📍 Lokasyon:** `{location}`")

    # ==========================================================================
    # KANAN: ITEMS DISPLAY LIST TABLE
    # ==========================================================================
    associated_items = db.get_items_by_project(pow_id)
    
    table_data = []
    grand_total = 0.0
    
    for idx, item in enumerate(associated_items, start=1):
        qty = float(item[0])
        unit = item[1]
        name = item[2]
        price = float(item[3])
        total = qty * price
        grand_total += total
        
        table_data.append({
            "#": idx,
            "Qty": qty,
            "Unit": unit,
            "Item Description": name,
            "Unit Price (₱)": price,
            "Total Price (₱)": total
        })

    # I-render bilang malinis na DataFrame
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(
            df.style.format({"Qty": "{:.2f}", "Unit Price (₱)": "{:,.2f}", "Total Price (₱)": "{:,.2f}"}),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("⚠️ Walang laman na mga aytem ang proyektong ito.")

    # 💰 SUMMARY BAR CONTROLLER
    st.metric(label="PROJECT TOTAL COST", value=f"₱ {grand_total:,.2f}")

    # ==========================================================================
    # BOTTOM ACTION CONTROL BOARD PANELS
    # ==========================================================================
    col1, col2, col3 = st.columns(3)

    with col1:
        # Paggamit ng functional script mula sa kabilang sheet module file natin kanina
        if st.button("👁️ Open Layout Preview & Download Suite", use_container_width=True, type="primary"):
            st.info("I-on ang module tab sa ibaba para makita ang Print Preview form.")
            # Trigger switcher pattern logic
            st.session_state.page_view_mode = "print_preview" 

    with col2:
        if st.button("✏️ Edit POW Record / Update Items", use_container_width=True):
            st.session_state.editing_pow_id = pow_id
            trigger_edit_modal_dialog(pow_id, project_name, location, associated_items)

    with col3:
        if st.button("❌ Delete Entire POW", use_container_width=True, type="secondary"):
            # Gumamit ng session state toggle para sa delete safety verification trigger guard
            st.session_state.confirm_delete_id = pow_id

    # CONTROL FOR SEPARATE TRIGGER CONFIRMATION SYSTEM
    if "confirm_delete_id" in st.session_state and st.session_state.confirm_delete_id == pow_id:
        st.error(f"⚠️ **KUMPIRMASYON:** Sigurado ka bang buburahin ang buong proyekto: **{project_name}**? Hindi na ito mababawi.")
        c_del1, c_del2 = st.columns(2)
        with c_del1:
            if st.button("Oo, Burahin ang Lahat", type="primary", use_container_width=True):
                if db.delete_pow_from_sql(pow_id):
                    st.success("Matagumpay na nabura ang buong POW record.")
                    del st.session_state.confirm_delete_id
                    st.rerun()
        with c_del2:
            if st.button("I-cancel", use_container_width=True):
                del st.session_state.confirm_delete_id
                st.rerun()

# ==============================================================================
# SUB-MODULE DIALOG: POPUP EDIT MODE SYSTEM (openpyxl & SQL SYNC)
# ==============================================================================
@st.dialog("✏️ EDIT MODE - Update POW Record & Sync Pipelines", width="large")
def trigger_edit_modal_dialog(pow_id, current_name, current_location, associated_items):
    """Pumapalit sa Toplevel modal frame engine ng Tkinter UI window block."""
    
    st.markdown("### 🏢 Details of POW")
    new_name = st.text_input("Project Title / Name:", value=current_name)
    new_loc = st.text_input("Project Location:",
