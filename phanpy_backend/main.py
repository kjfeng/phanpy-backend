from typing import Union
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from mastodon import Mastodon, MastodonError, MastodonNetworkError, MastodonUnauthorizedError
import uvicorn
from fastapi.logger import logger
# from oauthlib.oauth2 import BackendApplicationClient
# from requests_oauthlib import OAuth2Session

app = FastAPI()

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}+{q}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/login/{token}+{instance_url}")
# def masto_login(token: str, instance_url: str):
#     mastodon = Mastodon(
#         access_token=token,
#         api_base_url=instance_url
#     )   
#     return {"mastodon_obj": mastodon}

origins = [
    "http://localhost:5173",
    "localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/home_posts")
# def home_posts(access_token: str = Header(), instance_url: str = Header()):
#     mastodon = Mastodon(
#         access_token=access_token,
#         api_base_url=instance_url
#     )
#     try:   
#         return mastodon.timeline_home(limit=10)
#     except MastodonUnauthorizedError as err:
#         raise HTTPException(status_code=401, detail=err.args)
#     except MastodonNetworkError as err:
#         raise HTTPException(status_code=500, detail=err.args)

@app.get("/home_posts/{access_token}+{instance_url}")
def home_posts(access_token: str, instance_url: str, limit: int):
    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=instance_url
    )
    print(access_token)
    print(instance_url)
    try:   
        return mastodon.timeline_home(limit=limit)
    except MastodonUnauthorizedError as err:
        raise HTTPException(status_code=401, detail=err.args)
    except MastodonNetworkError as err:
        raise HTTPException(status_code=500, detail=err.args)


@app.get("/get_username")
def get_username(access_token: str = Header(), instance_url: str = Header()):
    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=instance_url
    )
    try:   
        return mastodon.me()
    except MastodonUnauthorizedError as err:
        raise HTTPException(status_code=401, detail=err.args)
    except MastodonNetworkError as err:
        raise HTTPException(status_code=500, detail=err.args)


def start_dev():
    """Starts uvicorn server with reload on code change enabled."""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

def start_prod():
    """Starts uvicorn server with reload on code change disabled."""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    start_dev()