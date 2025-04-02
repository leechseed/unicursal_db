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

from fastapi import HTTPException

@app.get("/articles/{article_id}/edit")
def edit_article_form(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    latest = db.query(Revision).filter(Revision.article_id == article_id).order_by(Revision.edited_at.desc()).first()
    return templates.TemplateResponse("edit_article.html", {"request": request, "article": article, "latest": latest})


@app.post("/articles/{article_id}/edit")
def submit_article_edit(
    article_id: int,
    content: str = Form(...),
    summary: str = Form(""),
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    revision = Revision(
        article_id=article.id,
        content=content,
        edited_by=1,
        summary=summary or "Updated content"
    )
    db.add(revision)
    db.commit()

    return RedirectResponse("/", status_code=303)

@app.get("/articles/{article_id}/history")
def article_history(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    revisions = db.query(Revision).filter(Revision.article_id == article_id).order_by(Revision.edited_at.desc()).all()

    return templates.TemplateResponse("article_history.html", {
        "request": request,
        "article": article,
        "revisions": revisions
    })
