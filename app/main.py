from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Article
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def homepage(request: Request, db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return templates.TemplateResponse("home.html", {"request": request, "articles": articles})

from fastapi import Form
from fastapi.responses import RedirectResponse
from app.models import Article, Revision

@app.get("/articles/new")
def new_article_form(request: Request):
    return templates.TemplateResponse("new_article.html", {"request": request})

@app.post("/articles/new")
def create_article(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    article = Article(title=title, is_redirect=False, created_by=1)
    db.add(article)
    db.flush()  # Get article.id before creating revision

    revision = Revision(
        article_id=article.id,
        content=content,
        edited_by=1,
        summary="Initial version"
    )
    db.add(revision)
    db.commit()

    return RedirectResponse("/", status_code=303)
