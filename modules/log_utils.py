import json
from collections import deque

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
    
def get_last_n(history_jsonl_file, n):
    with open(history_jsonl_file, "r") as f:
        return list(deque(f, maxlen=n)) # it works like a sliding window with maximum n elements in frame, one enters, one exists
    