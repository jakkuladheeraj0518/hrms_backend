import smtplib
from email.mime.text import MIMEText

def send_email(to_email: str, reset_link: str):
    msg = MIMEText(f"Click here to reset your password: {reset_link}")
    msg["Subject"] = "Password Reset"
    msg["From"] = "noreply@yourapp.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_gmail@gmail.com", "your_app_password")
        server.send_message(msg)
