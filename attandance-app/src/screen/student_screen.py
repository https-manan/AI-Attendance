import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashbard
import numpy as np
from PIL import Image


def student_screen():

    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xlarge')
    with c1:
        header_dashbard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()

    photo=st.camera_in("Position your face in center pls")
    if photo:
        np.array(Image.open(photo))