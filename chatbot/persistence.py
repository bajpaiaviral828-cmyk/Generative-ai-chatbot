import json
import os

# using json because I don't know how to set up sql yet
# plus it's easier to just read the file to debug
class SimpleJSONSaver:
    def __init__(self, filename="chats.json"):
        self.filename = filename
        
        # create the file if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def load(self, session_id):
        # read the whole file
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
                return data.get(session_id, [])
            except json.JSONDecodeError:
                # if file is corrupted or empty
                return []

    def save(self, session_id, history):
        # this is probably inefficient because it reads and writes the whole file every time
        # TODO: figure out a better way to do this later
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
                
        data[session_id] = history
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    def clear(self, session_id):
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
                
        if session_id in data:
            del data[session_id]
            
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
