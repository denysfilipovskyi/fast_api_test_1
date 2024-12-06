from abc import ABC, abstractmethod


class AbstractMsgBrokerRepository(ABC):
    @abstractmethod
    async def _connect():
        raise NotImplementedError

    @abstractmethod
    async def publish_message():
        raise NotImplementedError
