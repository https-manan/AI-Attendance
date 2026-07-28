
from src.components.dialogue_create_subject import create_subject_dialog 
from src.database.db import teacher_login,check_teacher_exists,create_teacher
import streamlit as st
from ui.base_layout import style_background_dashboard, style_base_layout
from components.header import header_dashbard
import share_subject_dialog




def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        st.subheader(f"Welcome,{teacher_data['name']}") 
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    st.space()

    if 'curren_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab='take_attandance'

    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    pass
def teacher_tab_manage_subjects():
    teacher_id =st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header('Manage subjects',width='stretch')
    with col2:
        if st.button('Create new subjects',width='stretch'):
            create_subject_dialog(teacher_id)
    #List all subjects
    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🏫", "Classes", sub['total_classes']),
            ]

            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])

            st.space()
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
    st.warning("NO SUBJECTS FOUND. CREATE ONE ABOVE")
def teacher_tab_attendance_records():
    pass



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