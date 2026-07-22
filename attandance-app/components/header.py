import streamlit as st




def header_home():
    st.image("app-logo.webp", width=200)
    st.markdown(
        """
            <h1>SNAP<br/>CLASS</h1>
        """,
        unsafe_allow_html=True
    )
