import streamlit as st
import db
import excel_generator
from openpyxl import load_workbook
import os

def main():
    st.markdown("## 🔍 PREVIEW SAVED PROGRAM OF WORK (POW)")
    st.markdown("---")

    # --- Humila ng Listahan ng Proyekto mula sa Database ---
    try:
        # Ginamit ang orihinal mong db function
        projects = db.get_project_list() 
    except Exception as e:
        st.error(f"❌ Error sa pag-load ng mga proyekto: {e}")
        return

    if not projects:
        st.info("💡 Walang mahanap na proyekto sa database. Magdagdag muna ng POW.")
        return

    # --- KALIWA AT KANAN SPLIT VIA STREAMLIT COLUMNS ---
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("### 🏢 List of Projects")
        
        # Gumawa ng malinis na diksyunaryo para sa selectbox selection
        # Format ng `proj`: (pow_id, project_name, location) batay sa query mo
        project_options = {f"📌 {p[1]} (ID: {p[0]})": p for p in projects}
        selected_key = st.selectbox("Pumili ng Proyekto:", list(project_options.keys()))
        
        selected_project_data = project_options[selected_key]
        current_pow_id = selected_project_data[0]
        current_project_name = selected_project_data[1]
        current_location = selected_project_data[2]

        st.markdown(f"**📍 Location:** `{current_location}`")
        st.markdown("---")

        # 🗑️ ACTION: DELETE ENTIRE POW
        st.markdown("#### 🚨 Danger Zone")
        with st.popover("❌ Delete Entire POW", use_container_width=True):
            st.warning(f"Sigurado ka bang buburahin ang buong proyektong: **{current_project_name}**? Hindi na ito mababawi.")
            if st.button("Oo, Burahin na", type="primary", use_container_width=True):
                if db.delete_pow_from_sql(current_pow_id):
                    st.success("Matagumpay na nabura ang buong POW record!")
                    st.rerun()
                else:
                    st.error("May error sa pagbura ng record.")

    with col_right:
        st.markdown(f"### 📋 Item List: *{current_project_name}*")
        
        # Humila ng aytem batay sa napiling ID
        associated_items = db.get_items_by_project(current_pow_id)
        
        if not associated_items:
            st.info("Walang mga aytem na nakita sa loob ng proyektong ito.")
            grand_total = 0.0
        else:
            # I-format ang data para sa magandang Web Table Display
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
                    "Unit Price": f"P {price:,.2f}",
                    "Total Price": f"P {total:,.2f}"
                })
            
            # Ipakita ang interactive dataframe/table sa web
            st.dataframe(table_data, use_container_width=True, hide_index=True)

        # 💰 SUMMARY COST BAR
        st.info(f"### 💰 PROJECT TOTAL COST: **P {grand_total:,.2f}**")

    st.markdown("---")

    # --- LOWER LEVEL TABS: ACTIONS (PREVIEW & EDIT) ---
    tab_preview, tab_edit = st.tabs(["👁️ Print & Excel Preview Layout", "✏️ Edit POW Record Mode"])

    with tab_preview:
        # Tinatawag ang web layout preview engine natin sa excel_generator.py!
        excel_generator.show_excel_preview_streamlit(current_pow_id)

    with tab_edit:
        st.markdown("### ✏️ Update POW Details")
        
        # Form fields para sa Project Metadata
        new_name = st.text_input("Project Title / Name:", value=current_project_name)
        new_loc = st.text_
