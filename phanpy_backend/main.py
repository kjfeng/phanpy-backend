from typing import Union
from fastapi import FastAPI, HTTPException, Header
from mastodon import Mastodon, MastodonError, MastodonNetworkError, MastodonUnauthorizedError
import uvicorn
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

@app.get("/home_posts")
def home_posts(access_token: str = Header(), instance_url: str = Header()):
    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=instance_url
    )
    try:   
        return mastodon.timeline_home()
    except MastodonUnauthorizedError as err:
        raise HTTPException(status_code=401, detail=err.args)
    except MastodonNetworkError as err:
        raise HTTPException(status_code=500, detail=err.args)


def start_dev():
    """Starts uvicorn server with reload on code change enabled."""
    uvicorn.run("phanpy_backend.main:app", host="0.0.0.0", port=8000, reload=True)

def start_prod():
    """Starts uvicorn server with reload on code change disabled."""
    uvicorn.run("phanpy_backend.main:app", host="0.0.0.0", port=8000, reload=False)