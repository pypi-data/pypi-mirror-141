import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

class Mail:
    mail = None
    context = MIMEMultipart()
    From = ""
    To = ""
    def __init__(self,host,port,user,Userpass,Mailfrom,Mailto,subject,content):
        self.From = Mailfrom
        self.To = Mailto
        self.mail = smtplib.SMTP()
        self.mail.connect(host,port)
        self.mail.login(user,Userpass)
        self.context['From'] = Header(Mailfrom,"utf-8")
        self.context['To'] = Header(Mailto,"utf-8")
        self.context['Subject'] = Header(subject,"utf-8")
        self.context.attach(MIMEText(content,"plain","utf-8"))
    def AddFile(self,FilePath):
        file = MIMEText(open(FilePath,"rb").readlines(),"base64","utf-8")
        file['Content-Type'] = "application/octet-stream"
        name_spilt = FilePath.spilt(str="\\")
        name = name_spilt[len(name_spilt)]
        file['Content-Disposition'] = "attachment;filename={}".format(name)
        self.context.attach(file)
        return

class MailError(Exception):
    def __init__(self):
        pass
    def what(self):
        return "MailError!"