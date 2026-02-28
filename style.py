import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. IMPORT FONT PROFESSIONALE */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        /* 2. REGOLA UNIVERSALE TESTO NERO (TUTTA L'APP TRANNE SIDEBAR) */
        /* Questo colpisce paragrafi, titoli, metriche e scritte nelle tabelle */
        .main .block-container p, 
        .main .block-container h1, 
        .main .block-container h2, 
        .main .block-container h3, 
        .main .block-container h4, 
        .main .block-container span, 
        .main .block-container label,
        .main .block-container div {
            color: #000000 !important;
        }

        .stApp {
            background-color: #f8fafc !important;
        }
        
        /* 3. SIDEBAR LUXURY (MANTENIAMO BIANCO SU BLU) */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        /* Forza il bianco solo nella sidebar */
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        .sidebar-title {
            font-family: 'Georgia', serif !important;
            color: #ffffff !important;
            text-align: center;
            font-size: 1.8rem !important;
            font-weight: bold;
            padding-top: 20px;
        }

        /* 4. SCHEDE METRICHE (DASHBOARD) */
        [data-testid="stMetric"] {
            background: #ffffff !important;
            border-radius: 20px !important;
            padding: 25px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        }
        
        /* Colore specifico per i numeri delle schede (Blu Profondo) */
        [data-testid="stMetricValue"] div {
            color: #004aad !important;
            font-weight: 800 !important;
        }

        /* 5. TABELLE E INPUT */
        /* Forza lo sfondo bianco e scritte nere per le tabelle */
        [data-testid="stDataFrame"], table, thead, tbody, th, td, tr {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Sfondo bianco per i campi dove si scrive */
        .stTextInput input, .stSelectbox div, .stDateInput input, .stNumberInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* 6. BOTTONI LUXURY */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3.5em;
            background: #0f172a !important;
            color: #ffffff !important;
            font-weight: 700;
            border: 1px solid #fbbf24 !important;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: #fbbf24 !important;
            color: #0f172a !important;
            box-shadow: 0 10px 20px rgba(251,191,36,0.3);
        }
        </style>
    """, unsafe_allow_html=True)
