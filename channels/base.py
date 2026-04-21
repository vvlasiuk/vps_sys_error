from abc import ABC, abstractmethod

class BaseChannel(ABC):
    @abstractmethod
    def create_message(self, msg: dict, config: dict) -> dict:
        """
        Формує структуру для вихідної черги відповідного каналу.
        :param msg: Вхідне повідомлення
        :param config: Конфіг каналів з responsibility.json
        :return: dict для відправки у чергу
        """
        pass
