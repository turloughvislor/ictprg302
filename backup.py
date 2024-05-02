#!/usr/bin/python3 # shebang. Allows code to execute without typing python in the terminal.
"""
Script title: backup.py
Author: Kassandra Owen
Author email: kassie.owen@live.com
Version control: 1

"""
# imports libraries
import sys #import system library for command line arguments
import os #import operating system library for file system operations 
import pathlib #import path library for file system paths
import shutil #imports library that allows file opererations. Allows copying and moving files.
import smtplib #imports library for email function
from datetime import datetime #import date and time stamp variable 
from backupcfg import jobs, dstPath, logPath, smtp #imports configurations from backupcfg

#Function to send email notifications with error message and date time stamp.

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
    try: #tests this block of code unless there is an exception 
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo() #informs server it is a smtp client
        smtp_server.starttls() #encrypts message
        smtp_server.ehlo() #informs server it is a smtp client again
        smtp_server.login(smtp["user"], smtp["password"]) #logs in to email server
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email) #sends the email message
        smtp_server.close() #terminates connection to server
    except Exception as e: #exception. will print error message on screen if above code failed.
        print("ERROR: Send email failed: " + str(e), file=sys.stderr)
        
        #function to log errors and error messages
def log(errorMessage):
    try: #executes log file writing code unless there is an exception
        file = open(logPath, "a") #opens file in logPath
        
        file.write(f"{errorMessage}.\n") #writes error message in log file
       
        file.close() #closes log file
    except FileNotFoundError: #exception occurs if log file is not found
        print("ERROR: File does not exist.") #prints error message if log file not found exception occurs
    except IOError: #exception if file path is not correct
        print("ERROR: File is not accessible.") #prints error message if file path not correct

#error handling function. prints error message and sends error message to log file with date time stamp
def error(errorMessage, dateTimeStamp): 
    print(f"{errorMessage}") #prints error message
    log(f"FAILURE: {errorMessage}, {dateTimeStamp}") #writes error message to log file
    sendEmail(errorMessage, dateTimeStamp) #sends email with error message
    
def main(): #main function of program. Backs up file1 to backup.log when executed without error
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S") #gets current date time stamp
    argCount = len(sys.argv) #checks command line arguments
    if argCount != 2:#counts arguments. if arg count is not equal to 2, an error occurs.
        error("ERROR: jobname missing from command line", dateTimeStamp) #error handling if arg count is not equal to 2.
    else: #error handling if exception occurs
        jobName = sys.argv[1] #counts arguments
        if jobName not in jobs: #error handling for incorrect job name entered
            error(f"ERROR: jobname {jobName} not defined.", dateTimeStamp) #prints and logs that jobname is not defined
        else:   #exception if srcpath error
            for srcPath in jobs[jobName]: #looping function
                if not os.path.exists(srcPath): #checks if path doesn't exist
                    print(f"ERROR: Source path {srcPath} does not exist.") #prints error message if srcpath doesn't exist
                else: #exception if srcpath does exist but destination path does not exist
                    if not os.path.exists(dstPath): #checks if dstpath does not exist
                        error(f"ERROR: Destination path {dstPath} does not exist.", dateTimeStamp) #prints error message if dstpath doesn't exist
                    else: #exception if srcpath and dstpath exist
                        srcDetails = pathlib.PurePath(srcPath) #gets source path details
                         
                        dstLoc = f"{dstPath}/{srcDetails.name}-{dateTimeStamp}" #points to destination location
                         
                        if pathlib.Path(srcPath).is_dir(): #copies directory
                            shutil.copytree(srcPath, dstLoc)
                        else:
                            shutil.copy2(srcPath, dstLoc) #copies file
                            #files and directories successfully are backed up to backups directory
                            
                        log(f"SUCCESS: Backed up {srcPath} to {dstLoc}, {dateTimeStamp}") #writes to log that files and directory were successfully backed up with date time stamp
                            
                           
                        
                    
                    
                
                
if __name__ == '__main__':
    main()