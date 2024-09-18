import json
import math

from .errors import NOT_FOUND, UNPROCESSABLE_ENTITY, BAD_REQUEST


async def app(scope, receive, send):
    assert scope["type"] == "http"

    method = scope["method"]
    path = scope["path"]

    if method == "GET" and path == "/factorial":
        await factorial(scope, receive, send)

    elif method == "GET" and path.startswith("/fibonacci"):
        await fibonacci(scope, receive, send)

    elif method == "GET" and path == "/mean":
        await mean(scope, receive, send)

    else:
        await NOT_FOUND(send)


async def factorial(scope, receive, send):
    query_string = scope["query_string"].decode()
    params = dict(p.split("=") for p in query_string.split("&") if "=" in p)

    if "n" not in params:
        await UNPROCESSABLE_ENTITY(send)
        return

    try:
        n = int(params["n"])

    except ValueError:
        await UNPROCESSABLE_ENTITY(send)
        return

    if n < 0:
        await BAD_REQUEST(send)
        return

    result = math.factorial(n)
    response = {"result": result}

    await send_json(send, response)


async def fibonacci(scope, receive, send):
    try:
        path = scope["path"]
        n = int(path.split("/")[-1])

    except (ValueError, IndexError):
        await UNPROCESSABLE_ENTITY(send)
        return

    if n < 0:
        await BAD_REQUEST(send)
        return

    result = fibonacci_number(n)
    response = {"result": result}

    await send_json(send, response)


async def mean(scope, receive, send):
    body = await receive_body(receive)

    try:
        numbers = json.loads(body)

        if not isinstance(numbers, list) or not all(
            isinstance(x, (int, float)) for x in numbers
        ):
            await UNPROCESSABLE_ENTITY(send)
            return

        if len(numbers) == 0:
            await BAD_REQUEST(send)
            return

        result = sum(numbers) / len(numbers)
        response = {"result": result}

        await send_json(send, response)

    except json.JSONDecodeError:
        await UNPROCESSABLE_ENTITY(send)


async def send_json(send, response_body):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(response_body).encode("utf-8"),
        }
    )


def fibonacci_number(n):
    if n in [0, 1]:
        return n

    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


async def receive_body(receive):
    body = b""
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)

    return body
