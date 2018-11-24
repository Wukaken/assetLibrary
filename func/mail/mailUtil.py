import os
import smtplib
if os.name == 'nt':
    from email.mime.text import MIMEText
else:
    from email.MIMEText import MIMEText
    

class MailUtils(object):
    def __init__(self):
        self.host = 'smtp.126.com'
        self.user = 'testAssetLib'
        self.pwd = 'tal13579'

        self.sender = 'testAssetLib@126.com'

    def sendMail(self, receivers, mailInfo):
        subject = mailInfo['subject']
        mess = mailInfo['mess']
        
        msg = MIMEText(mess, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ';'.join(receivers)

        smtp = smtplib.SMTP()
        smtp.connect(self.host, 25)
        smtp.login(self.user, self.pwd)
        smtp.sendmail(self.sender, receivers, msg.as_string())
        smtp.quit()
