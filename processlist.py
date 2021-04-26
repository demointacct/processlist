import os
import psutil
import time
from datetime import datetime
import schedule
import csv
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
import yagmail

gmailUser = 'sender@gmail.com'
gmailPassword = 'xxxxxxxxx'
recipient = 'receiver@gmail.com'

def find_processes():
    print("find process")
    logPath = os.path.join( os.getcwd(), datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.mkdir(logPath)    
    procs = list(psutil.process_iter())
    csv_file = r'%s\procLog_%i.csv' % (logPath,int(time.time()))
    with open(csv_file,"w",newline="") as file_writer:
        fields=["Cpu","Memory","Name"]
        writer=csv.DictWriter(file_writer,fieldnames=fields)
        writer.writeheader()
        for proc in procs:
            cpu_percent = proc.cpu_percent()
            mem_percent = proc.memory_percent()
            rss = str(proc.memory_info().rss)
            vms = str(proc.memory_info().vms)
            name = proc.name
            writer.writerow({"Cpu":cpu_percent,"Memory":mem_percent,"Name":name})

def send_csv_files():
    file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    zip_file_name = file_name + ".zip"
    zipped_file = zipfile.ZipFile(file_name + ".zip", "w")

    for file in os.listdir(os.curdir):
        dir_curr_date = datetime.now().strftime('%Y-%m-%d_%H')
        if os.path.isdir(os.curdir+'/'+file) and file.startswith(dir_curr_date):
            for f in os.listdir(os.curdir+'/'+file):
                if not(os.path.isdir(os.curdir+'/'+file+'/'+f)):
                    zipped_file.write(file+'\\'+f)
    try:        
        yag = yagmail.SMTP(user=gmailUser, password=gmailPassword)
        yag.send(to=recipient, subject='Sending Attachment', contents='Please find the attached', attachments=os.path.join( os.getcwd(), zip_file_name))
  
        print ('Email sent!')
    except Exception as e:
        print (e)

schedule.every(3).minutes.do(find_processes)
schedule.every(15).minutes.do(send_csv_files)

while 1:
    schedule.run_pending()
    time.sleep(1)


