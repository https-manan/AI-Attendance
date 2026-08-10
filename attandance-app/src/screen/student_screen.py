from src.components.dialog_enroll import enroll_dialog
from src.database.db import get_all_students,create_student,get_student_subject,get_student_attendance,unenroll_student_to_sub
from src.pipelines.face_pipeline import get_face_embeddings, predict_attandace,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashbard
from src.components.subject_card import subject_card
import numpy as np
from PIL import Image
import time


def student_dashboard():
    student_data=st.session_state.student_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()   
    with c2:
        st.subheader(f"Welcome,{student_data['name']}")      
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data  
            st.rerun()
    st.space()


    c1,c2=st.columns(2)
    with c1:
        st.header('Your enrolled subjects')
    with c2:
        if st.button('Enroll in subject',type='primary',width='stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your enrolled subjects"):
        subjects= get_student_subject(st.session_state.student_data['student_id'])
        attendance_logs=get_student_attendance(st.session_state.student_data['student_id'])

    #status map mai we gonna store har sub mai kun kaun students enrolled hai and unhone kitni classes kri hai 
    status_map={

    }
    for log in attendance_logs:
        sub_id=log['subject_id']
        if sub_id not in status_map:
            status_map[sub_id]={'total':0,'attended':0}

        status_map[sub_id]['total']+=1  #means class hui hai us sub ki
        if log.get('is_present'):
            status_map[sub_id]['attended']+=1  #means attended the class

    cols=st.columns(2)
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sub_id=sub['subject_id']

        stats=status_map.get(sub_id,{'total':0,'attended':0})
        def unenroll_btn(sub_id=sub_id):
            if st.button("Unenroll from this course",type='tertiary',key=f'unenroll_{sub_id}'):
                unenroll_student_to_sub(st.session_state.student_data['student_id'],sub_id)
                st.toast("Unenrolled from subject")
                st.rerun()
                

        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=(
                    ('🏛️','Total',stats['total']),
                    ('✅','Attended',stats['attended']),
                ),
                footer_callback=unenroll_btn
            )


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    if 'student_data' in st.session_state:
        student_dashboard()
        return

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

    photo = st.camera_input("Position your face in center pls")

    if photo:
        img = np.array(Image.open(photo))

        with st.spinner("Scanning...."):
            detected, all_ids, no_faces = predict_attandace(img)  #the func we define in face_rec that retrun detected,there ids and number of faces
            if no_faces == 0:
                st.warning("Face not found!")
                st.info("Coudent find a face in the photo, you can still register below if you're new")  #agar face detect na ho tab bhi register ka option milna chahiye
                st.session_state.show_registration = True
            elif no_faces > 1:
                st.warning("Multiple face detected")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)#get the student with detected face 
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized! you might be a new student!")
                    st.session_state.show_registration = True   #basically abb new student register hoga nichay

    if st.session_state.show_registration:
        with st.container(border=True):
            st.header('Register new profile')
            new_name = st.text_input("Enter your name", placeholder='Manan')
            st.subheader('optional: Voice enrollment')
            st.info('Enroll your voice for attandance')

            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Manan')
            except:
                st.error('Audio data fails')

            if st.button("Create Account", type='primary'):
                if new_name:
                    if photo:
                        with st.spinner('Creating profile'):
                            img = np.array(Image.open(photo))
                            encoding = get_face_embeddings(img)
                            if encoding:
                                face_emb = encoding[0].tolist()
                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embedding(audio_data.read())

                                resData = create_student(new_name, face_emb, voice_emb)

                                if resData:  # basically aab new entry hui hai to train classifier cache ko clear krke new cache load kr lega
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = resData[0]
                                    st.session_state.show_registration = False
                                    st.toast(f'Profile Created! Hi {new_name}!')
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Coudent capture your faceial features")  #yahan pe face not found tha isliye embeddings nai bane
                    else:
                        st.warning("Please capture your face again.")
                else:
                    st.warning("Please enter your name")