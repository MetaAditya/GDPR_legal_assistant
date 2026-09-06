

from typing import *
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from llm_module.utils.llm_utils import query_processing_pipeline


router = APIRouter()



# @router.get("/chat-stream")
# async def stream(prompt: str):

#     return StreamingResponse(
#         llm_utils.llm_stream(prompt),
#         media_type="text/event-stream"
#     )



# @router.get("/chat-stream")
# async def stream(prompt: str, user_id:str, username:str, chat_mode:str):
    
#     return StreamingResponse(
#         query_processing_pipeline(input_query=prompt,user_id=user_id, chat_mode=chat_mode),

        
#         media_type="text/event-stream"
#     )


@router.get("/chat-stream")
async def stream(prompt: str, user_id: str, username: str, chat_mode: str):

    print(f"CHAT STREAM STARTED: {prompt}", flush=True)

    generator = query_processing_pipeline(
        input_query=prompt,
        user_id=user_id,
        chat_mode=chat_mode
    )

    print(f"GENERATOR CREATED: {generator}", flush=True)

    return StreamingResponse(
        generator,
        media_type="text/event-stream"
    )