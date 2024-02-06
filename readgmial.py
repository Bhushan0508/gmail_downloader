from googleapiclient.discovery import build
from datetime import datetime, timedelta


from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Replace with your downloaded credentials JSON file path
CREDENTIALS_FILE = 'credentials.json'

# Define scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def get_credentials(SCOPES):
    credentials_file = 'credentials.json'

    # Build the service object using the credentials file
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']  # Replace with needed scopes
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes=scopes)
    credentials = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=credentials)
    print(credentials)
    return credentials
    
def fetch_emails_from_today():
    """
    Fetches Gmail messages from the current date using the Gmail API.

    Returns:
        list: A list of dictionaries, each representing a fetched email.
    """

    # Authenticate and build Gmail service
    gmail_service = build('gmail', 'v1', credentials=get_credentials(SCOPES))

    # Get today's date and convert to RFC 3339 format
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Define search query to filter messages from today only
    query = f'after:{today} before:{tomorrow}'

    try:
        # Use the 'users.messages.list' method to fetch messages
        response = gmail_service.users().messages().list(
            userId='me', q=query, maxResults=10).execute()
        messages = response.get('messages', [])

        # Extract relevant information from each message
        fetched_emails = []
        for message in messages:
            message_id = message['id']
            snippet = message.get('snippet')
            fetched_emails.append({'id': message_id, 'snippet': snippet})

        return fetched_emails

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Fetch and print emails from today
emails = fetch_emails_from_today()
for email in emails:
    print(f"Email ID: {email['id']}, Snippet: {email['snippet']}")