import os

from google.auth.external_account_authorized_user import (
    Credentials as ExternalCredentials,
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.json"


def get_credentials() -> Credentials | ExternalCredentials:
    """
    Return the credentials to use the API
    """
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    return credentials
