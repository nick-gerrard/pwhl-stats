import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from live import poller
from live.poller import live_state

router = APIRouter()


@router.get("/live")
async def live():
    async def event_stream():
        queue = asyncio.Queue()
        poller.clients.add(queue)
        try:
            if live_state:
                yield f"data: {json.dumps(live_state)}\n\n"
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        finally:
            poller.clients.discard(queue)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no"},
    )
