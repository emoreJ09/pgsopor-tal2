import streamlit as st
import db
import excel_generator  # Tinatawag ang bago mong excel_generator.py

def main():
    """
    Ito ang pangunahing function na hinahanap ng app.py.
    Dito pipili ng proyektong gustong i-preview o i-download ng user.
    """
    st.markdown("### 🔍 Preview & Export Program of Work (POW)")
    st.write("Dito maaari mong suriin ang layout ng POW at i-download ito bilang opisyal na Excel file.")
    st.markdown("---")

    try:
        # Kumuha ng listahan ng mga proyekto para sa dropdown selection
        projects = db.get_project_list()
    except Exception as e:
        st.error(f"❌ Error sa pag-konekta sa database: {e}")
        return

    if not projects:
        st.info("💡 Kasalukuyang walang naka-save na proyekto sa database na maaaring i-preview.")
        return

    # I-format ang mga pagpipilian para sa Selectbox/Dropdown
    # Format ng proj base sa db mo: (pow_id, project_name, location)
    project_options = {f"ID: {proj[0]} | {proj[1]} ({proj[2]})": proj[0] for proj in projects}
    
    selected_display = st.selectbox(
        "🎯 Pumili ng Proyekto na Nais I-preview/I-download:",
        options=list(project_options.keys())
    )

    if selected_display:
        # Kunin ang katumbas na pow_id ng piniling proyekto
        chosen_pow_id = project_options[selected_display]
        
        st.markdown("---")
        
        # Tawagin ang preview engine na nasa loob ng excel_generator.py
        try:
            excel_generator.show_excel_preview_streamlit(chosen_pow_id)
        except Exception as e:
            st.error(f"❌ May error sa pag-render ng preview: {e}")

if __name__ == "__main__":
    main()
