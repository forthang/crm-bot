from enum import Enum

class ClientStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in progress"
    DEPOSIT = "deposit"
    NO_ANSWER = "no answer"
    VOICE_MAIL = "voice mail"
    CALL_BACK = "call back"
    DEAD = "dead"
