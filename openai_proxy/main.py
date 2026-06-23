from fastapi import Request as FastAPIRequest
from fastapi_offline import FastAPIOffline
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Union, Dict, Any
import time, json, os, uuid
from datetime import datetime
from common.api import DeepSeekAPI
from common.config import DEEPSEEK_API_KEY

app = FastAPIOffline()

api = DeepSeekAPI(DEEPSEEK_API_KEY)

sessions: Dict[str, dict] = {}

AVAILABLE_MODELS = [{"id": "thinking_not_search", "object": "model1","created": 1677610602, "owned_by": "you"},
                    {"id": "thinking_search", "object": "model2","created": 1677610602, "owned_by": "you"},
                    {"id": "not_thinking_not_search", "object": "model3","created": 1677610602, "owned_by": "you"},
                    {"id": "not_thinking_search", "object": "model4","created": 1677610602, "owned_by": "you"}]

# ---------- Models ----------
class ContentPart(BaseModel):
    type: str = "text"
    text: Optional[str] = ""

class Message(BaseModel):
    role: str = "user"
    content: Union[str, List[ContentPart]] = ""

    reasoning_content: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def fill_defaults(cls, values):
        if values is None:
            return {"role": "user", "content": ""}

        if isinstance(values, dict):
            values.setdefault("role", "user")
            values.setdefault("content", "")
            values.setdefault("reasoning_content", "")
            return values

        return values

class ChatRequest(BaseModel):
    model_config = {"extra": "ignore"}
    
    messages: List[Message]
    model: str = "thinking_not_search"
    stream: Optional[bool] = False
    stream_options: Optional[Dict[str, Any]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    
# ---------- Helper ----------
def extract_content(content: Union[str, List[ContentPart]]) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(part.text or "" for part in content if part.type == "text")

def messages_to_api_format(messages: List[Message]) -> str:
    """تبدیل messages به فرمت API (اگر API از آرایه messages پشتیبانی کنه)"""
    parts = []
    for msg in messages:
        content = extract_content(msg.content)
        parts.append(f"[{msg.role.upper()}]\n{content}")
    return "\n\n".join(parts)
# ---------- Middleware برای لاگ ----------
@app.middleware("http")
async def log_time(request: FastAPIRequest, call_next):
    start = datetime.now()
    print(f"[{start.strftime('%H:%M:%S.%f')[:-3]}] --> {request.method} {request.url.path}")
    response = await call_next(request)
    end = datetime.now()
    print(f"[{end.strftime('%H:%M:%S.%f')[:-3]}] <-- {response.status_code} (took {(end-start).total_seconds():.2f}s)")
    return response

# ---------- Endpoints ----------
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    chat_id = api.create_chat_session()
    
    prompt = messages_to_api_format(request.messages)

    if request.model=="not_thinking_not_search":
            thinking=False
            search=False
    elif request.model=="thinking_not_search":
            thinking=True
            search=False 
    elif request.model=="thinking_search":
            thinking=True
            search=True
    elif request.model=="not_thinking_search":
            thinking=False
            search=True
    else:
        thinking, search = True, False  # default fallback
    if request.stream:
        def generate():
            
            # ارسال به API با کل history
            for chunk in api.chat_completion(
                chat_id, 
                prompt,  # کل messages به صورت prompt
                thinking_enabled=thinking,
                search_enabled=search
            ):
                chunk_type = chunk.get("type")
                
                if chunk_type == 'thinking':
                    # ارسال thinking به عنوان reasoning_content (طبق استاندارد OpenAI)
                    delta = {"reasoning_content": chunk.get("delta", "")}
                elif chunk_type == 'content':
                    delta = {"content": chunk.get("delta", "")}
                elif chunk_type == 'finished':
                    break  # خروج از حلقه برای ارسال final chunk
                else:
                    continue  # نوع ناشناخته، نادیده بگیر
                
                response_chunk = {
                    "id": f"chatcmpl-{chat_id}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": request.model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": delta,
                            "finish_reason": None
                        }
                    ]
                }
                yield f"data: {json.dumps(response_chunk)}\n\n"

            
            final_chunk = {
                "id": f"chatcmpl-{chat_id}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop"
                    }
                ]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    # حالت غیر-استریم
    full_text = ""
    full_thinking = ""
    
    for chunk in api.chat_completion(
        chat_id, 
        prompt,  # کل messages
        thinking_enabled=thinking,
        search_enabled=search
    ):
        chunk_type = chunk.get("type")
            
        if chunk_type == 'content':
            full_text += chunk.get("delta", "")
        elif chunk_type == 'thinking':
            full_thinking += chunk.get("delta", "")
        elif chunk_type == 'finished':
            break

    return {
        "id": f"chatcmpl-{chat_id}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": full_text,
                    "reasoning_content": full_thinking if full_thinking else None
                },

                "finish_reason": "stop"
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

@app.get("/v1/models")
async def list_models():
    return {"object": "list", "data": AVAILABLE_MODELS}