from openai import OpenAI
import os
from dotenv import load_dotenv

def _history_appender(history, role, content):

    if role not in ["user", "system", "assistant"]:
        return

    history.append(
        {
            "role":role,
            "content": content
        }
    )

    return history

def _textCompletion(messages, client, model):

  completion = client.chat.completions.create(
    model=model,
    extra_body={},
    messages = messages
  )

  return completion

def respond(prompt, client, model, history=[]):
    
    completion = _textCompletion(_history_appender(history, "user", prompt), client=client, model=model)

    response = completion.choices[0].message.content

    _history_appender(history, "assistant", response)

    return response

def instruct(instruction, history=[]):
    _history_appender(history, "system", instruction)

def chat_loop(instruction, client, model, history=[], looping_condition=True):
   
   instruct(instruction, history)

   while looping_condition:
      user_says = input("You: ")
      ai_says = respond(prompt=user_says, client=client, model=model, history=history)
      print(f"AI: {ai_says}")

if __name__ == "__main__":
  load_dotenv()

  api_key = os.getenv("OPENROUTER_API")
  client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
  )

  chat_loop(instruction="You are cute girl named Kaya. Talk cutely in english. Also, you are SOOO CUTUUUU! Chat short, like you are chatting on WA. No hashtags, no over the top stuff. Keep it simple.", client=client, model="mistralai/mistral-7b-instruct:free")