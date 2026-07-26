import streamlit as st


 
def style_background_home():
    st.markdown("""
       <style>
                .stApp{
                background:#2B2D31 !important
                }
                .stApp div[data-testid="stColumn"] {
                    background-color: #E0E3FF !important;
                    padding: 2.5rem !important;
                    border-radius:
                }
       </style>
    """,unsafe_allow_html=True)
    


def style_background_dashboard():
    st.markdown(""" 
        <style>
                .stApp{
                background:#2B2D31 !important
                }
       </style>
    """,unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
     <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
        #MainMenu,footer,header{
           visibility:hidden;
        }
        .block-container{
            padding-top:1.5rem !important;
        }
        h1{
                font-family:'Climate Cris',sans-sarif !important;
                font-size:3.5rem !important
                line-hight:1.1 !important;
                margin-botton:0rem !important
                color:#E0E3FF
        }
        h2{
                font-family:'Climate Cris',sans-sarif !important;
                font-size:3.5rem !important
                line-hight:1.1 !important;
                margin-botton:0rem !important
                color:#E0E3FF
        }
        h3,h4,p{
                font-family:'outfit',sans-sarif;
        }
        button{
            border-radius: 1.5rem !important;
            background: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        button[kind="secondary"]{
            border-radius: 1.5rem !important;
            background: #EB459E !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        button[kind="tertiary"]{
            border-radius: 1.5rem !important;
            background: black !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
     </style>
    """,unsafe_allow_html=True)
