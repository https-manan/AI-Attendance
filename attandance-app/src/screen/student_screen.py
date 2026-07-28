from src.components.dialog_enroll import enroll_dialog
from src.database.db import get_all_students,get_students_subjects,get_student_attandace
from src.pipelines.face_pipeline import get_face_embeddings, predict_attandace
from src.pipelines.voice_pipeline import get_voice_embedding
import streamlit as st
from ui.base_layout import style_background_dashboard, style_base_layout
from components.header import header_dashbard
from PIL import Image
import numpy as np

show_registration=False 
def student_dashboard():
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        st.subheader(f"Welcome,{student_data['name']}") 
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    st.space()
    c1,c2=st.columns(2)
    with c1:
        st.header('Your enrolled subjects')
    with c2:
        if st.button("Enrolled in subject",type='primary',width='stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner("Loding your enrolled subjects.."):
        subjects=get_students_subjects(student_id)
        logs=get_student_attandace(student_id)

    stats_map={}
    for log in logs:
        sid=log['subject_id']
        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
        stats_map[sid]['total']+=1
        if logs.get('is_present'):
            stats_map[sid]['attanded']+=1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid,{"total":0, "attended": 0} )

        with cols[i % 2]:
            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📋', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ]
            )

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return 
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashbard()
    with c2:
        st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace")
    st.header("Login using faceID")  
    st.space()
    st.space()
    photo_src=st.camera_input("Place your face in center")
    if photo_src:
        img=np.array(Image.open(photo_src))
        with st.spinner('AI is scanning...'):
            detect,all_ids,num_face=predict_attandace(img) 
            if num_face==0:
                st.warning("Face not found!")
            elif num_face>1:
                st.warning("Multiple face found")
            else:
                if detect:
                    student_id=list(detect.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']==student_id),None)
                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast("Welcome back")
                        st.rerun()
                else:
                    st.info("Face not recognized!you might be a new student!")
                    show_registration=True
        if show_registration:
            with st.container(border=True):
                st.header('Register new Profile')
                new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')
                st.subheader('Optional : Voice Enrollment')
                st.info("Enroll your for voice only attendance")
                audio_data = None

                try:
                    audio_data = st.audio_input('Record a short phrase like I am present, My name is Akash.')
                except Exception:
                    st.error('Audio Data failed!')
                if st.button("Create account",type='primary'):
                    if new_name:
                        with st.spinner('Creating profile...'):
                            img=np.array(Image.open(photo_src))
                            encodings=get_face_embeddings(img)
                            if encodings:
                                face_emb=encodings[0].tolist()
                                voice_emb=None
                                if audio_data:
                                    voice_emb=get_voice_embedding(audio.data.read())
                                response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = student
                                    st.toast(f'Welcome Back {student["name"]}')
                                    time.sleep(1)
                                    st.rerun()
                    else:
                        st.warning("Please enter your name")

