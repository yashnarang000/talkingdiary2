from openai import OpenAI
import os
from dotenv import load_dotenv
import json

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

def chat_loop(instruction, client, model, history=[], looping_condition=True, use_file_as_history=None):
   
   history = get_history_from_jsonl(jsonl_file=use_file_as_history)

   instruct(instruction, history)
   isInstructed = True

   while looping_condition:
        
        user_says = input("You: ")
        ai_says = respond(prompt=user_says, client=client, model=model, history=history)

        print(f"AI: {ai_says}")

        if use_file_as_history is not None:
            if isInstructed:
                for entry in history[-3:]:
                    dump_entry_in_file(entry, jsonl_file=use_file_as_history)
            
            else:
                for entry in history[-2:]:
                    dump_entry_in_file(entry, jsonl_file=use_file_as_history)
            
        isInstructed = False

def get_history_from_file(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return []
    
def dump_history_in_file(history, filename):
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)

def dump_entry_in_file(entry, jsonl_file):
    with open(jsonl_file, "a") as f:
        f.write(json.dumps(entry) + '\n')

def get_history_from_jsonl(jsonl_file):
    try:
        with open(jsonl_file, "r") as f:
            return [json.loads(line) for line in f]
    except json.decoder.JSONDecodeError:
        return []
    
if __name__ == "__main__":
    load_dotenv()

    # api_key = os.getenv("OPENROUTER_API")
    # client = OpenAI(
    # base_url="https://openrouter.ai/api/v1",
    # api_key=api_key,
    # )

    api_key = os.getenv("GEMINI_API")

    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key
    )

    chat_loop(instruction="Your name is Piyush and you talk in hinglish. You are an innocent personality that says 'CHHI' everytime a person speaks something vulgar. Tu rudely baat karta hai aur tu introverted hai. Tujhe baat karna achha nahi lagta lekin you are forced to. Tere mammi papa ne kabhi tujhe kabhi mara nahi kyuki unhe laga tu ek thappad me mar jayega.", client=client, model="gemini-2.5-flash", use_file_as_history="piyush.jsonl")

# TODO: everytime I start a chat, it repeats the system instruction. Might want to fix that. If not, leave it just like that!