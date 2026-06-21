import streamlit as st
import db  

# --- 1. I-IMPORT ANG MGA WEB CONVERTED FILES ---
import dashboard     
import add_pow       
import list_pow      
import preview_pow   

# I-initialize ang database sa unang load ng website
if 'db_ready' not in st.session_state:
    try:
        db.initialize_db()
    except Exception as e:
        pass
    st.session_state.db_ready = True

# State management para sa paglipat-lipat ng screen at user sessions
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = '📌 Main Dashboard'


# --- 2. MGA PALANDINGAN O PAHINGA NG WEB APP (SCREENS) ---

def show_login():
    st.markdown("<h2 style='text-align: center; color: #2196F3;'>ACCOUNT LOGIN</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username", key="login_user").strip()
    password = st.text_input("Password", type="password", key="login_pass").strip()
    
    # Inayos ang button width mula use_container_width=True patungong width="stretch"
    if st.button("Login", width="stretch", type="primary"):
        if not username or not password:
            st.warning("⚠️ Attention! All input fields must be filled out before proceeding")
        else:
            user_role = db.authenticate_user(username, password)
            
            if user_role:
                st.success(f"🎉 Success! Logged in as {user_role.upper()}.")
                st.session_state.username = username
                st.session_state.user_role = user_role
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("❌ Login Failed! Invalid username or password. Please try again.")
                
    st.markdown("---")
    # Inayos din ang width dito para pantay at stretch pa rin sa mobile/desktop screens
    if st.button("Don't have an account? Sign Up", width="stretch"):
        st.session_state.page = 'signup'
        st.rerun()


def show_signup():
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>CREATE ACCOUNT</h2>", unsafe_allow_html=True)
    
    username = st.text_input("New Username", key="reg_user").strip()
    password = st.text_input("New Password", type="password", key="reg_pass").strip()
    
    if st.button("Register Account", use_container_width=True):
        if not username or not password:
            st.warning("⚠️ Attention! All fields are required to register an account.")
        else:
            success, message = db.register_user(username, password, role='encoder')
            
            if success:
                st.success(f"🎯 {message}")
                st.info("Maaari ka nang bumalik sa Login page para mag-sign in.")
            else:
                st.error(f"❌ Registration Failed! {message}")
                
    st.markdown("---")
    if st.button("Already have an account? Log In", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()


# --- 3. DITO NAKAKONEKTA ANG MGA PILING FEATURES MO ---
def show_dashboard():
    # Sidebar para sa Navigation at Logout kapag naka-log in na
    st.sidebar.title("📁 PGSO MENU")
    st.sidebar.write(f"👤 User: **{st.session_state.username}**")
    st.sidebar.write(f"⚙️ Role: `{st.session_state.user_role.upper()}`")
    st.sidebar.markdown("---")
    
    # Mga Pagpipilian ng Encoder sa Sidebar
    menu_options = [
        "📌 Main Dashboard", 
        "➕ Add POW", 
        "📋 List POW", 
        "🔍 Preview POW"
    ]
    
    selection = st.sidebar.radio("Pumili ng Aksyon:", menu_options)
    st.sidebar.markdown("---")
    
    # Logout Button sa pinakailalim ng Sidebar
    if st.sidebar.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.page = 'login'
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.current_tab = '📌 Main Dashboard'
        st.rerun()

    # Main Screen Controller batay sa pinili sa Sidebar
    if selection == "📌 Main Dashboard":
        st.markdown(f"<h1 style='color: #333;'>🏢 PGSO Dashboard</h1>", unsafe_allow_html=True)
        st.subheader(f"Welcome, {st.session_state.username}!")
        
        try:
            dashboard.main()
        except AttributeError:
            try:
                dashboard.show_dashboard() 
            except:
                st.error("❌ Hindi matakbo ang dashboard.py. Siguraduhing may 'def main():' ito sa loob.")

    elif selection == "➕ Add POW":
        try:
            add_pow.main() 
        except AttributeError:
            st.error("❌ May error sa pag-load ng add_pow.py. Siguraduhing may 'def main():' ito sa loob.")

    elif selection == "📋 List POW":
        try:
            list_pow.main() 
        except AttributeError:
            st.error("❌ May error sa pag-load ng list_pow.py. Siguraduhing may 'def main():' ito sa loob.")
            
    elif selection == "🔍 Preview POW":
        try:
            preview_pow.main() 
        except AttributeError:
            st.error("❌ May error sa pag-load ng preview_pow.py. Siguraduhing may 'def main():' ito sa loob.")


# --- 4. APP CONTROLLER BLOCK ---
if st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'signup':
    show_signup()
elif st.session_state.page == 'dashboard':
    show_dashboard()
