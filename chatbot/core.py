import uuid
import google.generativeai as genai

from config import Config
from chatbot.memory import SlidingWindowMemory
from chatbot.validator import InputValidator
from chatbot.persistence import SimpleJSONSaver

import tenacity
from tenacity import retry, stop_after_attempt, wait_exponential
import google.api_core.exceptions

class ChatBot:

    def __init__(self, session_id=None, backend=None, max_turns=None, model_name=None):
        Config.validate()

        self.session_id = session_id or str(uuid.uuid4())
        self.model_name = model_name or Config.GEMINI_MODEL

        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.model_name)

        self.max_turns = max_turns or Config.MAX_HISTORY_TURNS
        self.memory = SlidingWindowMemory(max_turns=self.max_turns)

        self.validator = InputValidator()

        # default to saving in chats.json
        self.backend = backend or SimpleJSONSaver()

        # load history if it exists
        saved = self.backend.load(self.session_id)
        if saved:
            self.memory.load_from_saved(saved)

    # I found out the hard way that google has rate limits if you send too fast.
    # StackOverflow said to use 'tenacity' to automatically wait and try again instead of crashing.
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=tenacity.retry_if_exception_type((
            google.api_core.exceptions.ResourceExhausted,
            google.api_core.exceptions.ServiceUnavailable,
            google.api_core.exceptions.DeadlineExceeded
        )),
        reraise=True
    )
    def _generate_with_retry(self, history):
        return self.model.generate_content(history)

    def send(self, user_input):
        is_valid, clean_input = self.validator.validate_and_sanitize(user_input)
        if not is_valid:
            return "Please type something before hitting enter!"

        self.memory.add_user_message(clean_input)

        try:
            # this takes a few seconds sometimes
            response = self._generate_with_retry(self.memory.get_history())
            reply_text = response.text
        except Exception as e:
            # remove my message from memory so it doesn't get messed up
            self.memory.remove_last()
            return f"Something went wrong (probably google rate limits): {e}"

        self.memory.add_model_message(reply_text)
        
        # save after every turn, kinda slow but works
        self.backend.save(self.session_id, self.memory.get_history())

        return reply_text

    def reset(self):
        self.memory.clear()
        self.backend.clear(self.session_id)

    def get_turn_count(self):
        return self.memory.turn_count()
