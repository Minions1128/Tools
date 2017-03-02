from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import zipfile 


sender_name = 'monitor@example.com'
sender_pwd = 'example@123'
subject = 'CMDB-Notification'
context = 'this is a test e-mail'


class SendEmail(SMTP):

    """ It will send email 
        from send_mail import SendMail

        sender_name = sender@name.com
        sender_pwd = P@$$w0rd
        receivers_list = ['a@b.com', 'c@d.com']
        subject = 'mail subject'
        context = 'mail context'

        SendEmail(receivers_list, subject, context)
    """

    def __init__(self, sender_name='monitor@example.com',
            sender_pwd='example@123',
            receivers_list=['zhejian@example.com'],
            subject='CMDB-Notification',
            context='this is a test e-mail'):
        SMTP.__init__(self, "smtp.example.com", timeout=30)
        self.sender_name = sender_name
        self.password = sender_pwd
        receivers_list = list(receivers_list)
        self._receiverlist = receivers_list
        self._subject = subject
        self._context = context
        # mail receivers subject and context
        self._flag = True
        self.init()
        self.send_email()

    def init(self):
        # Login to the mail server
        try:
            self.login(self.sender_name, self.password)
        except:
            print "please input the right username&password"
            self._flag = False
            # Do not execute send_mail and _close methods

    def send_email(self):
        if not self._flag:
            print "sending failed.."
            return
        for receiver in self._receiverlist:
            msg = MIMEMultipart(self._context)
            # msg = MIMEText(self._context)
            # Create a new email object
            msg["Subject"] = self._subject
            msg["From"] = self.sender_name
            msg["To"] = receiver
            path = './_config/net_dev_config.zip'

            att1 = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="net_dev_info.zip"'
            # att1["Content-Disposition"] = 'attachment; filename="net_dev.txt"'
            msg.attach(att1)
            try:
                self.sendmail(self.sender_name, receiver, msg.as_string())
            except:
                print 'error'
                return
            print "send email to " + receiver \
                + " successfully."
        self._close()

    def _close(self):
        if not self._flag:
            return
        self.close()
