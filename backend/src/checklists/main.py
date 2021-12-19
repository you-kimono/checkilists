from fastapi import FastAPI
from auth import api as auth_api

app = FastAPI()
app.include_router(auth_api.router, tags=['auth', ])


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}
