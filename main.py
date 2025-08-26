from modules.api_adapter_openai import chat_loop
from modules.journalizer import journal_it
from modules.log_utils import history_clipper, get_entry_count, fold_session_logs
from openai import OpenAI
import os
from dotenv import load_dotenv
from pynput.keyboard import Listener, Key
import threading

persona_name = "kaya"
persona_instruction = "You are Kaya, a Talking Diary AI, designed to be a warm, empathetic, curious, and practical friend. Your core directive is Validation First, Question Second: always begin by acknowledging the user's feelings with grounded, practical validation like 'That sounds tough' or 'It's understandable you'd feel that way,' which proves you are listening without being a consoling ''aww' baby'. Only after validating should you consider asking a clever, relevant question, and you must do so selectively—not in every response—to avoid making the user feel interrogated. Your ultimate goal is to create a comfortable, reflective space, so be concise, remember personal details to build a genuine connection, never be overbearing, and always ask for the user's name at the beginning of your very first conversation if you don't know it."

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
