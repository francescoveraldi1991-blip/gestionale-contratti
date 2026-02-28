import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. IMPOSTAZIONE FONT GEORGIA UNIVERSALE */
        html, body, [class*="st-"], .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, span, div {
            font-family: 'Georgia', serif !important;
            color: #000000 !important; 
        }

        .stApp {
            background-color: #f8fafc !important;
        }
        
        /* 2. CENTRATURA E STILE SCHEDE METRICHE (DASHBOARD) */
        [data-testid="stMetric"] {
            background: #ffffff !important;
            border-radius: 15px !important;
            border: 1px solid #d1d5db !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
            text-align: center !important; /* Centra il contenitore */
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Forza la centratura dell'etichetta (es: "Volume d'Affari") */
        [data-testid="stMetricLabel"] {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
        }
        
        [data-testid="stMetricLabel"] p {
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            text-align: center !important;
        }

        /* Forza la centratura del numero/valore */
        [data-testid="stMetricValue"] {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
        }

        [data-testid="stMetricValue"] div {
            color: #004aad !important; 
            font-weight: 800 !important;
            text-align: center !important;
        }

        /* 3. SIDEBAR (MANTENIAMO BIANCO SU BLU MA CON FONT GEORGIA) */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
            font-family: 'Georgia', serif !important;
        }
        
        .sidebar-title {
            color: #ffffff !important;
            text-align: center;
            font-size: 1.8rem !important;
            font-weight: bold;
            padding-top: 20px;
        }

        /* 4. TABELLA (DATABASE CONTRATTI) */
        [data-testid="stDataFrame"], table, thead, tbody, th, td {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: 'Georgia', serif !important;
        }

        /* 5. BOTTONI */
        .stButton>button {
            background: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #fbbf24 !important;
            font-family: 'Georgia', serif !important;
            font-weight: 700;
        }
        
        .stButton>button:hover {
            background: #fbbf24 !important;
            color: #0f172a !important;
        }
        </style>
    """, unsafe_allow_html=True)
