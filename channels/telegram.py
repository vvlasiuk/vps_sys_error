from .base import BaseChannel

class TelegramChannel(BaseChannel):
    def create_message(self, msg: dict, config: dict) -> dict:
        # Вибір емодзі для error
        error_emoji = "❗"
        responsibility = msg.get("responsibility", "")
        # resp_emoji = {
        #     "network": "🌐",
        #     "database": "🗄️",
        #     "1c": "📦",
        #     "all": "🔔"
        # }.get(responsibility, "🛑")
        text = f"{error_emoji}[{msg['type']}] {msg['text']}"
        return {
            "destination": {
                "system": "telegram",
                "chat_id": config["chat_id"]
            },
            "type": "text",
            "content": text
        }
