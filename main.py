"""app"""
__docformat__ = "numpy"

import json
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn

from bot import models, schemas, helpers, utils, database

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def docs(request: Request):
    with open("bot/data/options.json", encoding="utf-8") as json_file:
        options = json.load(json_file)
        return templates.TemplateResponse(
            "home.html", {"request": request, "result": options}
        )


@app.post("/", status_code=200)
def webhook(
    message: schemas.Message,
    db: Session = Depends(database.get_db),  # noqa: B008
):
    helpers.handler(message)
    utils.add_post(db, message)
    return {}


@app.get("/messages", response_class=HTMLResponse)
def messages(
    request: Request,
    db: Session = Depends(database.get_db),  # noqa: B008
):
    return templates.TemplateResponse(
        "messages.html", {"request": request, "users": db.query(models.Post).all()}
    )


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0")
