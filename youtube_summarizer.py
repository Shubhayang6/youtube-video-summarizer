import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Loads all environment variables
load_dotenv()

# Configuring API keys
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = '''
    Imagine yourself as an youtube video summarizer. You will be taking the transcript text and summarize the entrire video and providing the important summary in points within 250 words The transctipt text will be appended here:
    '''

# Extracting the transcript data fro Youtube Videos
def extract_transcription(url):
    try:
        video_url = url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_url)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        
        return transcript
    
    except Exception as e:
        print(f"Error occured due to {e}")
        
        
# Summarizing the prompt with Gemini   
def generate_gemini_content(transcript_text, prompt):
    
    model =  genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Enter the youtube URL:")

if youtube_link:
    video_url = youtube_link.split("=")[1]
    st.image(f'http://img.youtube.com/vi/{video_url}/0.jpg', use_container_width=True)
    print(video_url)

if st.button("Get transcript"):
    transcript_text = extract_transcription(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Here is your transcription:")
        st.write(summary)
    