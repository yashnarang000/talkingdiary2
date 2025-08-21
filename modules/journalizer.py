import modules.api_adapter_openai as adap
import json
from datetime import datetime

def journalize(client, conversation, model):
    prompt  = f"Rewrite the narrative into a diary entry. Highlight the user's key experiences, emotions, and reflections as shared in the narrative. Craft a narrative that accurately reflects the user's story, avoiding assumptions or additions. Maintain a natural and engaging style. Do not focus on the other person user is chatting to. Just focus on the user. Just write the text, nothing else:\n{conversation}"
    journal = adap.respond(prompt=prompt, client=client, model=model)
    return journal

def jsonl_to_text(jsonl_history_file):

    conversation_list = []

    with open(jsonl_history_file, 'r') as f:

        entries = [json.loads(line) for line in f]

        for entry in entries:
            role = entry["role"]
            content = entry["content"]

            if role == "system":
                pass # ignore

            elif role == "user":
                conversation_list.append(f"Me: {content}")

            elif role == "assistant":
                conversation_list.append(f"AI: {content}")

    conversation = "\n".join(conversation_list)

    return conversation

def journal_it(session_history_path, client, output_file, model="gemini-2.5-flash"):
    content = jsonl_to_text(session_history_path)
    entry = journalize(client, content, model=model)

    now = datetime.now()
    formatted = now.strftime("%b %d, %Y")

    with open(output_file, 'a') as f:
        f.write(f"**{formatted}**\n{entry}\n\n")