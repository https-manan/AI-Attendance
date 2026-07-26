
from src.database.db import teacher_login,check_teacher_exists,create_teacher
import streamlit as st
from ui.base_layout import style_background_dashboard, style_base_layout
from components.header import header_dashbard


def register_teacher(teacher_username,teacher_name,teacher_password,teacher_confirmPassword):
    if not teacher_username or teacher_name or teacher_password:
        return False,"All fields are required!"
    if check_teacher_exists(teacher_username):
        return False,"Teacher already exists with this username"
    if teacher_password!=teacher_confirmPassword:
        return False,"Password dosent matches"
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True,"Successfully Created! Login Now"
    except Exception as e:
        return False,"Unexpected error"

    
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    teacher_screen_login()




def teacher_screen_login(): 
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace")


    st.header("Login using password",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='https-manan')
    st.space()
    st.space()
    teacher_password=st.text_input("Enter password",type='password',placeholder='*********')
    st.divider()

    btnc1,btnc2=st.columns(2)
    with btnc1:
        if st.bottom('Login',icon=':material/passkey:',shortcut='contorl+enter',width='stretch'):
            if teacher_login(teacher_username,teacher_password):
                st.toast("Welcome back!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and passowrd")

    with btnc2:
        st.bottom('Register',type='primary',icon=':material/passkey:',width='stretch')
        st.session_state.teacher_login_type="register"




def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace")
    st.header("Register your teachers profile")
    st.space()
    st.space()
    teacher_name=st.text_input("Enter name",placeholder='Manan')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='https-manan')
    st.space()
    st.space()
    teacher_password=st.text_input("Enter password",type='password',placeholder='*********')
    st.divider()
    teacher_confirmPassword=st.text_input("Enter password again",type='password',placeholder='*********')
    btnc1,btnc2=st.columns(2)
    with btnc1:
        st.bottom('Login',icon=':material/passkey:',shortcut='contorl+enter',width='stretch')
        st.session_state.teacher_login_type="login"
    with btnc2:
        if st.bottom('Register',type='primary',icon=':material/passkey:',width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_password, teacher_confirmPassword)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)