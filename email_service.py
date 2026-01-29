import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = "venugogineni053@gmail.com"          # sender gmail
APP_PASSWORD = "lytygvtswbcjuinn"  # gmail app password

def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✅ EMAIL SENT TO:", to_email)

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
