import Mail as smtp
import smtplib

def SendEMail(Mail):
    try:
        smtp.Mail.mail.sendmail(smtp.Mail.Mail.From,smtp.Mail.To,smtp.Mail.context.as_string())
    except smtplib.SMTPException:
        raise smtp.MailError()
