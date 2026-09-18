import streamlit as st


def header_home():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom: 1rem;">
                <h1 style='font-size: 3rem; letter-spacing: 2px; margin-bottom: 0;'>ClassRoll<span style="color: #5865F2;">AI</span></h1>
                <p style='color: #b5bac1; font-size: 1.1rem; margin-top: 5px;'>Select your portal to continue</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def header_dashbard():
    st.image("app-logo.webp", width=90)
    st.markdown(
        """
            <h2>ClassRoll<br/>AI</h2>
        """,
        unsafe_allow_html=True
    )