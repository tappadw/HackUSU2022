import datetime
from datetime import timedelta
import finnhub
import json
import os
import pandas as pd
import pandas_datareader as pdr
import requests
import schedule
import smtplib
import time
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

finnhub_client = finnhub.Client(api_key="c8qjaoqad3ienapjn90g")

stonk_list = []

stonks = ['AMZN', 'AMD', 'AAPL','BRK.A', 'DIS', 'GOOG', 'MSFT']


#Logic for running the api call and saving results to JSON
def saveJSON():
    #Gets the current stock price
    for stonk in stonks:
        minute_info = finnhub_client.quote(stonk) #Replace with stonk when complete
    
    with open('/home/ubuntu/environment/StockPrices.json','a') as outfile:
        outfile.write(json.dumps(minute_info)+stonk)
        outfile.write(",")



def sendEmail():
    fromaddr = "HackUSU2022.AWS@gmail.com"
    toaddr = "tappadw@gmail.com"
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    msg['From'] = fromaddr
    
    # storing the receivers email address 
    msg['To'] = toaddr
    
    # storing the subject 
    msg['Subject'] = "If you are seeing this it worked"
    
    # string to store the body of the mail
    body = "You are an egg and your stock is not stonks. You should never trade stonks again."
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # open the file to be sent 
    filename = "price_stock_graph.png"
    attachment = open("/home/ubuntu/environment/price_stock_graph.png", "rb")
    
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(fromaddr, "#HackUSU2022")
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    
    # terminating the session
    s.quit()


  
#Official Schedule Code
#If t is between 9:00 AM and 4:00 PM ET, then this runs and sends the email.
t = datetime.datetime.now()

start_time = '07:00:00.00'
start = datetime.datetime.strptime(start_time, '%H:%M:%S.%f')

end_time = '14:00:00.00'
end = datetime.datetime.strptime(end_time, '%H:%M:%S.%f')

for stonk in stonks:
    if start <= t: #<= end:
        
        scheduler1 = schedule.Scheduler()
        
        scheduler1.every(30).minutes.do(saveJSON)
        print("saveJSON Working")
        scheduler1.every(30).minutes.do(sendEmail)
        print("sendEmail Working")
    else:
        print("Trading has ended for the day")
        break


    while True:
        scheduler1.run_pending()
        time.sleep(1)