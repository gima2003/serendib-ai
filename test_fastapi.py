from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Out(BaseModel):
    name: str

@app.post("/test", response_model=Out)
def test():
    return {"wrong_field": "hello"} # Missing 'name', should fail response validation

if __name__ == "__main__":
    uvicorn.run(app, port=8001)
