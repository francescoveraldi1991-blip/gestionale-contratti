import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. FONT E COLORE UNIVERSALE */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
            color: #000000 !important; 
        }

        .stApp {
            background-color: #f8fafc !important;
        }
        
        /* 2. TITOLI E SOTTOTITOLI (EXECUTIVE DASHBOARD, ANALISI, ECC.) */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6, .main span, .main p {
            color: #000000 !important;
            font-weight: 700 !important;
        }

        /* 3. SCHEDE METRICHE (CONTRATTI IN ESSERE, CRITICAL ALERTS, ECC.) */
        /* Sfondo scheda */
        [data-testid="stMetric"] {
            background: #ffffff !important;
            border-radius: 15px !important;
            border: 1px solid #d1d5db !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        }

        /* Testo dell'etichetta (es: "Volume d'Affari") */
        [data-testid="stMetricLabel"] p {
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }

        /* Numero all'interno (es: "€ 120.000") */
        [data-testid="stMetricValue"] div {
            color: #004aad !important; /* Manteniamo un blu scuro per i numeri per eleganza */
            font-weight: 800 !important;
        }

        /* 4. TABELLA (DATABASE CONTRATTI) */
        [data-testid="stDataFrame"], table, thead, tbody, th, td {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* 5. SIDEBAR (MANTENIAMO BIANCO SU BLU) */
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

        /* 6. BOTTONI */
        .stButton>button {
            background: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #fbbf24 !important;
            font-weight: 700;
        }
        
        .stButton>button:hover {
            background: #fbbf24 !important;
            color: #0f172a !important;
        }
        </style>
    """, unsafe_allow_html=True)
