import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
     
    build_status = os.getenv("STATUS_BUILD", "desconhecido")
    build_tag = os.getenv("BUILD_TAG", "desconhecido")
    build_number = os.getenv("BUILD_NUMBER", "desconhecido")
    build_id = os.getenv("BUILD_ID", "desconhecido")
    job_name = os.getenv("JOB_NAME", "desconhecido")

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    email_remetente = os.getenv("EMAIL_REMETENTE")
    email_destino = os.getenv("EMAIL_DESTINO")

    assunto = "Resultado do pipeline CI/CD"
    corpo = f"""
Pipeline finalizado.

Build Status: {build_status}
Build Tag: {build_tag}
Build Number: {build_number}
Build ID: {build_id}
Job Name: {job_name}
""".strip()

    if not all([smtp_host, smtp_port, email_remetente, email_destino]):
        print("Segredos de e-mail não configurados. Notificação não enviada.")
        print(corpo)
        return

    msg = MIMEMultipart()
    msg["From"] = email_remetente
    msg["To"] = email_destino
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    with smtplib.SMTP(smtp_host, int(smtp_port)) as servidor:
        servidor.send_message(msg)

    print("Notificação enviada com sucesso.")


if __name__ == "__main__":
    main()