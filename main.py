from typing import Union
from fastapi import FastAPI
from mastodon import Mastodon
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}+{q}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/login/{token}+{instance_url}")
def masto_login(token: str, instance_url: str):
    mastodon = Mastodon(
        access_token=token,
        api_base_url=instance_url
    )   
    return {"mastodon_obj": mastodon}