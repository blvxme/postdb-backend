from asyncio import Queue
from typing import TypeVar, Generic

T = TypeVar("T")


class CommunicationQueue(Generic[T]):
    def __init__(self) -> None:
        self._queue = Queue[T]()

    async def send_message(self, message: T) -> None:
        return await self._queue.put(message)

    async def receive_message(self) -> T:
        return await self._queue.get()
