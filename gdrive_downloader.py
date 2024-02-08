from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io
import os
# Authentication (replace with your credentials file path)
drive_service = None
def init_gdrive():
    global drive_service
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     'client_secrets.json', scopes=['https://www.googleapis.com/auth/drive.readonly']
    # )
    # credentials = flow.run_local_server(port=0)
    # print('Credentials:=',credentials)
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    drive_service = build('drive', 'v3', credentials=creds)

def download(gdrive_fileid,filename):
    global drive_service
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     'client_secrets.json', scopes=['https://www.googleapis.com/auth/drive.readonly']
    # )
    # credentials = flow.run_local_server(port=0)
    # drive_service = build('drive', 'v3', credentials=credentials)

    # File ID and Download
    file_id = gdrive_fileid #'1MY4SSSEE-DL17ecWmjh5cNWKq2MxN7I8'  # Replace with the ZIP file ID
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO("downloads/"+filename, 'wb')  # Replace with desired filename
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    print("Download complete!")