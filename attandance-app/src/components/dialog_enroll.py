import streamlit as st
from src.database.db import enroll_student_to_sub
from src.database.config import supabase
import time


@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code provided by the teacher to enroll")
    join_code=st.text_input('Subject code',placeholder='Eg. BCS103')
    if st.button("Enroll now",type='primary',width='stretch'):
        if join_code:
            res=supabase.table("subjects").select('subject_id,name,subject_code').eq('subject_code',join_code).execute()  #checking if sub even exists
            if res.data:
                subject=res.data[0]
                student_id=st.session_state.student_data['student_id'] #To check that ye student id vala baccha is already exists to nahi krta iss subject mai

                check=supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()  #ye unique combo we are finding to we use 2 eq's

                if check.data:
                    st.warning('You are already enrolled in this subject')
                else:
                    if enroll_student_to_sub(student_id,subject['subject_id']):
                        st.success('Successfully enrolled')
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Enrollment failed")
            else:
                st.warning("Invalid subject code")
        else:
            st.warning("Enter the subject code")