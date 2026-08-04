import streamlit as st

def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #1e1f22 0%, #2b2d31 50%, #111214 100%) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    

def style_background_dashboard():
    st.markdown(""" 
        <style>
            .stApp {
                background: linear-gradient(135deg, #1e1f22 0%, #2b2d31 50%, #111214 100%) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
     <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        .block-container {
            padding-top: 2rem !important;
            max-width: 1200px !important;
        }
        h1, h2, h3, h4, p {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(43, 45, 49, 0.75) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 1.75rem !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            padding: 1rem !important;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-8px);
            border-color: rgba(88, 101, 242, 0.4) !important;
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.5), 0 0 20px rgba(88, 101, 242, 0.15) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] h2 {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: #F2F3F5 !important;
            text-align: center;
            margin-bottom: 1rem !important;
            letter-spacing: -0.02em;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] img {
            border-radius: 1.2rem;
            margin-bottom: 1.5rem;
            object-fit: cover;
        }
        .stButton > button {
            border-radius: 1rem !important;
            background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%) !important;
            color: white !important;
            padding: 0.75rem 1.5rem !important;
            border: none !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            width: 100% !important;
            box-shadow: 0 6px 20px rgba(88, 101, 242, 0.35);
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(88, 101, 242, 0.5);
            background: linear-gradient(135deg, #6772f4 0%, #5865F2 100%) !important;
        }
     </style>
    """, unsafe_allow_html=True)