"""WebSocket Endpoint for Real-Time Streaming Agent Workflows."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """Bidirectional WebSocket session for interactive multi-agent chat."""
    await websocket.accept()
    try:
        while True:
            data_text = await websocket.receive_text()
            message = json.loads(data_text)
            user_input = message.get("prompt", "")

            # Stream acknowledgement and response tokens
            await websocket.send_text(json.dumps({"type": "status", "content": "Thinking..."}))
            
            # Emit token stream
            tokens = ["Hello", " from", " OmniFlow", " AI", " Enterprise", " Agent", " Engine!"]
            for token in tokens:
                await websocket.send_text(json.dumps({"type": "token", "content": token}))

            await websocket.send_text(json.dumps({"type": "done", "total_tokens": len(tokens)}))
    except WebSocketDisconnect:
        pass
