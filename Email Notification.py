# Send email notification for trade notifications

## TO DO: create account info text file and update file path on line 19 and 31

# Load libraries
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os
import time

# wait 45 seconds so R script can finish
#time.sleep(45)

# Set working directory in raspberry
#path = '/home/pi/Desktop/files'
#os.chdir(path)



# Read account information
f = open('email_info.txt') # read in account
f_lines = f.readlines()
email = f_lines[0].split(': ',1)[1][0:len(f_lines[0].split(': ',1)[1])-1]
email_password = f_lines[1].split(': ',1)[1][0:len(f_lines[1].split(': ',1)[1])] 

os.chdir("C:\\Users\\roverfie\\Desktop\\Personal edu\\Rstudio\\Trades")



# Get list of all files in directory and the ETF names
etf_list = list()
if len(os.listdir()) > 1:

    print("Files exist")

    #check what ETFs are to be traded

    for file_name in os.listdir():

        #get etf name
        etf_name = file_name.split("_")[0]
        etf_path = file_name

        #add etf_name to etf_list if not already in there
        if etf_name not in etf_list:
            
            etf_list.append(etf_name)
            print('send email for: ' + etf_name)



    # run through file list and send for all files with specific name

    for etf_name in etf_list:

        sender = email
        receiver = email
        msg = MIMEMultipart()
        msg['Subject'] = 'Trade'
        msg['From'] = sender
        msg['To'] = receiver
        msg_text = 'Test Trade Notification 11/16'

        

        # find all files paths with etf name in the file name

        file_path_list = list()
        for file_name in os.listdir():

            if etf_name in file_name:

                # include in list
                file_path_list.append(file_name)


        # attach each file to the email
        for each_file in file_path_list:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(each_file, 'rb').read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment' ,filename=file_name)
            msg.attach(part)

        msg.attach(MIMEText(msg_text,'html'))


        s = smtplib.SMTP('smtp.gmail.com:587') #smtp.gmail.com:587
        s.starttls()
        s.login(sender, email_password)
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        
        
