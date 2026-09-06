# frontend.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
import asyncio,os
from settings import env_settings
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import time
from typing import *
from starlette.middleware.base import BaseHTTPMiddleware
from middleware_ import check_session
from fastapi import Depends
import psycopg2
from fastapi import UploadFile, File
import httpx
from fastapi.responses import Response

oauth = OAuth()

# oauth.register(
#     name="keycloak",
#     client_id=env_settings.KEYCLOAK_CLIENT_ID,
#     client_secret=env_settings.KEYCLOAK_CLIENT_SECRET,
#     server_metadata_url=(
#         "http://localhost:8080/realms/"
#         "legal_assistant/.well-known/openid-configuration"
#     ),
#     client_kwargs={
#         "scope": "openid profile email",
#          "code_challenge_method": "S256",
#     },
# )


oauth.register(
    name="keycloak",

    client_id=env_settings.KEYCLOAK_CLIENT_ID,
    client_secret=env_settings.KEYCLOAK_CLIENT_SECRET,

    authorize_url=(
        f"{env_settings.KEYCLOAK_PUBLIC_SERVER}/realms/"
        f"{env_settings.KEYCLOAK_REALM}/protocol/openid-connect/auth"
    ),

    access_token_url=(
        f"{env_settings.KEYCLOAK_SERVER}/realms/"
        f"{env_settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    ),

    jwks_uri=(
        f"{env_settings.KEYCLOAK_SERVER}/realms/"
        f"{env_settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    ),

    client_kwargs={
        "scope": "openid profile email",
        "code_challenge_method": "S256",
    },
)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
templates = Jinja2Templates(directory="templates")




app.add_middleware(
    SessionMiddleware,
    secret_key="replace-this-with-a-long-random-secret",
)

# app.add_middleware(
#     SessionTimeoutMiddleware,
# )
#############################################################SSSSSSS


@app.get("/login")
async def login(request: Request):

    redirect_uri = request.url_for("auth_callback")

    return await oauth.keycloak.authorize_redirect(
        request,
        redirect_uri,
    )


@app.get("/auth/callback", name="auth_callback")
async def auth_callback(request: Request):

    token = await oauth.keycloak.authorize_access_token(request)

    userinfo = token.get("userinfo")

    request.session["user"] = {
        "id": userinfo["sub"],
        "username": userinfo.get("preferred_username"),
        "email": userinfo.get("email"),
    }
    request.session["last_activity"] = time.time()

    return RedirectResponse(url="/")




@app.get("/")
async def home(request: Request, authenticated: bool = Depends(check_session),):

    
    user = request.session.get("user")
    
    

    if not user:
        return RedirectResponse(url="/login")



    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
        },
    )


# Proxy streaming from backend
async def proxy_stream(prompt: str, user_info:Dict, chat_mode: str):

    print(f"=========================={chat_mode}===================")
    async with httpx.AsyncClient(timeout=None) as client:

        async with client.stream(
            "GET",
            f"{env_settings.BACKEND_URL}/chat-stream",
            params={"prompt": prompt,"user_id":user_info.get("id",""), "username":user_info.get("username",""), "chat_mode":chat_mode }
        ) as response:

            async for chunk in response.aiter_text():

                # Forward chunks directly
                yield chunk


# @app.get("/logout")
# async def logout(request: Request):

#     # Remove local FastAPI session
#     request.session.clear()

#     # Keycloak logout endpoint
#     logout_url = (
#         f"{env_settings.KEYCLOAK_SERVER}/realms/legal_assistant/protocol/openid-connect/logout"
#         "?"
#         + urlencode({
#             "post_logout_redirect_uri": "http://localhost:9000/",
#             "client_id": env_settings.KEYCLOAK_CLIENT_ID,
#         })
#     )

#     return RedirectResponse(url=logout_url)




@app.get("/logout")
async def logout(request: Request):

    # Clear FastAPI session
    request.session.clear()

    # Browser must access Keycloak through localhost
    logout_url = (
        f"{env_settings.KEYCLOAK_PUBLIC_SERVER}"
        f"/realms/{env_settings.KEYCLOAK_REALM}"
        f"/protocol/openid-connect/logout?"
        + urlencode({
            "post_logout_redirect_uri": env_settings.KEYCLOAK_POST_LOGOUT_REDIRECT_URI,
            "client_id": env_settings.KEYCLOAK_CLIENT_ID,
        })
    )

    return RedirectResponse(url=logout_url)


# Frontend streaming endpoint
@app.get("/frontend-stream")
async def frontend_stream(prompt: str, request:Request, chat_mode:str):

    user_info = request.session.get("user")
    if not user_info:
        return
    

    return StreamingResponse(
        proxy_stream(prompt, user_info, chat_mode),
        media_type="text/event-stream"
    )



############File upload###########



@app.post("/upload")
async def upload_file(request: Request,file: UploadFile = File(...), ):

    file_bytes = await file.read()
    user_info = request.session.get("user")
    user_name=user_info.get("id","")

    file_data = {
        "file": (
            file.filename,
            file_bytes,
            file.content_type,
            )

            
    }
    form_data = {
        "user_id": user_name
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            f"{env_settings.BACKEND_URL}/upload",
            files=file_data,
            data=form_data
        )

    return response.json()

############################Graph Data ###################

class DB_connect():

    def __init__(self):

        dbname=env_settings.PG_DB
        user=env_settings.PG_USER
        password=env_settings.PG_PASSWORD
        host=env_settings.PG_HOST
        port=env_settings.PG_PORT
    

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()






#############################################################
@app.get("/api/graph")
async def get_graph():

    db = DB_connect()

    # Get nodes
    db.cur.execute("""
        SELECT
            id,
            type,
            properties
        FROM nodes
    """)

    nodes = db.cur.fetchall()

    # Get relationships
    db.cur.execute("""
        SELECT
            id,
            source_id,
            source_type,
            target_id,
            target_type,
            type,
            properties
        FROM relationships
    """)

    relationships = db.cur.fetchall()

    db.cur.close()
    db.conn.close()

    return {
        "nodes": [
            {
                "id": row[0],
                "type": row[1],
                "properties": row[2] or {}
            }
            for row in nodes
        ],

        "relationships": [
            {
                "id": row[0],
                "source": row[1],
                "source_type": row[2],
                "target": row[3],
                "target_type": row[4],
                "type": row[5],
                "properties": row[6] or {}
            }
            for row in relationships
        ]
    }


@app.get("/graph")
async def graph_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="graph_viz.html"
    )

#################################
@app.get("/download")
async def download_from_backend():

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{env_settings.BACKEND_URL}/download"
        )

    return Response(
        content=response.content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="download.pdf"'
        }
    )