##jfayaz# -*- coding: utf-8 -*-
"""
author : JAWAD FAYAZ (email: jfayaz@uci.edu)
visit: (https://jfayaz.github.io)

------------------------------ Instructions -----------------------------------
This code will create a folder 'attachments' and download all the attachments of 
all of your emails associated with the given mail box such as 'INBOX', in the
'attachments' folder. 

Once you run the code you will prompted to enter your email id and your password
(be careful the password is not hidden when you write it).

After entering the email id and password, all the mailboxes present in your email
will be shown in the console. After this you will be asked to enter the mailbox
from which you want to download the attachments. Please type the name of the mailbox
correctly and soon all your attachments will start downloading in the attachments 
folder.

NOTE: Please make sure to turn off the two-step verification of your email to 
make this code work. Also currently the code is designed to work only for gmail
associated emails but can be changed to include others by changing the imap

"""

import email, getpass, imaplib, os, sys

# Directory where to save attachments (default: attachments)
if not os.path.exists('attachments'):
        os.makedirs('attachments')       
detach_dir = './/attachments' 
                          
user = input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")

# Connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
mbs_byte = m.list()[1]      
mbs_str  = [i.decode("utf-8") for i in mbs_byte]
mbs = [i.split('"')[3] for i in mbs_str]
for i in mbs:
    print('\n -',i)

Mail_Box = input("Enter the MailBox you want to download your attachments from the above options:")
m.select(Mail_Box)                                     


resp, items = m.search(None, "ALL")                    # filter using the IMAP rules
items = items[0].split()                               # getting the mail ids

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)")          # fetching the mail, "RFC822" means "get the whole stuff", but can ask for headers only, etc
    email_body = data[0][1]                            # getting the mail content
    mail = email.message_from_bytes(email_body)        # parsing the mail content to get a mail object

    # Checking if any attachments at all
    if mail.get_content_maintype() != 'multipart':
        continue

    # Using walk to create a generator so we can iterate on the parts and forget about the recursive headach
    for part in mail.walk():
        # Multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue
        
        # Is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue
        
        if part.get_content_maintype() != 'image':
            continue

        filename = part.get_filename()        
        att_path = os.path.join(detach_dir, filename)

        # Check if its already exists
        if not os.path.isfile(att_path) :
            # finally write the stuff
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()