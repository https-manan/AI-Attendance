import streamlit as st
from src.database.db import enroll_student_to_sub
import segno
import io
import supabase

import time

@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code provided by the teacher to enroll")
    join_code=st.text_input('Subject code',placeholder='Eg. BCS103')

    if st.button("Enroll now",type='primary',width='stretch'):
        if join_code:
            res=supabase.table("Subject").select('subject_id,name,subject_code').eq('subject_code',join_code).execute()
            if res.data:
                subject=res.data[0]
                subject_id=st.session_state.student_data['student_id']
                check=supabase.table('subject_student').select('*').eq('subject_id',subject['subjejct_id']).eq('student_id',student_id)
                if check.data:
                    st.warning('You are already enrolled in the program')
                else:
                    enroll_student_to_sub(student_id,subject['subject_id'])
                    st.success('Successfully enrolled')
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("Enter the subject code")