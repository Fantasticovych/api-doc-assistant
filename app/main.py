from fastapi import FastAPI

app = FastAPI(
    title="API Doc Assistant",
    description="LLM-Powered API Documentation Assistant",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to API Doc Assistant!"}