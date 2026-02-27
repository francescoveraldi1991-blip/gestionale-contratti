import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Import font professionale */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        /* Sfondo generale e font */
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
            color: #1a1a1a !important; /* Testo nero ovunque */
        }

        .stApp {
            background: #f8fafc; /* Sfondo chiaro e pulito */
        }
        
        /* Sidebar Luxury */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        /* Titolo Elite v3.0 in Georgia Bianco */
        .sidebar-title {
            font-family: 'Georgia', serif !important;
            color: #ffffff !important;
            text-align: center;
            font-size: 1.8rem !important;
            font-weight: bold;
            margin-bottom: 0px;
        }

        /* Card Metriche Invariate (Glassmorphism chiaro) */
        [data-testid="stMetric"] {
            background: white !important;
            border-radius: 20px !important;
            padding: 25px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        }
        
        /* Riquadri, Expander e Form: Sfondo Bianco e Testo Nero */
        .stStep, .stAlert, .stFileUpload, .stSelectbox, .stDateInput, .stNumberInput, .stTextInput, div[data-testid="stExpander"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 12px !important;
        }

        /* Fix per i testi dentro gli expander e i box */
        .stMarkdown p, .stMarkdown h3, label p {
            color: #1a1a1a !important;
        }

        /* Bottoni */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3.5em;
            background: #0f172a;
            color: #ffffff !important;
            font-weight: 700;
            border: 1px solid #fbbf24;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: #fbbf24;
            color: #0f172a !important;
            box-shadow: 0 10px 20px rgba(251,191,36,0.3);
        }

        /* Dataframe (Tabella) */
        [data-testid="stDataFrame"] {
            background: white !important;
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
