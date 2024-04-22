#!/usr/bin/python3
"""
Script title:
Author: Kassandra Owen
Author email: kassie.owen@live.com
Version control:

"""

import sys
import os
import pathlib
import shutil
import smtplib
from datetime import datetime
from backupcfg import jobs, dstPath, logPath, smtp

def sendEmail(message, dateTimeStamp): 
    """ 
    Send an email message to the specified recipient. 
    Parameters: 
    message (string): message to send. 
    dateTimeStamp (string): Date and time when program was run. 
    """ 
    # create email message 
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n' 
   
    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: Send email failed: " + str(e), file=sys.stderr)

def log(errorMessage):
    try:
        file = open(logPath, "a")
        
        file.write(f"{errorMessage}.\n")
       
        file.close()
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")

def error(errorMessage, dateTimeStamp):
    print(f"{errorMessage}")
    log(f"FAILURE: {errorMessage}, {dateTimeStamp}")
    sendEmail(errorMessage, dateTimeStamp)
    
def main():
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    argCount = len(sys.argv)
    if argCount != 2:
        error("ERROR: jobname missing from command line", dateTimeStamp)
    else:
        jobName = sys.argv[1]
        if jobName not in jobs:
            error(f"ERROR: jobname {jobName} not defined.", dateTimeStamp) 
        else:   
            for srcPath in jobs[jobName]:
                if not os.path.exists(srcPath):
                    print(f"ERROR: Source path {srcPath} does not exist.") #
                else:
                    if not os.path.exists(dstPath):
                        error(f"ERROR: Destination path {dstPath} does not exist.", dateTimeStamp)
                    else: 
                        srcDetails = pathlib.PurePath(srcPath)
                         
                        dstLoc = f"{dstPath}/{srcDetails.name}-{dateTimeStamp}"
                         
                        if pathlib.Path(srcPath).is_dir():
                            shutil.copytree(srcPath, dstLoc)
                        else:
                            shutil.copy2(srcPath, dstLoc)
                            
                        log(f"SUCCESS: Backed up {srcPath} to {dstLoc}, {dateTimeStamp}")
                            
                           
                        
                    
                    
                
                
if __name__ == '__main__':
    main()