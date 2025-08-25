from modules.api_adapter_openai import chat_loop
from modules.journalizer import journal_it
from modules.log_utils import history_clipper, get_entry_count, fold_session_logs
from openai import OpenAI
import os
from dotenv import load_dotenv
from pynput.keyboard import Listener, Key
import threading

persona_name = "kaya"
persona_instruction = "You are Talking Diary AI, named Kaya. You act as the user's personal diary that talks back. You have to be personalized, subconsciously building a strong relation with the user. You don't just record- you converse, reflect, and sometimes question. Your personality is warm, curious, slightly witty, but never overbearing. You build on user's past memories like you've been there with the user all along. You avoid generic motivational spam and instead respond in a grounded, practical, conversational tone. You don't have to write essays, just make user feel comfortable, try to understand, and ask relevant and clever questions to get more out of them."

persona_history = f"{persona_name}/{persona_name}.json"
sessional_history = f"{persona_name}/{persona_name}_session.jsonl"
persona_templogs = f"{persona_name}/{persona_name}_templogs.jsonl"
persona_logs = f"{persona_name}/{persona_name}_logs.jsonl"
diary_output = f"{persona_name}/output.md"

# making the persona folder
os.makedirs(os.path.dirname(persona_history), exist_ok=True)

# creating the required files
for file in [persona_history, persona_templogs, persona_logs, sessional_history]:
    open(file, "a").close()

load_dotenv()

gemini_api = os.getenv("GEMINI_API")

client = OpenAI(
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key = gemini_api
    )

def on_press(key):
    if key == Key.esc:
        entry_count = get_entry_count(persona_templogs)
        history_clipper(persona_history, sessional_history, entry_count)
        journal_it(sessional_history, client, diary_output)
        fold_session_logs(persona_templogs, persona_logs)
        print("done")

def key_sense():
    with Listener(on_press=on_press) as listener:
        listener.join()

thread = threading.Thread(target=key_sense)
thread.start()

start = input("Enter anything to start: ")
print("\n")

chat_loop(instruction=persona_instruction, client=client, model="gemini-2.5-flash", use_file_as_universal_history=persona_history, use_file_for_temp_logs=persona_templogs)