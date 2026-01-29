from asyncio import Queue


class CommunicationQueue:
    def __init__(self) -> None:
        self._queue = Queue[str]()

    async def send_message(self, message: str) -> None:
        return await self._queue.put(message)

    async def receive_message(self) -> str:
        return await self._queue.get()
