import streamlit as st
import db

# I-set ang paunang configuration ng webpage profile tab
st.set_page_config(
    page_title="My App Manager",
    page_icon="💼",
    layout="centered" if "logged_in" not in st.session_state or not st.session_state.logged_in else "wide"
)

# ==============================================================================
# SYSTEM INITIALIZATION & STATE MANAGEMENT
# ==============================================================================
# Patakbuhin ang database migration system sa unang load ng page
if "db_initialized" not in st.session_state:
    db.initialize_db()
    st.session_state.db_initialized = True

# Siguraduhing may default structural keys ang ating application state router
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default initial routing view
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ==============================================================================
# ROUTING CONTROLLER CORE LOGIC
# ==============================================================================
def navigate_to(page_name):
    """Utility function na pumapalit sa window management routing ng Tkinter."""
    st.session_state.page = page_name
    st.rerun()

def process_logout():
    """Nililinis ang user variables kapag nag-click ng logout."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.page = "login"
    st.rerun()

# ==============================================================================
# SCREEN RENDERING FRAMEWORK SWITCHBOARD
# ==============================================================================
def main():
    # --------------------------------------------------------------------------
    # VIEW 1: LOGIN SCREEN PAGE
    # --------------------------------------------------------------------------
    if st.session_state.page == "login":
        st.markdown("## 🔐 System Portal Login")
        st.caption("Ipasok ang iyong credentials para makapasok sa application workspace.")
        
        with st.form("login_gateway_form"):
            user_input = st.text_input("Username:", placeholder="e.g., encoder1")
            pass_input = st.text_input("Password:", type="password", placeholder="••••••••")
            
            submit_login = st.form_submit_button("Sign In to Workspace", use_container_width=True)
            
            if submit_login:
                if not user_input or not pass_input:
                    st.error("⚠️ Paki-sulat ang username at password.")
                else:
                    # Pagtawag sa authenticate_user function mula sa db.py mo
                    role = db.authenticate_user(user_input, pass_input)
                    
                    if role == "pending":
                        st.warning("⏳ Ang account na ito ay kasalukuyan pang pinoproseso para sa Admin Approval.")
                    elif role:
                        st.session_state.logged_in = True
                        st.session_state.username = user_input
                        st.session_state.user_role = role
                        st.session_state.page = "dashboard"
                        st.success("🎉 Pagpasok Matagumpay!")
                        st.rerun()
                    else:
                        st.error("❌ Mali ang Username o Password. Subukang muli.")
                        
        st.write("")
        st.caption("Wala ka pang account sa cloud database system?")
        if st.button("📝 Create New Encoder Account", use_container_width=True):
            navigate_to("signup")

    # --------------------------------------------------------------------------
    # VIEW 2: SIGNUP / REGISTER SCREEN PAGE
    # --------------------------------------------------------------------------
    elif st.session_state.page == "signup":
        st.markdown("## 📝 Registration Gateway")
        st.caption("Magrehistro ng bagong encoder account sa Cloud Database system node.")
        
        with st.form("signup_registration_form"):
            new_user = st.text_input("Desired Username:")
            new_pass = st.text_input("Secure Password:", type="password")
            confirm_pass = st.text_input("Confirm Password:", type="password")
            
            submit_signup = st.form_submit_button("Submit Registration for Approval", use_container_width=True)
            
            if submit_signup:
                if not new_user or not new_pass:
                    st.error("⚠️ Lahat ng fields ay kailangang punan.")
                elif new_pass != confirm_pass:
                    st.error("❌ Hindi nagtutugma ang Password at Confirm Password.")
                else:
                    success, message = db.register_user(new_user, new_pass, role='encoder')
                    if success:
                        st.success(f"✅ {message}")
                        st.info("I-redirect ka na ngayon sa login panel.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {message}")
                        
        if st.button("⬅️ Bumalik sa Login Screen", use_container_width=True):
            navigate_to("login")

    # --------------------------------------------------------------------------
    # VIEW 3: MAIN OFFICE DASHBOARD
    # --------------------------------------------------------------------------
    elif st.session_state.page == "dashboard":
        # Dito mo pwedeng i-import ang dynamic layouts mo tulad ng AddPowModule natin kanina
        # Ine-emulate nito ang: OfficeDashboard(username=..., user_role=...)
        
        # --- TOP HEADER SIDEBAR CONTROL ---
        st.sidebar.markdown(f"### 👤 Active: {st.session_state.username}")
        st.sidebar.markdown(f"🎯 **Role:** `{st.session_state.user_role.upper()}`")
        
        if st.sidebar.button("🚪 Logout / Sign Out", type="secondary", use_container_width=True):
            process_logout()
            
        st.sidebar.divider()
        
        # --- TAB NAVIGATION WORKSPACE SCRIPT ---
        # Ginagamit natin ito bilang kapalit ng Tkinter Frame Switching architecture
        workspace_tab = st.sidebar.radio(
            "🗂️ Navigation Modules", 
            options=["Program of Work (POW)", "Admin Management Panel", "System Logs"]
        )
        
        if workspace_tab == "Program of Work (POW)":
            # Dito mo tatawagin ang module rendering code ng dashboard o add pow view
            st.markdown(f"### Welcome Back, {st.session_state.username}! 👋")
            st.info("Pumili ng sub-action module o gamitin ang POW management suite.")
            
            # Paunang halimbawa ng pag-link:
            # from add_pow_view import render_add_pow_module
            # render_add_pow_module()
            
        elif workspace_tab == "Admin Management Panel":
            if st.session_state.user_role.lower() != "admin":
                st.error("⛔ Access Denied: Ang module na ito ay para lamang sa System Administrators.")
            else:
                st.markdown("### 🛠️ Admin User Approval Controller")
                # Dito ilalagay ang db.get_all_encoders() display loops mo
                
        else:
            st.markdown("### 📑 System Diagnostics Configuration")
            st.caption("Active monitoring engine configuration pipelines.")

if __name__ == "__main__":
    main()
