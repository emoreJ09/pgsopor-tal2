import streamlit as st

# I-import ang lahat ng modules na ginawa natin
import login_views
import preview_pow_module
import preview_module  # Ito yung layout text preview core

# 1. INITIALIZE CONFIGURATION & STATES
st.set_page_config(page_title="POW Management System", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default entry node
if "page_view_mode" not in st.session_state:
    st.session_state.page_view_mode = "table_view"  # Default dashboard view

# ==============================================================================
# ROUTER FRAME 1: AUTHENTICATION GATEWAY (Kapag hindi pa naka-login)
# ==============================================================================
if not st.session_state.logged_in:
    if st.session_state.page == "signup":
        login_views.render_register_screen()
    else:
        login_views.render_login_screen()

# ==============================================================================
# ROUTER FRAME 2: SECURE SYSTEM WORKSPACE (Kapag nakapasok na ang user)
# ==============================================================================
else:
    # --- SIDEBAR CONTROL NAVIGATION PANEL ---
    st.sidebar.title(f"👤 {st.session_state.username.upper()}")
    st.sidebar.caption(f"Role Profile: {st.session_state.user_role.upper()}")
    st.sidebar.write("---")
    
    # Navigation Radio Buttons (Dito pinipili kung anong feature ang bubuksan)
    menu_choice = st.sidebar.radio(
        "🗂️ Navigation Menu",
        ["Dashboard & POW List", "Create New POW (Form)"]
    )
    
    st.sidebar.write("---")
    # LOGOUT BUTTON PIPELINE
    if st.sidebar.button("🚪 Logout Account", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.username = ""
        st.session_state.user_role = ""
        st.rerun()

    # --- MAIN CONTENT CONTROLLER ROUTING ---
    if menu_choice == "Dashboard & POW List":
        
        # Sub-routing para sa Preview at Edit features sa loob ng Dashboard
        if st.session_state.page_view_mode == "print_preview":
            # Pindutin ang button para bumalik sa table mode
            if st.button("⬅️ Back to Main Table View", type="secondary"):
                st.session_state.page_view_mode = "table_view"
                st.rerun()
            
            # Patakbuhin ang Text Layout Preview Engine
            preview_module.render_excel_preview_module()
        
        else:
            # I-render ang pangunahing Preview, Edit, at Delete Grid Module natin
            preview_pow_module.render_preview_pow_module()
            
    elif menu_choice == "Create New POW (Form)":
        st.markdown("## ➕ Create New Program of Work")
        st.info("Dito ilalagay ang iyong Tkinter Form component para sa paglikha ng bagong POW.")
        # Dito mo i-call ang function para sa pag-add ng bagong project record...
