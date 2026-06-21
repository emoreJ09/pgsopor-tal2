import streamlit as st
import db

def main():
    st.markdown("### ➕ Add Project of Work (POW)")
    st.info("Form para sa pag-add ng POW. I-paste natin dito ang mga input fields mo mamaya.")
    
    # Halimbawa ng Streamlit Input fields na ipapait natin sa Tkinter Entries mo:
    title = st.text_input("Project Title")
    location = st.text_input("Location")
    budget = st.number_input("Estimated Budget", min_value=0.0)
    
    if st.button("Save Project", type="primary"):
        st.success("Sample Save Triggered!")
