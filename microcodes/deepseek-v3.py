from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API")

client = OpenAI(
base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
api_key=api_key,
)

completion = client.chat.completions.create(
  model="gemini-2.5-flash",
  messages=[
    {
        "role":"system",
        "content": "You are Kaya, a helpful diary assistant."
    },
    {
      "time": "12 am fuck off",
      "role": "user",
      "content": "Who are you and introduce yourself in a little bit of detail.",
    }
  ]
)
print(completion.choices[0].message.content)