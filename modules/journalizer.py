import api_adapter_openai as adap
import json
from collections import deque

def journalize(client, conversation):
    prompt  = f"Rewrite the narrative into a diary entry. Highlight the user's key experiences, emotions, and reflections as shared in the narrative. Craft a narrative that accurately reflects the user's story, avoiding assumptions or additions. Maintain a natural and engaging style:\n{conversation}"
    journal = adap.respond(prompt=prompt, client=client, model="gemini-2-5-pro")
    return journal

def get_last_n(history_file_in_jsonl, anchor, entry_file):
    # anchor is the length of history list in the last session

    with open(history_file_in_jsonl, "r") as f:
        return list(deque(f, maxlen=anchor))