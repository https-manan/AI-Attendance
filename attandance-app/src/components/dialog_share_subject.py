import streamlit as st
from src.database.db import create_subject
import segno
import io


# This is a decorator. this @st.dialog
# A decorator modifies the behavior of the function below it.
# st.dialog() tells Streamlit that instead of displaying the function normally, it should open it inside a popup dialog.
# "Share Class Link" is the title of that popup.


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name,subject_code):
    app_domain="https://localhoast:8501/"   #after deploying URL of the deployed URL here
    join_url=f"{app_domain}/?join_code={subject_code}"  #Basically creating a URL for QR code
    st.header("Scan to join")
    qr=segno.make(join_url) #to iss url ka ek QR code bn jayga using segno library
    out=io.BytesIO          #This is for ki jo QR code image bni hai we gonna store that in RAM itself koi file vagera m store nahi krenge
    qr.save(out,kind='png',scale=10,border=1)
    col1,col2=st.columns(2)
    with col1:
        st.markdown('### copy link')
        st.code(join_url,language="text")  #st.code se copy vala button aa jata hai 
        st.code(subject_code,language="text")
        st.info("Copy this link to share")
    with col2:
        st.markdown('### Scan to join')
        st.image(out.getvalue(),use_column_width=True,caption="QR Code for class joining")

