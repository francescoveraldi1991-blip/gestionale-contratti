import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. RESET TOTALE: FONT GEORGIA E NERO UNIVERSALE */
        html, body, [class*="st-"], .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, span, div {
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

        /* 3. FIX PER INPUT (ARCHIVIO) */
        .stTextInput input, .stNumberInput input, .stDateInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #fbbf24 !important;
            border-radius: 10px !important;
        }

        /* 4. CARICAMENTO FILE (FILE UPLOADER) - LUXURY DARK VERSION */
        [data-testid="stFileUploader"] {
            background-color: #ffffff !important; /* Sfondo Blu Notte */
            border: 2px dashed #fbbf24 !important; /* Bordo Oro */
            border-radius: 15px !important;
            padding: 30px !important;
        }
        
        /* FORZA LE SCRITTE IN BIANCO NELL'UPLOADER */
        [data-testid="stFileUploader"] section {
            color: #ffffff !important;
        }
        
        /* Colore per "Drag and drop file here" e "Limit 200MB" */
        [data-testid="stFileUploader"] div, 
        [data-testid="stFileUploader"] span, 
        [data-testid="stFileUploader"] small {
            color: #ffffff !important;
        }

        /* Bottone interno "Browse files" */
        [data-testid="stFileUploader"] button {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border-radius: 8px !important;
            font-weight: bold !important;
        }

        /* 5. SIDEBAR LUXURY */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
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
            background: #ffffff !important;
            color: #ffffff !important;
            border: 1px solid #fbbf24 !important;
            font-family: 'Georgia', serif !important;
            font-weight: 700;
            border-radius: 12px;
        }
        .stButton>button:hover {
            background: #ffffff !important;
            color: #0f172a !important;
        }
        </style>
    """, unsafe_allow_html=True)
