from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
import os
from googleapiclient.errors import HttpError
import base64

gmail_service = None
def init_gmail():
    global gmail_service
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     'client_secrets.json', scopes=['https://www.googleapis.com/auth/drive.readonly']
    # )
    # credentials = flow.run_local_server(port=0)
    # print('Credentials:=',credentials)
    creds = None
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send'
              ,'https://www.googleapis.com/auth/gmail.compose']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token_gmail.json"):
        creds = Credentials.from_authorized_user_file("token_gmail.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token_gmail.json", "w") as token:
                token.write(creds.to_json())
    gmail_service = build('gmail', 'v1', credentials=creds)

init_gmail()
# Replace with your downloaded credentials file path

try:
    user_id = "me"  # Replace with "me" or specific user ID
    results = gmail_service.users().messages().list(userId=user_id, q='from: dhanvantarict@gmail.com","hr.ctscan@gmail.com","info@matrix-healthcare.in').execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
    else:
        # Iterate through messages and use `users.messages.get` for details
        for message in messages:
            message_id = message["id"]
            print(message_id)
            # Retrieve specific message details here
            # ...
            txt = gmail_service.users().messages().get(userId='me', id=message_id).execute() 

            # Use try-except to avoid any Errors 
            try: 
                # Get value of 'payload' from dictionary 'txt' 
                payload = txt['payload'] 
                headers = payload['headers'] 
    
                # Look for Subject and Sender Email in the headers 
                for d in headers: 
                    if d['name'] == 'Subject': 
                        subject = d['value'] 
                    if d['name'] == 'From': 
                        sender = d['value'] 
    
                # The Body of the message is in Encrypted format. So, we have to decode it. 
                # Get the data and decode it with base 64 decoder. 
                #parts = payload.get('parts')[0] 
                #data = parts['body']['data'] 
                #data = data.replace("-","+").replace("_","/") 
                #decoded_data = base64.b64decode(data) 
    
                # Now, the data obtained is in lxml. So, we will parse  
                # it with BeautifulSoup library 
                #soup = BeautifulSoup(decoded_data , "lxml") 
                #body = soup.body() 
    
                # Printing the subject, sender's email and message 
                print("Subject: ", subject) 
                print("From: ", sender) 
                #print("Message: ", body) 
                print('\n') 
            except: 
                pass
            
except HttpError as error:
    print(f"An error occurred: {error}")
    
try:
    message_id = "1234567890"  # Replace with the desired message ID
    message = gmail_service.users().messages().get(userId=user_id, id=message_id).execute()
    print(f"Message subject: {message['snippet']}")
    # Explore `message` dictionary for content, sender, attachments, etc.
except HttpError as error:
    print(f"An error occurred: {error}")