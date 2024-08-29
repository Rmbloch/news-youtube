import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CLIENT_SECRETS_FILE = "client_secret_626888950265-28j9q2tq8j5noe3jh74t2udf5mlodi85.apps.googleusercontent.com(1).json"  # Replace with the path to your client secrets file
TOKEN_PICKLE_FILE = "token.pickle"

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available do the redirect stuff
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run TOKEN PICkLE lol
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

if __name__ == "__main__":
    get_authenticated_service()