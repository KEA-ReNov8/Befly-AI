class CustomException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

class ServerException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.code = "SERVER_ERROR"
