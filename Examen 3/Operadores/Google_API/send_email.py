from .Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_email(message):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg = message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'jaimetr97@gmail.com'
    mimeMessage['subject'] = 'Duda - Aplicativo Scanner Online'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    try:
        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(message)
        return True
    except errors.HttpError:
        return False
