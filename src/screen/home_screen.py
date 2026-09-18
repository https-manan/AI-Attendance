import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()
    header_home()
    st.markdown("<br>", unsafe_allow_html=True)
    _, main_col, _ = st.columns([1, 10, 1])
    
    with main_col:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            with st.container(border=True):
                st.markdown('<div class="portal-content">', unsafe_allow_html=True)
                st.header("I am student")
                st.image('student.jpg', use_container_width=True)
                if st.button("Student portal", use_container_width=True):
                    st.session_state['login_type'] = 'student'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            with st.container(border=True):
                st.markdown('<div class="portal-content">', unsafe_allow_html=True)
                st.header("I am teacher")
                st.image('Teacher.png', use_container_width=True)
                if st.button("Teacher portal", use_container_width=True):
                    st.session_state['login_type'] = 'teacher'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)