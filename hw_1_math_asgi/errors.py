import json


async def not_found(send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "Not Found"}).encode("utf-8"),
        }
    )


async def bad_request(send):
    await send(
        {
            "type": "http.response.start",
            "status": 400,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "Bad Request"}).encode("utf-8"),
        }
    )


async def unprocessable_entity(send):
    await send(
        {
            "type": "http.response.start",
            "status": 422,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": json.dumps({"error": "Unprocessable Entity"}).encode("utf-8"),
        }
    )


NOT_FOUND = not_found
UNPROCESSABLE_ENTITY = unprocessable_entity
BAD_REQUEST = bad_request
