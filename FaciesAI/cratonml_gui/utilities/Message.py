from dataclasses import dataclass


@dataclass
class Message:
    message: str
    is_error: bool = False
    is_warning: bool = False
    is_message_for_all: bool = False
