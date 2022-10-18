import smtplib
import os
from email.mime.text import MIMEText


def send_error(message):
    sender = "kkropachev1@gmail.com"
    # your password = "your password"
    password = 'irvglgwmdaiavtjr'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText('Проблема с транзакцией номер ' + message)
        msg["Subject"] = "Ошибка в данных"
        server.sendmail(sender, sender, msg.as_string())

    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"
