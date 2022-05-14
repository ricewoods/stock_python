import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import json

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    msg.atttach(MIMEText(body))
    return msg

def send(from_addr, to_addrs, msg, my_password):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587) # GmailのSMTPサーバーへ
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, my_password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

def mailjob():
    with open('secret.json') as f:
        info = json.load(f)
        
    FROM_ADDRESS = info['email']
    MY_PASSWORD = info['password']
    
    TO_ADDRESS = 'ricewoods@gmail.com'
    BCC = ''
    SUBJECT = '国内外マーケット指標'
    BODY = '本日の結果になります。'
    attachment = MIMEApplication(df.read())
    attachment.add_header("Content-Disposition", "attachment", filename="market.csv")
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)
