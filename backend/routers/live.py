import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from live import poller

router = APIRouter()


@router.get("/live")
async def live():
    async def event_stream():
        queue = asyncio.Queue()
        poller.clients.add(queue)
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        finally:
            poller.clients.discard(queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
