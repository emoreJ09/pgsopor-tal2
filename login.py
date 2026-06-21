import streamlit as st
import db  # Naka-link sa iyong inayos na db.py module

def render_login_screen():
    """Renders the standalone Account Login portal view."""
    st.markdown("## 🔐 ACCOUNT LOGIN")
    st.caption("Workspace Access Authentication Engine")
    
    # Paggamit ng Streamlit form para maiwasan ang un-submitted execution reruns
    with st.form(key="login_form_handler"):
        username = st.text_input("Username:", placeholder="Ipasok ang username...", autocomplete="username")
        password = st.text_input("Password:", type="password", placeholder="Ipasok ang password...", autocomplete="current-password")
        
        # Form submission button act as the main trigger handler
        login_submitted = st.form_submit_button("Login to System", type="primary", use_container_width=True)
        
        if login_submitted:
            username_clean = username.strip()
            password_clean = password.strip()
            
            # Validation Check Validation Logic
            if not username_clean or not password_clean:
                st.warning("⚠️ Attention! All input fields must be filled out before proceeding.")
            else:
                # Pagtawag sa authenticate_user query process mula sa database core
                user_role = db.authenticate_user(username_clean, password_clean)
                
                if user_role == "pending":
                    st.warning("⏳ Access Deferred: Your registration request is still pending for admin authorization approval.")
                elif user_role:
                    # I-commit ang tracking metadata configurations sa memory state layer
                    st.session_state.logged_in = True
                    st.session_state.username = username_clean
                    st.session_state.user_role = user_role
                    st.session_state.page = "dashboard"
                    
                    st.success(f"🎉 Success! Your credentials have been verified. Logged in as {user_role.upper()}.")
                    st.rerun()
                else:
                    st.error("❌ Login Failed! Invalid username or password. Please try again.")

    # Link routing section para lumipat sa Register view
    st.write("")
    if st.button("Don't have an account? Sign Up", type="secondary", use_container_width=True):
        st.session_state.page = "signup"
        st.rerun()


def render_register_screen():
    """Renders the account creation portal module screen view."""
    st.markdown("## 📝 CREATE ACCOUNT")
    st.caption("New Encoder Account Registration Gateway Node")
    
    with st.form(key="registration_form_handler"):
        new_username = st.text_input("New Username:", placeholder="Pumili ng natatanging username...")
        new_password = st.text_input("New Password:", type="password", placeholder="Gumawa ng ligtas na password...")
        confirm_password = st.text_input("Confirm New Password:", type="password", placeholder="Ulitin ang password...")
        
        register_submitted = st.form_submit_button("Register Account", type="primary", use_container_width=True)
        
        if register_submitted:
            username_clean = new_username.strip()
            password_clean = new_password.strip()
            confirm_clean = confirm_password.strip()
            
            if not username_clean or not password_clean or not confirm_clean:
                st.warning("⚠️ Attention! All fields are required to register an account.")
            elif password_clean != confirm_clean:
                st.error("❌ Registration Failed! Hindi nagtutugma ang ginawa mong password.")
            else:
                # Isulat ang registration records patungong cloud sa pamamagitan ng db core module
                success, message = db.register_user(username_clean, password_clean, role='encoder')
                
                if success:
                    st.success(f"✅ Success! {message}")
                    # Awtomatikong ibalik sa login frame pagkatapos ng matagumpay na submission node process
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error(f"❌ Registration Failed! {message}")

    # Link routing section para bumalik sa login form
    st.write("")
    if st.button("Already have an account? Log In", type="secondary", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
