import streamlit as st
from components.header import header_home
from ui.base_layout import style_base_layout


def home_screen():

    header_home()
    style_base_layout()
    col1,col2=st.columns(2)

    with col1:
        st.header("I am student")
        st.image('student.jpg')
        if st.button("Student portal"):
            st.session_state['login_type']='student'
            st.rerun()
    with col2:
        st.header("I am teacher")
        st.image('Teacher.png')
        if st.button("Teacher portal"):
            st.session_state['login_type']='teacher'
            st.rerun()
        
