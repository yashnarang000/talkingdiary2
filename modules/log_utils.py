import json
from collections import deque
import time
from datetime import datetime

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
    
def log_session(session_jsonl_file, current_entry_count):

    current_timestamp = str(time.time())

    with open(session_jsonl_file, 'r+') as f:
        try:
            last_session_data = [json.loads(line) for line in f][-1]
            current_session_data = {"timestamp": current_timestamp, "entry_count": current_entry_count + last_session_data["entry_count"]}
        except IndexError:
            current_session_data = {"timestamp": current_timestamp, "entry_count": current_entry_count}

        f.write(json.dumps(current_session_data) + '\n')

def fold_session_logs(temp_session_jsonl, session_jsonl):
    with open(temp_session_jsonl, 'r+') as f:
        temp_session_data = [json.loads(line) for line in f]
        first_entry_data = temp_session_data[0]
        last_entry_data = temp_session_data[-1]
        f.seek(0)
        f.truncate()

    start_time = datetime.fromtimestamp(float(first_entry_data["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.fromtimestamp(float(last_entry_data["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')

    with open(session_jsonl, 'r+') as f:
        try:
            last_session_data = [json.loads(line) for line in f][-1]
            current_session_id = str(int(last_session_data["session_id"]) + 1)
        except IndexError:
            current_session_id = "0"

        session_data = {"session_id": current_session_id, "start": start_time, "end": end_time}
        f.write(json.dumps(session_data) + '\n')

def history_clipper(universal_history_jsonl, sessionwise_history_jsonl, entry_count):
    '''
    clips the last entry_count number of entries to another file 
    '''
    clipped_history = get_last_n(history_jsonl_file=universal_history_jsonl, n=entry_count)

    with open(sessionwise_history_jsonl, 'w') as f:
        f.write(json.dumps(clipped_history))

# Universal history : this history is 'remembered' by the llm
# Sessional history :  this history is that part of universal history whose diary entry is yet to be made

if __name__ == '__main__':
    fold_session_logs('test_session.jsonl', 'new.jsonl')