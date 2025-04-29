import asyncio
import uuid
import json
from aio_pika import connect, Message, DeliveryMode

class RPCBase:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect(self.amqp_url)
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None

class RPCClient(RPCBase):
    def __init__(self, amqp_url: str):
        super().__init__(amqp_url)
        self.callback_queue = None
        self.futures = {}

    async def connect(self):
        await super().connect()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)

    async def on_response(self, message):
        await message.ack()
        future = self.futures.pop(message.correlation_id, None)
        if future:
            future.set_result(json.loads(message.body))

    async def call(self, queue_name: str, data: dict, timeout: int = 30) -> dict:
        correlation_id = str(uuid.uuid4())
        future = asyncio.get_event_loop().create_future()
        self.futures[correlation_id] = future

        message = Message(
            json.dumps(data).encode(),
            correlation_id=correlation_id,
            reply_to=self.callback_queue.name,
            delivery_mode=DeliveryMode.PERSISTENT
        )

        await self.channel.default_exchange.publish(message, routing_key=queue_name)

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            self.futures.pop(correlation_id, None)
            raise TimeoutError(f"RPC call to {queue_name} timed out")

class RPCServer(RPCBase):
    def __init__(self, amqp_url: str):
        super().__init__(amqp_url)
        self.handlers = {}

    def register_handler(self, queue_name: str, handler_func):
        self.handlers[queue_name] = handler_func

    async def start(self):
        for queue_name in self.handlers:
            queue = await self.channel.declare_queue(queue_name, durable=True)
            await queue.consume(self.process_message)
        print("RPC Server started. Waiting for requests...")
        await asyncio.Future()  # Удерживаем сервер активным

    async def process_message(self, message):
        await message.ack()
        queue_name = message.routing_key
        handler = self.handlers.get(queue_name)
        if handler:
            data = json.loads(message.body)
            result = await handler(data)
            response_message = Message(
                json.dumps(result).encode(),
                correlation_id=message.correlation_id,
                delivery_mode=DeliveryMode.PERSISTENT
            )
            if message.reply_to is not None:
                await self.channel.default_exchange.publish(
                    response_message,
                    routing_key=message.reply_to
                )