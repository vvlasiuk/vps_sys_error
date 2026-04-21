import importlib
from channels.base import BaseChannel
from config import load_responsibility

responsibility_cfg = load_responsibility()

class Dispatcher:
    def __init__(self):
        self.channel_cache = {}

    def get_channel(self, channel_name):
        if channel_name in self.channel_cache:
            return self.channel_cache[channel_name]
        try:
            module = importlib.import_module(f"channels.{channel_name}")
            class_name = f"{channel_name.capitalize()}Channel"
            channel_cls = getattr(module, class_name)
            if not issubclass(channel_cls, BaseChannel):
                raise TypeError(f"{class_name} does not implement BaseChannel")
            self.channel_cache[channel_name] = channel_cls()
            return self.channel_cache[channel_name]
        except Exception as e:
            print(f"[Dispatcher] Channel '{channel_name}' error: {e}")
            return None

    def dispatch(self, msg: dict):
        out_msgs = []
        # Всі повідомлення завжди надсилаються отримувачам з all
        if "all" in responsibility_cfg:
            channels = responsibility_cfg["all"]["channels"]
            for ch_name, ch_cfg in channels.items():
                channel = self.get_channel(ch_name)
                if channel:
                    try:
                        out_msgs.append((ch_name, channel.create_message(msg, ch_cfg)))
                    except Exception as e:
                        print(f"[Dispatcher] Error in channel '{ch_name}': {e}")
        else:
            print("[Dispatcher] 'all' not defined in responsibility.json")
        return out_msgs
