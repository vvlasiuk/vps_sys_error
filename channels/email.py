from .base import BaseChannel

class EmailChannel(BaseChannel):
    def create_message(self, msg: dict, config: dict) -> dict:
        return {
            "destination": {
                "system": "email",
                "address": config["address"]
            },
            "text": msg["message"]
        }
