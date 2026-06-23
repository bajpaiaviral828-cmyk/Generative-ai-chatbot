class InputValidator:

    @staticmethod
    def is_valid(text):
        return bool(text and text.strip())

    @staticmethod
    def sanitize(text):
        return text.strip()

    @classmethod
    def validate_and_sanitize(cls, text):
        if not cls.is_valid(text):
            return False, ""
        return True, cls.sanitize(text)
