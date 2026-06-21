import streamlit as st
from datetime import datetime
import db  # Konektado sa corrected db.py layer mo

def main():
    st.markdown("### 📜 PROGRAM OF WORKS (POW) MASTERLIST HISTORY")
    st.info("💡 **Tip para sa Mobile:** Maaari mong i-swipe pakaliwa o pakanan ang mga talahanayan (tables) kung hindi kasya ang lahat ng kolum sa screen ng iyong cellphone.")
    
    try:
        # Hihilahin ang mga records mula sa db
        records = db.get_all_pow_history()
    except Exception as e:
        st.error(f"❌ Error sa pag-load ng POW History: {e}")
        return

    if not records:
        st.info("💡 Walang mahanap na sineb na Program of Work (POW) history sa database.")
        return

    # --- PROCESS DATA INTO MONTH BRACKETS (Kumbaga sa Treeview Parent/Child Nodes) ---
    grouped_data = {}

    for row in records:
        pow_id = row[0]
        proj_name = row[1]
        location = row[2]
        grand_total = float(row[3])
        created_at = row[4]

        # Siguraduhing datetime object ang hawak natin
        if isinstance(created_at, str):
            try:
                dt_obj = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt_obj = datetime.now()
        else:
            dt_obj = created_at

        # Kunin ang Month Bracket Name (hal. "JUNE 2026")
        month_name = dt_obj.strftime("%B %Y").upper()
        time_str = dt_obj.strftime("%H:%M:%S")
        date_str = dt_obj.strftime("%m/%d/%Y")

        if month_name not in grouped_data:
            grouped_data[month_name] = []

        grouped_data[month_name].append({
            "POW ID": pow_id,
            "Project Name": proj_name,
            "Location": location,
            "Grand Total Amount": f"₱ {grand_total:,.2f}",
            "Time": time_str,
            "Date": date_str
        })

    # --- RENDER THE WEB LAYOUT (MONTH BY MONTH EXPANDERS) ---
    for month_bracket, items in grouped_data.items():
        # Gumamit ng st.expander na parang Treeview toggle node na pwedeng i-collapse
        with st.expander(f"📅 {month_bracket} ({len(items)} Records Locked)", expanded=True):
            
            # Ipakita ang mga data rows sa loob ng expander gamit ang interactive Streamlit Dataframe
            st.dataframe(
                items,
                use_container_width=True,
                hide_index=False,
                column_config={
                    "POW ID": st.column_config.TextColumn("POW ID", width="small"),
                    "Project Name": st.column_config
