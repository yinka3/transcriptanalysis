import pprint
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
youtube = build('youtube', version='v3', developerKey=os.environ.get('GOOGLE_API_KEY'))

prompt_content = """You are to conduct Deep fact-check and will always response with JSON.
You should search on the internet or use model knowledge to fact-check the following transcript.
Analyze any factual errors, inconsistencies, or misleading statements but no need to output it.
Finally, output a score ranging from 0 to 100, where 100 is the most accurate and 0 is completely wrong.
Justify your score based on the number and severity of the errors found.
Your JSON response must adhere to the following schema:

{
    "video_link": "string",
    "analysis": "string",
    "final_score": "number"
}

For example:
{
    "video_link": "https://www.youtube.com/watch?v=video_id",
    "analysis": "This is an example of a justification analysis of score.",
    "final_score": 75
}"""



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

def format_transcript(link, transcript):

    final_text = f"""
        Here is the youtube link for the video to fact-check: {link}
        This is the transcript, you can verify if there are any missing information before giving the score on accuracy:
        Transcript: {transcript}"""

    return final_text


# Hard checking for now
results = search('top anime fights')
video_id = results['items'][0]['id']['videoId']
video_link = get_yt_link('Z3Aje4GcURA&ab')
transcript = get_transcript('Z3Aje4GcURA&ab')
text = format_transcript(video_link, transcript)
response = client.models.generate_content(
    model='gemini-2.0-pro-exp-02-05',
    contents=text,
    config=types.GenerateContentConfig(
        system_instruction=prompt_content,
        temperature=0.2,
        top_p=0.95,
        top_k=32,
        candidate_count=1,
        seed=6,
        max_output_tokens=1500,
        presence_penalty=0.0,
        frequency_penalty=0.0
    ),
)

pprint.pprint(response.text)

