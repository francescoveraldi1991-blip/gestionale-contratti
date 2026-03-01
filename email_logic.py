import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_expiry_email(destinatario, nome_cliente, data_scadenza):
    # --- CONFIGURAZIONE PARAMETRI (Da inserire nei Secrets di Streamlit o qui) ---
    mittente_email = "tuo_indirizzo@gmail.com"  # Inserisci la tua mail
    password_email = "tua_password_app"         # Inserisci la Password per le App
    
    oggetto = f"⚠️ AVVISO SCADENZA CONTRATTO: {nome_cliente}"
    
    corpo_messaggio = f"""
    Gentile Amministratore,
    
    Il sistema ELITE Management ti informa che il contratto relativo al cliente:
    
    📌 **{nome_cliente}**
    
    risulta in scadenza il giorno: **{data_scadenza}**.
    
    Si prega di avviare le procedure di rinnovo o di adeguamento ISTAT tramite l'Editor Contratti della Web App.
    
    Cordialmente,
    Elite Digital Assistant 💎
    """

    msg = MIMEMultipart()
    msg['From'] = mittente_email
    msg['To'] = destinatario
    msg['Subject'] = oggetto
    msg.attach(MIMEText(corpo_messaggio, 'plain'))

    try:
        # Configurazione Server Gmail (esempio)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mittente_email, password_email)
        text = msg.as_string()
        server.sendmail(mittente_email, destinatario, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Errore nell'invio email: {e}")
        return False
