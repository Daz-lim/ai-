from fastapi import APIRouter
from src.app.models.schemas import ChatRequest
from fastapi.responses import StreamingResponse
from src.app.agents.chief import search_recipes,clear_message,get_messages
router = APIRouter()


@router.post("/chat/stream")
async def chat_endpoint(request: ChatRequest):
    """流式对话"""
    return StreamingResponse(
        search_recipes(
            prompt=request.message,
            image=request.image_url,
            thread_id=request.thread_id),
        media_type="text/event-stream"
    )


@router.get("/chat/messages")
async def get_chat_messages(thread_id: str):
    """获取历史消息"""
    messages = get_messages(thread_id)
    return {"messages": messages}

@router.delete("/chat/messages")
async def clear_chat_messages(thread_id: str):
    """清空历史消息"""
    clear_message(thread_id)
    return {"success": True}