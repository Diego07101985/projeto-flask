import smtplib
from email.header import Header
from email.mime.text import MIMEText


class ServiceEmail:
    def __init__(self, mail_from,
                 mail_to,
                 mail_username,
                 mail_password,
                 mail_subject,
                 mail_message):

        self.mailInfo = {
            "from": mail_from,
            "to": mail_to,
            "username": mail_username,
            "password": mail_password,
            "mailsubject": mail_subject,
            "mailtext": mail_message,
            "mailencoding": "utf-8"
        }

    def sendEmail(self):
        msg = MIMEText(self.mailInfo["mailtext"])
        msg["Subject"] = Header(self.mailInfo["mailsubject"],
                                self.mailInfo["mailencoding"])
        msg["from"] = self.mailInfo["from"]
        msg["to"] = self.mailInfo["to"]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(self.mailInfo["username"], self.mailInfo["password"])
        server.sendmail(self.mailInfo["from"],
                        self.mailInfo["to"], msg.as_string())
        server.quit()
