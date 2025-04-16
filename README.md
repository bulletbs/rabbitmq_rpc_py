# Asynchronous RabbitMQ RPC library

`rabbitmq_rpc_py` is a lightweight, asynchronous Remote Procedure Call (RPC) library for Python, built on top of RabbitMQ and `aio-pika`. It enables developers to create client-server applications that communicate via named events (methods) over RabbitMQ with minimal setup.

## Features

- **Asynchronous Communication**: Built with `asyncio` for non-blocking operations.
- **Named Events**: Supports method-like calls using RabbitMQ queues (e.g., `rpc.sum_numbers`).
- **Simple API**: Easy-to-use client and server classes for quick integration.
- **Extensible**: Add custom handlers for specific use cases.
- **Python Compatibility**: Works with Python 3.8 and above.

## Installation

Install `rabbitmq_rpc_py` using `uv` or `pip`:

```bash
uv add rabbitmq_rpc_py
```

Or with `pip`:

```bash
pip install rabbitmq_rpc_py
```

## Requirements

To use `rabbitmq_rpc_py`, ensure the following are set up:

- **RabbitMQ**: A running RabbitMQ server. You can start one locally using Docker:
  ```bash
  docker run -d -p 5672:5672 rabbitmq
  ```
- **Python**: Version 3.8 or higher.
- **Dependencies**: The `aio-pika` library, which is automatically installed as a dependency of `rabbitmq_rpc_py`.

## Usage

Below are examples demonstrating how to use `rabbitmq_rpc_py` to create an RPC server and client. The server handles two methods:
- `rpc.sum_numbers`: Calculates the sum of a list of numbers provided in the input data.
- `rpc.echo_text`: Returns the input text unchanged.

### Example: RPC Server

Create a file named `server.py` to set up the server:

```python
import asyncio
from rabbitmq_rpc_py import RPCServer

async def sum_numbers(data):
    numbers = data.get("numbers", [])
    total = sum(numbers)
    return {"result": total}

async def echo_text(data):
    text = data.get("text", "")
    return {"result": text}

async def main():
    server = RPCServer("amqp://localhost/")
    await server.connect()
    server.register_handler("rpc.sum_numbers", sum_numbers)
    server.register_handler("rpc.echo_text", echo_text)
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
```

Run the server:

```bash
python server.py
```

Expected output:

```
RPC Server started. Waiting for requests...
```

### Example: RPC Client

Create a file named `client.py` to set up the client:

```python
import asyncio
from rabbitmq_rpc_py import RPCClient

async def main():
    client = RPCClient("amqp://localhost/")
    await client.connect()
    
    # Call sum_numbers
    result_sum = await client.call("rpc.sum_numbers", {
        "numbers": [1, 2, 3, 4, 5]
    })
    print(f"Sum result: {result_sum}")
    
    # Call echo_text
    result_echo = await client.call("rpc.echo_text", {
        "text": "Hello, RabbitMQ!"
    })
    print(f"Echo result: {result_echo}")
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run the client in a separate terminal (while the server is running):

```bash
python client.py
```

Expected output:

```
Sum result: {'result': 15}
Echo result: {'result': 'Hello, RabbitMQ!'}
```

## License

This project is licensed under the MIT License.
