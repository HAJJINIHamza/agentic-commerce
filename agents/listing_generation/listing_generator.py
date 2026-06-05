import requests
import json 
import os 
from dotenv import load_dotenv

#env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

response = requests.post(
    url = "https://openrouter.ai/api/v1/chat/completions",
    headers= {
        "Authorization": F"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        #"HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        #"X-OpenRouter-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    data = json.dumps({
        "model" : "meta-llama/llama-3.3-70b-instruct:free",
        "messages" : [
            { "role" : "user",
              "content" : "What are you ? how can you be usefull to me ?" }
        ]
    }
  )
)

