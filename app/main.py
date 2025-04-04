from app import auth
from app.auth import get_current_user

from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import markdown

from .database import SessionLocal
from .models import Article, Category, Revision, Tag

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
def homepage(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    articles = db.query(Article).all()
    categories = db.query(Category).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "articles": articles,
        "categories": categories,
        "user": user
    })

@app.get("/search")
def search(request: Request, q: str = "", db: Session = Depends(get_db), user=Depends(get_current_user)):
    articles = db.query(Article).filter(Article.title.ilike(f"%{q}%")).all()
    return templates.TemplateResponse("search_results.html", {
        "request": request,
        "articles": articles,
        "query": q,
        "user": user
    })

@app.get("/articles/new")
def new_article_form(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user:
        return RedirectResponse("/login", status_code=303)
    categories = db.query(Category).all()
    tags = db.query(Tag).all()  # New: fetch all tags
    return templates.TemplateResponse("new_article.html", {
        "request": request,
        "categories": categories,
        "tags": tags
    })

@app.post("/articles/new")
def create_article(
    title: str = Form(...),
    content: str = Form(...),
    category_ids: List[int] = Form(default=[]),
    tag_ids: List[int] = Form(default=[]),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user:
        return RedirectResponse("/login", status_code=303)

    article = Article(title=title, is_redirect=False, created_by=user.id)

    if category_ids:
        article.categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    if tag_ids:
        article.tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    db.add(article)
    db.flush()  # flush to assign article.id

    revision = Revision(
        article_id=article.id,
        content=content,
        edited_by=user.id,
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

app.include_router(auth.router)

from typing import List

@app.post("/articles/new")
def create_article(
    title: str = Form(...),
    content: str = Form(...),
    category_ids: List[int] = Form(default=[]),
    tag_ids: List[int] = Form(default=[]),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    article = Article(title=title, is_redirect=False, created_by=user.id)

    if category_ids:
        article.categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    if tag_ids:
        article.tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    db.add(article)
    db.flush()

    revision = Revision(
        article_id=article.id,
        content=content,
        edited_by=user.id,
        summary="Initial version"
    )
    db.add(revision)
    db.commit()

    return RedirectResponse("/", status_code=303)

from app.models import Tag

@app.get("/tags/{tag_id}")
def tag_view(tag_id: int, request: Request, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    articles = tag.articles

    return templates.TemplateResponse("tag.html", {
        "request": request,
        "tag": tag,
        "articles": articles
    })
