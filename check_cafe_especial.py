import smtplib
import os
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

URL = "https://rio.armazemdocampo.com.br/produto/cafe-especial-em-graos-250g-raizes-do-campo/"

def is_available():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Localiza apenas a área do produto principal
    product_section = soup.find("div", class_="summary entry-summary")

    # Dentro dessa seção, procura o botão de compra
    if product_section:
        button = product_section.find("button", class_="single_add_to_cart_button")
        return button and "disabled" not in button.attrs.get("class", [])
    return False

def send_email():
    from_addr = os.environ["EMAIL_FROM"]
    to_addr = os.environ["EMAIL_TO"]
    password = os.environ["EMAIL_PASSWORD"]

    subject = "Produto disponível!"
    body = f"O produto está disponível: {URL}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

if is_available():
    send_email()
