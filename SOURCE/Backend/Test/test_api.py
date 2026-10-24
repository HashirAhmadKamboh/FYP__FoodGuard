from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/predict/")
async def predict_food(request: Request):
    print("HEADERS:", request.headers)
    body = await request.body()
    print("BODY LENGTH:", len(body))
    print("BODY SNIPPET:", body[:200])
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
