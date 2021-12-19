from fastapi import FastAPI
from auth import api as auth_api
from checklists import api as checklists_api

app = FastAPI()
app.include_router(auth_api.router, tags=['auth', ])
app.include_router(checklists_api.router, prefix='/checklists', tags=['checklists', ])


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}
