import smtplib
import ssl
from email.message import EmailMessage
from config.smtp_config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, DESTINATARIO

def enviar_correo(asunto, cuerpo):
    mensaje = EmailMessage()
    mensaje["From"] = SMTP_USER
    mensaje["To"] = DESTINATARIO
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=contexto) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(mensaje)
        print(f"[SMTP] Correo enviado: {asunto}")
    except Exception as e:
        print(f"[SMTP ERROR] {e}")
