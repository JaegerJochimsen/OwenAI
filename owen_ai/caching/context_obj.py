import datetime


class ContextObj:
    def __init__(self, context_string: str):
        self.timestamp = datetime.datetime.utcnow()
        self.context = context_string

    def getContext(self) -> str:
        return self.context

    def getTimestamp(self) -> datetime:
        return self.timestamp
