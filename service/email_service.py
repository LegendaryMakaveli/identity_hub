import smtplib
from email.message import EmailMessage

class EmailService:

    def __init__(self):
        self.email_address = "youremail@gmail.com"
        self.email_password = "App_password"

    def send(self, to_email, subject, message):
        email = EmailMessage()
        email["From"] = self.email_address
        email["To"] = to_email
        email["Subject"] = subject
        email.set_content(message)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(email)

            print("[EMAIL SENT]")

        except Exception as e:
            print("[EMAIL FAILED]:", str(e))
