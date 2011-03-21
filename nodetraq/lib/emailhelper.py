import smtplib

from email.mime.text import MIMEText

def send_email(message, subject,
              email_from='DO.NOT.REPLY@yourdomain.accounts',
              email_to=[], server='localhost', port='25'):

    if not isinstance(email_to, list):
        email_to = [email_to]
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = ", ".join(email_to)
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(email_from, email_to, msg.as_string())
    return True
