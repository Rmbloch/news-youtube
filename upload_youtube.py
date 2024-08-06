from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config import CLIENT_SECRETS_FILE
import socket
import pytz
from thumbnail import ThumbnailGenerator

socket.setdefaulttimeout(1800)

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
REFRESH_TOKEN = "1//06U_XNcBRO4sXCgYIARAAGAYSNwF-L9IrTqGPn_i6s2Z7DyCP0WVMOr2KyO0NBYFlMisXhjeQri3ZPsZeJ65Auf9sRiaW9gotYZE"

def get_authenticated_service():
    # Load client secrets
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

    # Use the refresh token to get new credentials
    credentials = Credentials.from_authorized_user_info(
        {
            "client_id": flow.client_config['client_id'],
            "client_secret": flow.client_config['client_secret'],
            "refresh_token": REFRESH_TOKEN
        },
        SCOPES
    )

    # If the credentials are expired, refresh them
    if credentials.expired:
        credentials.refresh(Request())

    return build('youtube', 'v3', credentials=credentials)

def upload_to_youtube(video_file, description, tags, thumbnail, image_1, image_2):
    youtube = get_authenticated_service()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"Daily Global News {(datetime.now(pytz.timezone('America/Los_Angeles')) - timedelta(days=1)).strftime('%Y-%m-%d')}",
                "description": description,
                "tags": tags,
                "categoryId": "25"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_file)
    )
    response = request.execute()

    thumbnail_generator = ThumbnailGenerator()
    thumbnail_generator.generate(
        f" Daily Global News\n {(datetime.now(pytz.timezone('America/Los_Angeles')) - timedelta(days=1)).strftime('%Y-%m-%d')}",
        'LEMONMILK-MediumItalic.otf',
        image1=image_1,
        image2=image_2
    )

    video_id = response['id']
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload('thumbnail.jpg', mimetype='image/jpeg')
    ).execute()
    return response
