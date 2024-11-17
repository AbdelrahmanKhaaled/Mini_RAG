from fastapi import FastAPI
app = FastAPI()

@app.get("/welcome")
def welcome():
    return {"messag": "Welcome, Hello world"}