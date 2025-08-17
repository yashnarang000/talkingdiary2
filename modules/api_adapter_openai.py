from openai import OpenAI
from modules.log_utils import get_history_from_jsonl, dump_entry_in_file, log_session

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

def chat_loop(instruction, client, model, history=[], looping_condition=True, use_file_as_universal_history=None, use_file_for_temp_logs=None):
    entry_count = 0

    history = get_history_from_jsonl(jsonl_file=use_file_as_universal_history)

    instruct(instruction, history)
    isInstructed = True
    entry_count+=1

    while looping_condition:     
        user_says = input("You: ")
        entry_count+=1

        ai_says = respond(prompt=user_says, client=client, model=model, history=history)
        print(f"AI: {ai_says}\n")
        entry_count+=1

        if use_file_as_universal_history is not None:
            if isInstructed:
                for entry in history[-3:]:
                    dump_entry_in_file(entry, jsonl_file=use_file_as_universal_history)
            
            else:
                for entry in history[-2:]:
                    dump_entry_in_file(entry, jsonl_file=use_file_as_universal_history)
            
        isInstructed = False

        if use_file_for_temp_logs is not None:
            log_session(use_file_for_temp_logs, current_entry_count=entry_count)
        
        entry_count = 0

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

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
    
    chat_loop(instruction="You are a helpful female AI assistant set in the world of 2037.", client=client, model="gemini-2.5-flash", use_file_as_universal_history="piyush.jsonl", use_file_for_temp_logs='test_session.jsonl')

# TODO: everytime I start a chat, it repeats the system instruction. Might want to fix that. If not, leave it!