
INFO = 3
WARNING = 2
ERROR = 1


class Debug:

    def __init__(self, debug_level=INFO):
        self.debug_level = debug_level

    def log(self, msg, log_level=INFO):
        if log_level >= self.debug_level:
            print(msg)

    def info(self, msg):
        self.log(msg, INFO)

    def warning(self, msg):
        self.log(msg, WARNING)

    def error(self, msg):
        self.log(msg, ERROR)