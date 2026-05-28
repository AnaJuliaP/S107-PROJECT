import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys


def main():
     
    # TODO (Integrante 2): Remover as variaveis do GitHub abaixo e substituir pelas do Jenkins
    # (ex: JOB_NAME, BUILD_NUMBER, BUILD_URL) pois o professor proibiu o uso de GitHub Actions.
    
    build_status = os.getenv("STATUS_BUILD", "desconhecido")
    build_tag = os.getenv("BUILD_TAG", "desconhecido")
    job_name = os.getenv("JOB_NAME", "desconecido")
    build_number = os.getenv("BUILD_NUMBER", "desconecido")
    build_url = os.getenv("BUILD_URL", "desconhecido")

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    email_remetente = os.getenv("EMAIL_REMETENTE")
    email_destino = os.getenv("EMAIL_DESTINO")

    assunto = "Resultado do pipeline CI/CD"
    corpo = f"""
Pipeline finalizado.

Repositório: {job_name}
Build Status: {build_status}
Build Tag: {build_tag}
Build Number: {build_number}
Execução: {build_url}
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