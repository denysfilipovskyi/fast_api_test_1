from abc import ABC, abstractmethod


class AbstractNoSqlRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError
