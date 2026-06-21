import streamlit as st
import db  

# --- 1. MGA IN-IMPORT MONG MODULES (Inayos ang path para sa GitHub) ---
import add_pow        
import preview_pow    
import list_pow       

def main():
    """
    Ito ang pangunahing landing page ng iyong dashboard.
    Lalabas ito kapag ang pinili sa menu ng app.py ay '📌 Main Dashboard'.
    """
    st.markdown("### 📊 PGSO Statistics Overview")
    
    # Gumawa ng magagandang summary cards (Metrics) para sa mga encoders
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="➕ New POW Added Today", value="0", delta="Ready")
    with col2:
        st.metric(label="📁 Total Documents Tracked", value="0", delta="Operational")
    with col3:
        st.metric(label="👤 Current User Role", value=f"{st.session_state.user_role.upper()}")

    st.markdown("---")

    # --- SAKALING MA-CLICK ANG MGA PANSAMANTALANG UTILITY BUTTONS ---
    st.info("💡 **Tip para sa Encoders:** Gamitin ang maliit na arrow (`>`) sa kaliwang itaas ng cellphone upang buksan ang Menu at makapag-add o makapag-list ng Program of Work (POW).")
    
    # Dokumento at Forms section na wala pa sa system
    st.subheader("📋 Other Documents & Forms (Updates Soon)")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🛒 PR (Purchase Request)", use_container_width=True):
            st.warning("🚀 This feature (Purchase Request) will be available in the future update.")
    with col_b:
        if st.button("🚗 TO (Travel Order)", use_container_width=True):
            st.warning("🚀 This feature (Travel Order) will be available in the future update.")
    with col_c:
        if st.button("⚙️ System Settings", use_container_width=True):
            st.warning("🚀 Settings panel is under development.")

    # --- ADMIN EXCLUSIVE FEATURE ---
    if st.session_state.user_role == "admin":
        st.markdown("---")
        st.subheader("👥 Admin Control Panel")
        if st.button("🛠️ Open User Management", type="primary", use_container_width=True):
            st.info("Dito ilalagay ang user management code mo mamaya.")

def future_update_notice():
    st.warning("🚀 This feature is coming soon in the next system deployment.")
