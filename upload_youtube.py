from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import socket
import os
import pickle
import pytz
from thumbnail import ThumbnailGenerator

socket.setdefaulttimeout(1800)

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
TOKEN_PICKLE_FILE = "token.pickle"

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials found")

    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_file, description, tags, title, image_1, image_2):
    youtube = get_authenticated_service()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
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
        f" Daily Global News\n {(datetime.now(pytz.timezone('America/Los_Angeles'))).strftime('%Y-%m-%d')}",
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

def upload_short(video_file, description, tags, title):
    youtube = get_authenticated_service()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
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