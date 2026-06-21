import streamlit as st
from openpyxl import load_workbook
import db  # Konektado sa corrected db.py layer mo

def main():
    st.markdown("### ➕ Create Program of Work (POW)")
    st.markdown("---")

    # --- STATE MANAGEMENT (Katumbas ng self.temporary_items sa Tkinter) ---
    if 'temporary_items' not in st.session_state:
        st.session_state.temporary_items = []

    # --- ITEM ENTRY FORM (Katumbas ng Form Frame at Entry Bindings) ---
    st.markdown("#### 📋 Item Entry (Max 150 Items)")
    
    col1, col2, col3, col4 = st.columns([1, 1, 3, 2])
    
    with col1:
        qty_input = st.number_input("Qty:", min_value=0, value=0, step=1, key="add_qty")
    with col2:
        unit_input = st.selectbox("Unit:", ["pc", "gal", "lit", "tin", "box", "bag", "cu.m"], index=0, key="add_unit")
    with col3:
        search_query = st.text_input("Item Name (Type to search):", key="search_item_name").strip()
    with col4:
        price_input = st.number_input("Unit Price (₱):", min_value=0.0, value=0.00, step=1.0, format="%.2f", key="add_price")

    # --- SMART SEARCH DROPDOWN SIMULATION ---
    selected_name = search_query
    if search_query:
        matched_results = db.search_master_items(search_query)
        if matched_results:
            options_list = [f"{item[0]} ({item[1]}) - ₱{float(item[2]):,.2f}" for item in matched_results[:10]]
            chosen_match = st.selectbox("💡 May mga tugmang aytem sa Database. Pumili kung nais gamitin:", ["-- Gumawa ng Bagong Detalye --"] + options_list)
            
            if chosen_match != "-- Gumawa ng Bagong Detalye --":
                match_index = options_list.index(chosen_match)
                selected_name = matched_results[match_index][0]
                st.info(f"✨ Napili: **{selected_name}** | Unit sa DB: `{matched_results[match_index][1]}` | Presyo: `₱{float(matched_results[match_index][2]):,.2f}`")
        else:
            st.warning(f"🔍 Ang '{search_query}' ay wala pa sa iyong database. Kapag idinagdag, awtomatiko itong marerehistro bilang bagong aytem.")

  # --- BUTTON: ADD TO LIST FUNCTION ---
    if st.button("➕ Add to List", type="secondary", width="stretch"):
        if len(st.session_state.temporary_items) >= 150:
            st.error("⚠️ Limit Reached: Hanggang 150 items lamang ang pwedeng ilagay sa isang POW.")
        elif not selected_name:
            st.warning("⚠️ Input Error: Paki-lagay ang Item Name bago mag-add.")
        else:
            final_name = selected_name.title()
            
            check_exists = db.search_master_items(final_name)
            is_new_item = True
            for item in check_exists:
                if item[0].lower() == final_name.lower():
                    is_new_item = False
                    break
            
            if is_new_item:
                if hasattr(db, 'add_new_master_item'):
                    db.add_new_master_item(final_name, unit_input, price_input)
                
                excel_path = r"G:\jrm\master_items.xlsx"
                try:
                    wb = load_workbook(excel_path)
                    ws = wb.active
                    new_row = ws.max_row + 1
                    ws.cell(row=new_row, column=1, value=final_name)
                    ws.cell(row=new_row, column=2, value=unit_input)
                    ws.cell(row=new_row, column=3, value=price_input)
                    wb.save(excel_path)
                    wb.close()
                except Exception as e:
                    pass

            st.session_state.temporary_items.append({
                'qty': qty_input,
                'unit': unit_input,
                'name': final_name,
                'price': price_input
            })
            st.success(f"✔️ Added: {qty_input} {unit_input} - {final_name}")
            st.rerun()

    st.markdown("---")

    # --- TABLE DISPLAY & REMOVE FUNCTION ---
    st.markdown(f"#### 📊 Current Items Added ({len(st.session_state.temporary_items)} / 150)")
    
    if st.session_state.temporary_items:
        table_data = []
        grand_total = 0.0
        
        for index, item in enumerate(st.session_state.temporary_items, start=1):
            total_price = item['qty'] * item['price']
            grand_total += total_price
            table_data.append({
                "#": index,
                "Qty": item['qty'],
                "Unit": item['unit'],
                "Item Name": item['name'],
                "Unit Price": f"₱ {item['price']:,.2f}",
                "Total Price": f"₱ {total_price:,.2f}"
            })
            
        # Inayos ang width ng dataframe dito
        st.dataframe(table_data, width="stretch", hide_index=True)
        st.markdown(f"<h3 style='text-align: right; color: #2b6cb0;'>GRAND TOTAL: ₱ {grand_total:,.2f}</h3>", unsafe_allow_html=True)
        
        col_del, col_space = st.columns([2, 5])
        with col_del:
            item_to_remove = st.number_input("Ipasok ang # ng aytem na nais alisin:", min_value=1, max_value=len(st.session_state.temporary_items), step=1)
            # Inayos ang width ng remove item button
            if st.button("🗑️ Remove Item", type="primary", width="stretch"):
                del st.session_state.temporary_items[int(item_to_remove) - 1]
                st.toast("Item removed successfully!")
                st.rerun()
                
        st.markdown("---")
        
        # --- FINALIZE WORKFLOW ---
        st.markdown("#### 💾 Save Project Details to Database")
        proj_name = st.text_input("Project Name:", key="final_proj_name").strip().title()
        proj_loc = st.text_input("Location:", key="final_proj_loc").strip().title()
        
        # Inayos ang width ng main database save button
        if st.button("💾 CONFIRM & SAVE WHOLE POW TO MYSQL", type="primary", width="stretch"):
            if not proj_name or not proj_loc:
                st.warning("⚠️ Kulang: Pakisulat ang Project Name at Location bago i-save.")
            else:
                success = db.save_pow_to_sql(proj_name, proj_loc, st.session_state.temporary_items)
                if success:
                    st.balloons()
                    st.success("🎉 Matagumpay na nai-save ang buong POW sa MySQL Database!")
                    st.session_state.temporary_items = []
                    st.rerun()
                else:
                    st.error("❌ Database Error: Nagka-error sa pag-save sa MySQL Server.")
    else:
        st.info("💡 Kasalukuyang walang laman ang listahan. Mag-add ng mga aytem sa itaas upang mag-preview.")
