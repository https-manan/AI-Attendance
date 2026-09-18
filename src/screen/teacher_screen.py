import pandas
from src.components.dialog_add_photo import add_photo_dialog
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attandance import voice_attendance_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_create_subject import create_subject_dialog 
from src.database.db import get_attendance_for_teacher, teacher_login,check_teacher_exists,create_teacher,get_teacher_subjects
import streamlit as st
from src.ui.base_layout import (style_background_dashboard,style_base_layout)
from src.components.header import header_dashbard
from src.components.subject_card import subject_card
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attandace
from datetime import datetime
import numpy as np
import pandas as pd



def teacher_screen():  
    style_background_dashboard()    
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()



def teacher_screen_login(): 
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type'] = None

    st.header("Login using password")
    teacher_username=st.text_input("Enter username",placeholder='https-manan')
    teacher_password=st.text_input("Enter password",type='password',placeholder='*********')
    st.divider()

    btnc1,btnc2=st.columns(2)
    with btnc1:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_password):
                st.toast("Welcome back!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")
    with btnc2:
        if st.button('Register',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type="register"



def register_teacher(teacher_username,teacher_name,teacher_password,teacher_confirmPassword):
    if not teacher_username or not teacher_name or not teacher_password:
        return False,"All fields are required!"
    if check_teacher_exists(teacher_username):
        return False,"Teacher already exists with this username"
    if teacher_password!=teacher_confirmPassword:
        return False,"Enter same password"
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True,"Successfully Created! Login Now"
    except Exception as e:
        return False,"Unexpected error"





def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type'] = None
    st.header("Register your teachers profile")
    teacher_name=st.text_input("Enter name",placeholder='Manan')
    teacher_username=st.text_input("Enter username",placeholder='https-manan')
    teacher_password=st.text_input("Enter password",type='password',placeholder='*********')
    teacher_confirmPassword=st.text_input("Enter password again",type='password',placeholder='*********')
    st.divider()
    btnc1,btnc2=st.columns(2)
    with btnc1:
        if st.button('Register',type='primary',icon=':material/passkey:',width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_password, teacher_confirmPassword)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            st.session_state.teacher_login_type="login"




def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False 


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

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'

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
    teacher_id=st.session_state.teacher_data['teacher_id']
    st.header('Take attandance')

    if 'attendance_images' not in st.session_state:   #basically saari images that we gonna get in input we gonna store in session_state.attandance_image
        st.session_state.attendance_images=[]

    subjects=get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('you havent created any subjects yet! Please create one to begin!')
        return 
    
    subject_options={f"{s['name']}-{s['subject_code']}":s['subject_id']for s in subjects}  #for loop on subjects to get name and all from it like dropdown for sub to select them

    col1, col2 = st.columns([3,1])   #selctbox and photo add krne ka lia button and basically this [3,1] is the ratio of the cols like 4 mai se 3 ka size and 1 ka size and all
    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))
    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photo_dialog()

    selected_subject_id = subject_options[selected_subject_label]#basically we are selecting sub with this selected_sub_label to in selected sub ka data nikal lenge from the main sub table in DB
    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        galary_cols=st.columns(4)    #basically hum joo saare images upload hui hai in st.session_state.attendance_image unhe bus display kra rhe hai ki like these all are the images 

        for idx,img in enumerate(st.session_state.attendance_images):    #Yha pe 4 by 4 ka grid bnaya hai to preview photos
            with galary_cols[idx%4]:
                st.image(img,width='stretch',caption=f"Photo{idx+1}")  #Adding image for displaying

        #This 3 cols r for clear all photos,take attendance and take voice att 
        
        has_photos=bool(st.session_state.attendance_images) #We have used bool to get false if no image and true elese wise
        c1,c2,c3=st.columns(3)
        with c1:   #Deleting all the images
            if st.button("Clear all photos",width='stretch',type='tertiary',icon=':material/delete:',disabled= not has_photos):
                st.session_state.attendance_images=[]
                st.rerun()

        with c2:  #This is for actually taking attandance
            if st.button('Run face analysis',width='stretch',type='secondary',icon=':material/analytics:',disabled= not has_photos):
                with st.spinner("Scanning classroom photos"):
                    all_detected_ids={} #This all detected ids gonna store the unique ids of students from all the images uploaded like this
                                        #{
                                        #     101: ["Photo 1", "Photo 3"],
                                        #     102: ["Photo 1"],
                                        #     105: ["Photo 2", "Photo 4"]
                                        # }

                    for idx,img in enumerate(st.session_state.attendance_images):  #Go over each photo stored in attendance_img and run face detection
                        img_np=np.array(img.convert('RGB'))  # basically image ko RGB mai convert phale bhi kr skte thae its good for model to understand and all 
                        detected,_,_=predict_attandace(img_np)
                        if detected:
                            for sid in detected.keys():
                                student_id=int(sid)
                                all_detected_ids.setdefault(student_id,[]).append(f'Photo {idx+1}')  #jo all_detected_ids bnaya tha uppar usme simplly append the stu_id with images all that are found in the image
                                                                                                    # {
                                                                                                    #     101: []
                                                                                                    # }                       To like studnet with id 101 detect hua to uski image store krenge in form of dictionary
                                                                                                    # .append("Photo 1")
                                                                                                    # {
                                                                                                    #     101: ["Photo 1"]
                                                                                                    # }
                    enrolled_res=supabase.table('subject_students').select('*,students(*)').eq('subject_id',selected_subject_id).execute()  #jo bacche detect hue hai unhe present mark else ko absent mark  
                    enrolled_students=enrolled_res.data

                    if not enrolled_students:
                        st.warning("No students enrolled in this course")
                    else:
                        results,attendance_to_log=[],[]
                        current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  #Basically date and time display

                        for node in enrolled_students:
                            student = node['students']
                            sources = all_detected_ids.get(int(student['student_id']), [])#Sourse mai we store jo student aaya h vo kunsi photo s aaya hai and agr nahi h to empty sourse []
                            is_present = len(sources) > 0  #if sourse is present then present and we append in res

                            results.append({    #Ye table is to show the users
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Source": ", ".join(sources) if is_present else "-",
                                "Status": "✅ Present" if is_present else "❌ Absent"
                            })

                            attendance_to_log.append({  #And this table is to store in DB
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })

                        attendance_result_dialog(pd.DataFrame(results), attendance_to_log) #To this dialog get the result and displays it
        with c3:
            if st.button("Use voice attandance",type='primary',width='stretch',icon=':material/mic:'):
                voice_attendance_dialog(selected_subject_id)



def teacher_tab_manage_subjects():
    teacher_id =st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header('Manage subjects',width='stretch')
    with col2:
        if st.button('Create new subjects',width='stretch'):
            create_subject_dialog(teacher_id)
    #List all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🧑🏼‍🎓", "Students", sub['total_students']),
                ("🎒", "Classes", sub['total_classes']),
            ]

            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])

            st.space()
            subject_card(              #This sub card we gonna use in student and teacher side both 
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.warning("NO SUBJECTS FOUND. CREATE ONE ABOVE")



def teacher_tab_attendance_records():
    teacher_id=st.session_state.teacher_data['teacher_id'] #This teacherId is needed to get all the subjects of the teacher and then from it all the attandance logs of all the students in that sub 
    records=get_attendance_for_teacher(teacher_id)

    if not records:
        return 

    data=[]

    for r in records:
        ts=r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df=pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + "/"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = (summary.sort_values(by='ts_group',ascending=False)
                  [['Time','Subject','Subject code','Attendance stats']]
                  )

    st.dataframe(display_df,width='stretch',hide_index=True)