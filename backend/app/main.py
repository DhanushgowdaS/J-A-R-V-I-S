from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse
from .core import respond, get_history, clear_history, list_history
from .config import settings
from .database import initialize, add_memory, list_memories, delete_memory\nfrom .tools import list_tools, execute_tool

app = FastAPI(title="J-A-R-V-I-S API",version="0.4.0",description="Local API for the J-A-R-V-I-S personal assistant.")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],allow_credentials=True,allow_methods=["GET","POST","DELETE"],allow_headers=["Content-Type","Authorization"])

@app.on_event("startup")
def startup():
    initialize()

@app.get("/api/health",tags=["system"])
def health_check():
    return {"status":"ok","service":"J-A-R-V-I-S API","version":"0.4.0"}

@app.get("/api",tags=["system"])
def api_info():
    return {"name":"J-A-R-V-I-S","status":"core-foundation","message":"Backend is running.","provider_configured":bool(settings.ai_api_key)}

@app.post("/api/chat",response_model=ChatResponse,tags=["assistant"])
async def chat(request:ChatRequest):
    if not request.message.strip(): raise HTTPException(status_code=422,detail="Message cannot be empty.")
    result=await respond(request.message,request.conversation_id)
    return ChatResponse(conversation_id=result["conversation_id"],reply=result["reply"],mode=result["mode"],provider_configured=bool(settings.ai_api_key))

@app.get("/api/conversations",tags=["assistant"])
def conversations():
    return {"conversations":list_history()}

@app.get("/api/conversations/{conversation_id}/history",tags=["assistant"])
def conversation_history(conversation_id:str):
    return {"conversation_id":conversation_id,"messages":get_history(conversation_id)}

@app.delete("/api/conversations/{conversation_id}",tags=["assistant"])
def delete_conversation(conversation_id:str):
    return {"deleted":clear_history(conversation_id)}

@app.get("/api/tools",tags=["tools"])
def available_tools():
    return {"tools":list_tools()}

@app.post("/api/tools/{tool_name}/execute",tags=["tools"])
def run_tool(tool_name:str, payload:dict):
    try:
        return {"tool":tool_name,"result":execute_tool(tool_name,payload)}
    except KeyError:
        raise HTTPException(status_code=404,detail="Tool is not available.")
    except (ValueError,ZeroDivisionError,OverflowError) as exc:
        raise HTTPException(status_code=400,detail=str(exc))

@app.get("/api/memory",tags=["memory"])
def memory_list(category:str|None=None):
    return {"memories":list_memories(category)}

@app.post("/api/memory",tags=["memory"])
def memory_create(payload:dict):
    content=payload.get("content")
    if not isinstance(content,str) or not content.strip():
        raise HTTPException(status_code=422,detail="Memory content is required.")
    if len(content)>2000:
        raise HTTPException(status_code=422,detail="Memory content exceeds 2000 characters.")
    category=payload.get("category","general")
    if not isinstance(category,str) or len(category)>80:
        raise HTTPException(status_code=422,detail="Invalid memory category.")
    memory_id=add_memory(content,category)
    return {"id":memory_id,"saved":True}

@app.delete("/api/memory/{memory_id}",tags=["memory"])
def memory_delete(memory_id:int):
    return {"deleted":delete_memory(memory_id)}
