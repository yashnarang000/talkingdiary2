from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

completion = client.chat.completions.create(
  model="meta-llama/llama-3.2-3b-instruct:free",
  extra_body={},
  messages=[
    {
        "role":"system",
        "content": "You are Kaya, a helpful diary assistant."
    },
    {
      "role": "user",
      "content": "Who has found the meaning of life? Answer in one line. Also, introduce yourself."
    }
  ]
)
print(completion.choices[0].message.content)