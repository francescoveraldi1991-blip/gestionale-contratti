import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. RESET TOTALE: FONT GEORGIA E NERO UNIVERSALE */
        html, body, [class*="st-"], .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, span, div, small {
            font-family: 'Georgia', serif !important;
            color: #000000 !important; 
        }

        .stApp {
            background-color: #f8fafc !important;
        }
        
        /* 2. SCHEDE METRICHE CENTRATE */
        [data-testid="stMetric"] {
            background: #ffffff !important;
            border-radius: 15px !important;
            border: 1px solid #d1d5db !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
            text-align: center !important;
        }
        [data-testid="stMetricLabel"] p { color: #000000 !important; font-weight: 600 !important; }
        [data-testid="stMetricValue"] div { color: #004aad !important; font-weight: 800 !important; }

        /* 3. FIX RADICALE PER INPUT E RETTANGOLI (ARCHIVIO) */
        /* Sfondo bianco per tutti i contenitori di input */
        div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="popover"] {
            background-color: #ffffff !important;
            border-radius: 10px !important;
        }

        /* Rettangoli di inserimento testo, numeri e date */
        .stTextInput input, .stNumberInput input, .stDateInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #fbbf24 !important; /* Bordo Oro */
            border-radius: 10px !important;
            height: 45px !important;
        }

        /* Selettore a tendina (Selectbox) */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #fbbf24 !important;
            border-radius: 10px !important;
        }

        /* 4. CARICAMENTO FILE (FILE UPLOADER) - ELIMINA IL NERO INTERNO */
        [data-testid="stFileUploader"] {
            background-color: #ffffff !important;
            border: 2px dashed #fbbf24 !important;
            border-radius: 15px !important;
            padding: 30px !important;
            color: #000000 !important;
        }
        
        /* Forza il colore del tasto "Browse files" all'interno dell'uploader */
        [data-testid="stFileUploader"] button {
            background-color: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #fbbf24 !important;
            border-radius: 8px !important;
        }

        /* Testo "Drag and drop file here" */
        [data-testid="stFileUploader"] section {
            color: #000000 !important;
        }

        /* 5. SIDEBAR LUXURY (Invariata) */
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

        /* 6. BOTTONI AZIONE */
        .stButton>button {
            background: #0f172a !important;
            color: #ffffff !important;
            border: 1px solid #fbbf24 !important;
            font-family: 'Georgia', serif !important;
            font-weight: 700;
            border-radius: 12px;
            text-transform: uppercase;
        }
        .stButton>button:hover {
            background: #fbbf24 !important;
            color: #0f172a !important;
        }
        </style>
    """, unsafe_allow_html=True)
