import pprint
import openai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

api_key = 'AIzaSyB5wNyphqfJyzU8Yc16y7Ws38832_K1iBQ'
api_serv_name = 'youtube'
api_version = 'v3'
openai.api_key = ''

youtube = build('youtube', 'v3', developerKey=api_key)

def search(query):
    req = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=50,
        order='relevance',
        type='video',
    )

    response = req.execute()
    return response

def get_yt_link(video_id):
    return f'https://www.youtube.com/watch?v={video_id}'

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ""
    for txt in transcript:
        text += txt["text"] + " "
    return text

results = search('top anime fights')

video_id = results['items'][0]['id']['videoId']
print(video_id)
print(get_yt_link(video_id))
pprint.pprint(get_transcript(video_id))
