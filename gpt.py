from openai import OpenAI
import os  # Import the os module
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




# Load environment variables from the .env file
load_dotenv()

# Set OpenAI API key from environment variable

def get_transcript(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    output = ''
    for x in transcript:
        sentence = x['text']
        output += f'{sentence}\n'
    return output

def check_facts(subtitles):
    prompt = f"You are the AI fact-checker. I will provide you with some prompts, and your task is to determine whether they are true or false. This is a political debate, so you must indicate who is telling the truth and who is not by starting with their statement, followed by whether it is true or false. For example: 'Trump or Harris' - their statement - It must be either true or false, not partially true or partially false, and include the number in front. {subtitles}"
    try:
        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI factchekcer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during GPT fact check: {e}")
        return "Error checking facts"

def main():
    video_url = 'https://www.youtube.com/watch?v=B6Pc6YRgDqo'
    print(f"Fetching transcript for: {video_url}")
    transcript = get_transcript(video_url)
    print("Transcript fetched.")
    print("Checking facts...")
    result = check_facts(transcript)
    print("Fact-checking result:")
    print(result)

if __name__ == "__main__":
    main()
