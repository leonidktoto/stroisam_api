from fastapi import FastAPI

app=FastAPI()


@app.get("/category")
def get_category():
    return "категории"