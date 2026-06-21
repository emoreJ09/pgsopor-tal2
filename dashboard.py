import streamlit as st
import pandas as pd
import db  # Siniguradong naka-import ang database module mo

# --- CONFIGURATION & THEMING ---
st.set_page_config(
    page_title="PGSO Management System - Main Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States para sa Application Routing at Memory Layer
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Workspace"
if "selected_pow_id" not in st.session_state:
    st.session_state.selected_pow_id = None
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

class OfficeDashboardStreamlit:
    def __init__(self, username, user_role, on_logout_callback):
        self.username = username
        self.user_role = user_role
        self.on_logout = on_logout_callback
        
    def render(self):
        # --- SIDEBAR COMPONENT ---
        with st.sidebar:
            st.markdown(
                "<h2 style='text-align: center; color: #1a365d;'>🏛️ PGSO PORTAL</h2>", 
                unsafe_allow_html=True
            )
            st.write(f"**User:** {self.username} (`{self.user_role.upper()}`)")
            st.divider()
            
            st.markdown("### 📋 POW OPERATIONS")
            if st.button("➕ ADD NEW POW", use_container_width=True):
                st.session_state.current_page = "Add POW"
                st.session_state.edit_mode = False
                st.rerun()
                
            if st.button("👁️ PREVIEW POW RECORDS", use_container_width=True):
                st.session_state.current_page = "Preview POW"
                st.session_state.edit_mode = False
                st.rerun()
                
            if st.button("📊 POW MASTERLIST HISTORY", use_container_width=True):
                st.session_state.current_page = "POW Masterlist"
                st.session_state.edit_mode = False
                st.rerun()
                
            st.markdown("### 📄 DOCUMENTS & FORMS")
            if st.button("🛒 PR (Purchase Request)", use_container_width=True):
                self.future_update_notice()
            if st.button("🚗 TO (Travel Order)", use_container_width=True):
                self.future_update_notice()
                
            st.markdown("### ⚙️ SYSTEM")
            if st.button("🛠️ SETTINGS", use_container_width=True):
                self.future_update_notice()
                
            if self.user_role == "admin":
                if st.button("👥 MANAGE USERS", use_container_width=True):
                    st.session_state.current_page = "User Management"
                    st.rerun()
            
            st.write("")
            if st.button("🚪 Mag-Logout", type="primary", use_container_width=True):
                self.on_logout()

        # --- TOPBAR & HEADER AREA ---
        st.markdown(f"# {st.session_state.current_page}")
        st.caption(f"Active Session Context: Localized Database Layer Engine Active")
        st.divider()

        # --- ROUTING ENGINE / MULTI-MODULE DISPATCHER ---
        if st.session_state.current_page == "Dashboard Workspace":
            self.show_welcome_message()
            
        elif st.session_state.current_page == "Add POW":
            st.info("Encoding Area - Add New POW Module is mounted.")
            # Dito pwedeng i-render ang structure ng iyong dating AddPowModule(content_area)
            
        elif st.session_state.current_page == "Preview POW":
            st.info("Data Viewer - Preview POW Records Module is mounted.")
            # Dito pwedeng i-render ang structure ng iyong dating PreviewPowModule(content_area)
            
        elif st.session_state.current_page == "POW Masterlist":
            self.render_pow_masterlist_view()
            
        elif st.session_state.current_page == "User Management" and self.user_role == "admin":
            self.render_user_management_view()

    def show_welcome_message(self):
        st.markdown("### Main Dashboard Workspace")
        with st.container(border=True):
            st.markdown("#### 📘 PGSO Portal System Info")
            guide_text = (
                "All necessary workspace menus have been successfully initialized on the left-side panel (Sidebar) for your office operations:\n\n"
                "- **ADD / EDIT / PREVIEW** – For managing all master data records and transactional data entry.\n"
                "- **POW / PR / TO** – For processing operational program of works, purchase requests, and travel orders.\n"
                "- **SETTINGS** – For system configuration and environment adjustments.\n\n"
                "These navigation controls are currently armed and fully optimized, standing ready for your backend integration and localized database transaction routines.\n\n"
                "**Complete System Guide & Structural Architecture:**\n"
                "The data administration module acts as the gatekeeper of your operational storage layer. "
                "Basic inputs are validated locally prior to executing transactions against the integrated database structures."
            )
            st.info(guide_text)

    def future_update_notice(self):
        st.toast("Ang function na ito ay kasalukuyang inihahanda para sa susunod na update.", icon="⚠️")

    # --- POW RECORD TABLE & EDIT ROW CONTROLLER ---
    def render_pow_masterlist_view(self):
        st.markdown("### Office Records - POW Masterlist History")
        
        # Mocking or simulating selection layer inside Streamlit context
        # Sa actual, maaari mong kunin ang listahan mula sa db.get_all_projects()
        st.write("Pumili ng Proyekto sa listahan sa ibaba upang i-load ang functional dynamic editor:")
        
        # Halimbawang kunwaring ID selection (Palitan ng totoong database query iteration mo)
        proj_id_input = st.number_input("Ipasok ang Target Project ID para sa Edit Mode:", min_value=1, step=1, key="manual_id_select")
        
        if st.button("✏️ Mag-edit / Load Project System Matrix", type="secondary"):
            st.session_state.selected_pow_id = proj_id_input
            st.session_state.edit_mode = True
            st.toast(f"Na-load na ang Record ID #{proj_id_input}!", icon="📝")
            
        # Pag-render sa Edit Form kung ito ay pinili (Katumbas ng open_edit_pow_modal)
        if st.session_state.edit_mode and st.session_state.selected_pow_id:
            st.divider()
            st.markdown(f"#### ✏️ EDIT MODE - Update POW Record ID: `{st.session_state.selected_pow_id}`")
            
            # Fetch current database snapshot details
            try:
                # Kukuha ng sample array values para sa demonstration data frame conversion
                associated_items = db.get_items_by_project(st.session_state.selected_pow_id)
            except Exception:
                associated_items = [(1.0, "pcs", "Sample Item Description from DB", 150.00)]

            with st.form("edit_pow_batch_form", clear_on_submit=False):
                col1, col2 = st.columns(2)
                with col1:
                    ent_proj_name = st.text_input("Project Title / Name:", value="Existing Project Title Alpha")
                with col2:
                    ent_location = st.text_input("Project Location:", value="Province Compound, Area Main")
                
                st.markdown("##### Listahan ng mga Aytem (Interactive Grid)")
                st.caption("Maaari mong baguhin ang mga linya o magdagdag sa pinaka-baba ng table grid.")
                
                # Streamlit Spreadsheet-like Interactive Editor Toolkit Component Dataframe
                df_items = pd.DataFrame(associated_items, columns=["QTY", "UNIT", "ITEM DESCRIPTION", "UNIT PRICE"])
                edited_df = st.data_editor(df_items, num_rows="dynamic", use_container_width=True)
                
                btn_final_save = st.form_submit_submit_button("💾 SAVE ALL CHANGES & OVERWRITE DATABASE", type="primary")
                
                if btn_final_save:
                    new_name = ent_proj_name.strip()
                    new_loc = ent_location.strip()
                    
                    if not new_name or not new_loc:
                        st.error("Hindi pwedeng iwanang blangko ang Project Name at Location, boss.")
                    else:
                        try:
                            # Pag-convert sa dataframe rows pabalik sa tuple batch architecture
                            final_items_to_save = edited_df.values.tolist()
                            
                            # Database batch routine transaction orchestration executions
                            success_main = db.update_project_main_details(st.session_state.selected_pow_id, new_name, new_loc)
                            success_items = db.update_project_items_batch(st.session_state.selected_pow_id, final_items_to_save)
                            
                            if success_main and success_items:
                                st.success("Matagumpay na na-overwrite at na-update ang buong data, boss!")
                                st.session_state.edit_mode = False
                                st.rerun()
                            else:
                                st.error("May error sa database query. Pakisuri kung tugma ang table names.")
                        except Exception as e:
                            st.error(f"Format Validation Error Runtime Exception: {str(e)}")

    # --- ADMIN USER MANAGEMENT DASHBOARD ---
    def render_user_management_view(self):
        st.markdown("### Registered Encoders Control Center")
        
        try:
            users = db.get_all_encoders()
        except Exception:
            users = [(1, "JuanEncoder", "encoder", "pending"), (2, "MariaAdmin", "admin", "active")]

        if not users:
            st.info("No other registered users found.")
            return

        for user in users:
            u_id, u_name, u_role, u_status = user[0], user[1], user[2], user[3]
            
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"👤 **{u_name}** | Role: `{u_role.upper()}` | Status: `{u_status.upper()}`")
                with c2:
                    if u_status == "pending":
                        if st.button("✅ Approve", key=f"app_{u_id}", use_container_width=True):
                            if db.approve_user_by_id(u_id):
                                st.toast(f"User {u_name} activated successfully!", icon="🚀")
                                st.rerun()
                            else:
                                st.error("Failed to approve system user reference node.")
                with c3:
                    if st.button("🗑️ Delete", key=f"del_{u_id}", use_container_width=True, type="primary"):
                        if db.delete_user_by_id(u_id, u_name):
                            st.toast(f"User {u_name} removed safely.", icon="🔒")
                            st.rerun()
                        else:
                            st.error("Failed to execute data array cleanup runtime directive.")

# --- APPLICATION ENTRY EXECUTION POINT WRAPPER ---
def dummy_logout():
    st.success("Logging out session context...")
    st.session_state.clear()

# Streamlit bootstrap context instantiation logic initialization routines
if __name__ == "__main__":
    # Context simulation layer data arrays variables setup
    app = OfficeDashboardStreamlit(username="AdminUserOne", user_role="admin", on_logout_callback=dummy_logout)
    app.render()
