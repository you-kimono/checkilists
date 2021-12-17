from fastapi import FastAPI
from auth import api as auth_api

app = FastAPI()
app.include_router(auth_api.router, prefix='/users', tags=['users', ])


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}
