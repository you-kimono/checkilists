from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'hello, stronzo!'}


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}
