from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import markdown  # ✅ Required for Markdown rendering

from .database import SessionLocal
from .models import Article, Category, Revision

app = FastAPI()

# Static and templates setup
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
    categories = db.query(Category).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "articles": articles,
        "categories": categories
    })

@app.get("/articles/new")
def new_article_form(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return templates.TemplateResponse("new_article.html", {
        "request": request,
        "categories": categories
    })

@app.post("/articles/new")
def create_article(
    title: str = Form(...),
    content: str = Form(...),
    category_ids: List[int] = Form(default=[]),
    db: Session = Depends(get_db)
):
    article = Article(title=title, is_redirect=False, created_by=1)

    if category_ids:
        article.categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    db.add(article)
    db.commit()  # commits to get the ID

    revision = Revision(
        article_id=article.id,
        content=content,
        edited_by=1,
        summary="Initial version",
        edited_at=datetime.utcnow()
    )

    db.add(revision)
    db.commit()

    return RedirectResponse("/", status_code=303)

@app.get("/articles/{article_id}/edit")
def edit_article_form(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    latest = db.query(Revision).filter(Revision.article_id == article_id).order_by(Revision.edited_at.desc()).first()

    return templates.TemplateResponse("edit_article.html", {
        "request": request,
        "article": article,
        "latest": latest
    })

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
        summary=summary or "Updated content",
        edited_at=datetime.utcnow()
    )
    db.add(revision)
    db.commit()

    return RedirectResponse("/", status_code=303)

import markdown

@app.get("/articles/{article_id}/history")
def article_history(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    revisions = (
        db.query(Revision)
        .filter(Revision.article_id == article_id)
        .order_by(Revision.edited_at.desc())
        .all()
    )

    for rev in revisions:
        rev.rendered = markdown.markdown(rev.content or "", extensions=["fenced_code", "tables"])

    return templates.TemplateResponse("article_history.html", {
        "request": request,
        "article": article,
        "revisions": revisions
    })

@app.get("/categories/{category_id}")
def category_view(category_id: int, request: Request, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    articles = (
        db.query(Article)
        .join(Article.categories)
        .filter(Category.id == category_id)
        .all()
    )

    return templates.TemplateResponse("category.html", {
        "request": request,
        "category": category,
        "articles": articles
    })

@app.get("/articles/{article_id}")
def article_detail(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    latest_revision = (
        db.query(Revision)
        .filter(Revision.article_id == article_id)
        .order_by(Revision.edited_at.desc())
        .first()
    )

    rendered_html = markdown.markdown(
        latest_revision.content or "",
        extensions=["fenced_code", "tables"]
    )

    return templates.TemplateResponse("article_detail.html", {
        "request": request,
        "article": article,
        "latest_revision": latest_revision,
        "rendered_html": rendered_html
    })
