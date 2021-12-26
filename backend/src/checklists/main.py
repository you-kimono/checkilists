from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import api as auth_api
from checklists import api as checklists_api

app = FastAPI()

origins = [
    'http://localhost:3000',
    'localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_api.router, tags=['auth', ])
app.include_router(checklists_api.router, prefix='/checklists', tags=['checklists', ])


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}
