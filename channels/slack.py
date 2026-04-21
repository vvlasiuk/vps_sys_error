from .base import BaseChannel

class SlackChannel(BaseChannel):
    def create_message(self, msg: dict, config: dict) -> dict:
        return {
            "destination": {
                "system": "slack",
                "channel": config["channel"]
            },
            "text": msg["message"]
        }
