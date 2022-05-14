#!/usr/bin/env python
# coding: utf-8

# In[1]:
def execution(event, context):

    import requests
    from bs4 import BeautifulSoup


    # In[2]:


    url = 'https://www.rakuten-sec.co.jp/web/market/data/list.html'


    # In[3]:


    res = requests.get(url)


    # In[4]:


    soup = BeautifulSoup(res.content, "html.parser")


    # In[5]:


    #elems = soup.find_all('tr')
    elems = soup.find_all('th')
    elems


    # In[6]:


    titles = []
    for elem in elems:
        try:
            title = elem.contents[1].text
            titles.append(title)
        except:
            continue


    # In[7]:


    pickup_links = []
    for elem in elems:
        try:
            pickup_links.append("https://www.rakuten-sec.co.jp" + elem.find('a').get('href'))
        except:
            continue


    # In[8]:


    pickup_links2 = []
    for url in pickup_links:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('iframe')
            pickup_links2.append(elems[0].get('src'))
        except:
            continue


    # In[9]:


    link2 = requests.get(pickup_links2[0])
    soup = BeautifulSoup(link2.content, "html.parser")
    elems3 = soup.find_all('td')


    # In[10]:


    market = []
    for url in pickup_links2:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('td')
            rmove = elems[0].text
            market.append(rmove.replace('\n', "").replace('\r', "").replace('\xa0', "").replace('\t', ""))
        except:
            continue


    # In[65]:


    import pandas as pd
    import numpy as np
    import os
    df = pd.DataFrame(list(zip(titles,market)),columns = ['index', 'rate'])


    # In[71]:


    #先頭および末尾のスペースを削除し、カッコ内の値をカッコもろとも削除
    df['rate'] = df['rate'].replace({'\s':'', "\(.*\)":""},regex=True)

    # In[72]:

    if not os.path.isdir('/tmp/'):
        os.mkdir('/tmp/')

    df.to_csv('/tmp/market.csv')

    mailjob()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import json

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
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
    
    with open(r"/tmp/market.csv", "rb") as f:
        attachment = MIMEApplication(f.read())

    attachment.add_header("Content-Disposition", "attachment", filename="market.csv")
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    msg.attach(attachment)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)



#!/usr/bin/env python
# coding: utf-8

# In[1]:
def execution(event, context):

    import requests
    from bs4 import BeautifulSoup


    # In[2]:


    url = 'https://www.rakuten-sec.co.jp/web/market/data/list.html'


    # In[3]:


    res = requests.get(url)


    # In[4]:


    soup = BeautifulSoup(res.content, "html.parser")


    # In[5]:


    #elems = soup.find_all('tr')
    elems = soup.find_all('th')
    elems


    # In[6]:


    titles = []
    for elem in elems:
        try:
            title = elem.contents[1].text
            titles.append(title)
        except:
            continue


    # In[7]:


    pickup_links = []
    for elem in elems:
        try:
            pickup_links.append("https://www.rakuten-sec.co.jp" + elem.find('a').get('href'))
        except:
            continue


    # In[8]:


    pickup_links2 = []
    for url in pickup_links:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('iframe')
            pickup_links2.append(elems[0].get('src'))
        except:
            continue


    # In[9]:


    link2 = requests.get(pickup_links2[0])
    soup = BeautifulSoup(link2.content, "html.parser")
    elems3 = soup.find_all('td')


    # In[10]:


    market = []
    for url in pickup_links2:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('td')
            rmove = elems[0].text
            market.append(rmove.replace('\n', "").replace('\r', "").replace('\xa0', "").replace('\t', ""))
        except:
            continue


    # In[65]:


    import pandas as pd
    import numpy as np
    import os
    df = pd.DataFrame(list(zip(titles,market)),columns = ['index', 'rate'])


    # In[71]:


    #先頭および末尾のスペースを削除し、カッコ内の値をカッコもろとも削除
    df['rate'] = df['rate'].replace({'\s':'', "\(.*\)":""},regex=True)

    # In[72]:

    if not os.path.isdir('/tmp/'):
        os.mkdir('/tmp/')

    df.to_csv('/tmp/market.csv')

    mailjob()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import json

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
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
    
    with open(r"/tmp/market.csv", "rb") as f:
        attachment = MIMEApplication(f.read())

    attachment.add_header("Content-Disposition", "attachment", filename="market.csv")
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    msg.attach(attachment)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)



#!/usr/bin/env python
# coding: utf-8

# In[1]:
def execution(event, context):

    import requests
    from bs4 import BeautifulSoup


    # In[2]:


    url = 'https://www.rakuten-sec.co.jp/web/market/data/list.html'


    # In[3]:


    res = requests.get(url)


    # In[4]:


    soup = BeautifulSoup(res.content, "html.parser")


    # In[5]:


    #elems = soup.find_all('tr')
    elems = soup.find_all('th')
    elems


    # In[6]:


    titles = []
    for elem in elems:
        try:
            title = elem.contents[1].text
            titles.append(title)
        except:
            continue


    # In[7]:


    pickup_links = []
    for elem in elems:
        try:
            pickup_links.append("https://www.rakuten-sec.co.jp" + elem.find('a').get('href'))
        except:
            continue


    # In[8]:


    pickup_links2 = []
    for url in pickup_links:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('iframe')
            pickup_links2.append(elems[0].get('src'))
        except:
            continue


    # In[9]:


    link2 = requests.get(pickup_links2[0])
    soup = BeautifulSoup(link2.content, "html.parser")
    elems3 = soup.find_all('td')


    # In[10]:


    market = []
    for url in pickup_links2:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('td')
            rmove = elems[0].text
            market.append(rmove.replace('\n', "").replace('\r', "").replace('\xa0', "").replace('\t', ""))
        except:
            continue


    # In[65]:


    import pandas as pd
    import numpy as np
    import os
    df = pd.DataFrame(list(zip(titles,market)),columns = ['index', 'rate'])


    # In[71]:


    #先頭および末尾のスペースを削除し、カッコ内の値をカッコもろとも削除
    df['rate'] = df['rate'].replace({'\s':'', "\(.*\)":""},regex=True)

    # In[72]:

    if not os.path.isdir('/tmp/'):
        os.mkdir('/tmp/')

    df.to_csv('/tmp/market.csv')

    mailjob()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import json

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
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
    
    with open(r"/tmp/market.csv", "rb") as f:
        attachment = MIMEApplication(f.read())

    attachment.add_header("Content-Disposition", "attachment", filename="market.csv")
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    msg.attach(attachment)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)



#!/usr/bin/env python
# coding: utf-8

# In[1]:
def execution(event, context):

    import requests
    from bs4 import BeautifulSoup


    # In[2]:


    url = 'https://www.rakuten-sec.co.jp/web/market/data/list.html'


    # In[3]:


    res = requests.get(url)


    # In[4]:


    soup = BeautifulSoup(res.content, "html.parser")


    # In[5]:


    #elems = soup.find_all('tr')
    elems = soup.find_all('th')
    elems


    # In[6]:


    titles = []
    for elem in elems:
        try:
            title = elem.contents[1].text
            titles.append(title)
        except:
            continue


    # In[7]:


    pickup_links = []
    for elem in elems:
        try:
            pickup_links.append("https://www.rakuten-sec.co.jp" + elem.find('a').get('href'))
        except:
            continue


    # In[8]:


    pickup_links2 = []
    for url in pickup_links:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('iframe')
            pickup_links2.append(elems[0].get('src'))
        except:
            continue


    # In[9]:


    link2 = requests.get(pickup_links2[0])
    soup = BeautifulSoup(link2.content, "html.parser")
    elems3 = soup.find_all('td')


    # In[10]:


    market = []
    for url in pickup_links2:
        try:
            link = requests.get(url)
            soup = BeautifulSoup(link.content, "html.parser")
            elems = soup.find_all('td')
            rmove = elems[0].text
            market.append(rmove.replace('\n', "").replace('\r', "").replace('\xa0', "").replace('\t', ""))
        except:
            continue


    # In[65]:


    import pandas as pd
    import numpy as np
    import os
    df = pd.DataFrame(list(zip(titles,market)),columns = ['index', 'rate'])


    # In[71]:


    #先頭および末尾のスペースを削除し、カッコ内の値をカッコもろとも削除
    df['rate'] = df['rate'].replace({'\s':'', "\(.*\)":""},regex=True)

    # In[72]:

    if not os.path.isdir('/tmp/'):
        os.mkdir('/tmp/')

    df.to_csv('/tmp/market.csv')

    mailjob()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
import json

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
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
    
    with open(r"/tmp/market.csv", "rb") as f:
        attachment = MIMEApplication(f.read())

    attachment.add_header("Content-Disposition", "attachment", filename="market.csv")
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    msg.attach(attachment)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)


