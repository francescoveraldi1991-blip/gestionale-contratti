import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Forza lo sfondo dell'intera pagina e dei contenitori */
        .stApp, .main, .block-container {
            background-color: #f8fafc !important;
        }

        /* TRUCCO PER LA TABELLA: Forza il contenitore a essere bianco */
        [data-testid="stDataFrame"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 15px !important;
        }

        /* Questo serve per le tabelle vecchio stile e box di testo */
        table, thead, tbody, th, td, tr {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* --- SIDEBAR (Manteniamo Luxury) --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        }
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

        /* --- BOTTONI --- */
        .stButton>button {
            background: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #fbbf24 !important;
        }
        </style>
    """, unsafe_allow_html=True)
