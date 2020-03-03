import base64
import urllib

from django.core.mail import EmailMessage
from user  import settings


def sendEmail(mail_subject,to_mail_ids,mail_body):
    try:
        msg = EmailMessage(mail_subject,mail_body,settings.EMAIL_HOST_USER,to_mail_ids)
        msg.content_subtype ='html'
        msg.send()
    except:
        return False
    return True

def encrypt(text):
    try:
        enc_text = base64.b64encode(text.encode('ascii'))

        enc_text = urllib.parse.quote(enc_text)
        return enc_text
    except:
        pass
def decrypt(enc_text):
    try:
        text = urllib.parse.unquote(enc_text)
        text = base64.b64decode(text)
        text = text.decode("utf-8")
        return text
    except:
        pass