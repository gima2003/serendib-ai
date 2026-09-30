from fastapi import FastAPI
from backend.routes.profile_route import router
import uvicorn

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=8002)
