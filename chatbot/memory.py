class SlidingWindowMemory:

    def __init__(self, max_turns=10):
        # basically how many Q&A pairs we remember before dropping old ones
        self.max_turns = max_turns
        self.history = []

    def add_user_message(self, text):
        self.history.append({
            "role": "user",
            "parts": [{"text": text}]
        })
        self._trim_history()

    def add_model_message(self, text):
        self.history.append({
            "role": "model",
            "parts": [{"text": text}]
        })
        self._trim_history()

    def _trim_history(self):
        # if the history gets too long, Gemini will throw a token limit error.
        # so I just delete the oldest 2 items (user + model response)
        # TODO: maybe check actual token count instead of just array length later?
        while len(self.history) > self.max_turns * 2:
            self.history.pop(0)
            if self.history:
                self.history.pop(0)

    def get_history(self):
        return list(self.history)

    def load_from_saved(self, messages):
        # load from json
        self.history = list(messages)
        self._trim_history()

    def clear(self):
        self.history = []

    def remove_last(self):
        # if an error happens, we need to delete the user's message so they can try again
        if self.history and self.history[-1]["role"] == "user":
            self.history.pop()

    def turn_count(self):
        # divide by 2 because one turn is a user message AND a model message
        return len(self.history) // 2
