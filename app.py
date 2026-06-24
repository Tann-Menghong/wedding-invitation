import os
import json
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Wedding Invitation")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
CONTENT_FILE = DATA_DIR / "content.json"
MESSAGES_FILE = DATA_DIR / "messages.json"
GALLERY_FILE = DATA_DIR / "gallery.json"

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
jinja_env = Environment(loader=FileSystemLoader(str(BASE_DIR / "templates")), autoescape=True)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "wedding2025")


def load_content() -> dict:
    if CONTENT_FILE.exists():
        with open(CONTENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_content(data: dict):
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_messages() -> list:
    if MESSAGES_FILE.exists():
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_messages(messages: list):
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def load_gallery() -> list:
    if GALLERY_FILE.exists():
        with open(GALLERY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_gallery(photos: list):
    with open(GALLERY_FILE, "w", encoding="utf-8") as f:
        json.dump(photos, f, ensure_ascii=False, indent=2)


def check_admin(request: Request):
    token = request.cookies.get("admin_token")
    if token != "authenticated":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, name: Optional[str] = None):
    content = load_content()
    messages = load_messages()
    gallery = load_gallery()
    template = jinja_env.get_template("index.html")
    html = template.render(content=content, messages=messages, gallery=gallery, guest_name=name)
    return HTMLResponse(content=html)


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    token = request.cookies.get("admin_token")
    template = jinja_env.get_template("admin.html")
    if token != "authenticated":
        html = template.render(authenticated=False, content={}, messages=[], gallery=[])
        return HTMLResponse(content=html)
    content = load_content()
    messages = load_messages()
    gallery = load_gallery()
    html = template.render(authenticated=True, content=content, messages=messages, gallery=gallery)
    return HTMLResponse(content=html)


@app.post("/admin/login")
async def admin_login(request: Request):
    form = await request.form()
    password = form.get("password", "")
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie("admin_token", "authenticated", httponly=True, max_age=86400)
        return response
    response = RedirectResponse(url="/admin?error=1", status_code=303)
    return response


@app.post("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin", status_code=303)
    response.delete_cookie("admin_token")
    return response


@app.post("/api/content")
async def update_content(request: Request):
    check_admin(request)
    form = await request.form()
    content = load_content()

    for key in form:
        if key.startswith("file_"):
            continue
        keys = key.split(".")
        obj = content
        for k in keys[:-1]:
            if k not in obj:
                obj[k] = {}
            obj = obj[k]
        obj[keys[-1]] = form[key]

    save_content(content)
    return {"status": "ok"}


@app.post("/api/content/schedule")
async def update_schedule(request: Request):
    check_admin(request)
    body = await request.json()
    content = load_content()
    content["schedule"] = body.get("schedule", [])
    save_content(content)
    return {"status": "ok"}


@app.post("/api/upload/hero")
async def upload_hero(request: Request, file: UploadFile = File(...)):
    check_admin(request)
    ext = Path(file.filename).suffix
    filename = f"hero{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    content = load_content()
    content["hero"]["hero_image"] = f"/static/uploads/{filename}"
    save_content(content)
    return {"status": "ok", "path": f"/static/uploads/{filename}"}


@app.post("/api/upload/music")
async def upload_music(request: Request, file: UploadFile = File(...)):
    check_admin(request)
    ext = Path(file.filename).suffix
    filename = f"music{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    content = load_content()
    content["hero"]["background_music"] = f"/static/uploads/{filename}"
    save_content(content)
    return {"status": "ok", "path": f"/static/uploads/{filename}"}


@app.post("/api/upload/qr-usd")
async def upload_qr_usd(request: Request, file: UploadFile = File(...)):
    check_admin(request)
    ext = Path(file.filename).suffix
    filename = f"qr_usd{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    content = load_content()
    content["qr"]["usd_image"] = f"/static/uploads/{filename}"
    save_content(content)
    return {"status": "ok", "path": f"/static/uploads/{filename}"}


@app.post("/api/upload/qr-khr")
async def upload_qr_khr(request: Request, file: UploadFile = File(...)):
    check_admin(request)
    ext = Path(file.filename).suffix
    filename = f"qr_khr{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    content = load_content()
    content["qr"]["khr_image"] = f"/static/uploads/{filename}"
    save_content(content)
    return {"status": "ok", "path": f"/static/uploads/{filename}"}


@app.post("/api/upload/map")
async def upload_map(request: Request, file: UploadFile = File(...)):
    check_admin(request)
    ext = Path(file.filename).suffix
    filename = f"map{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    content = load_content()
    content["venue"]["map_image"] = f"/static/uploads/{filename}"
    save_content(content)
    return {"status": "ok", "path": f"/static/uploads/{filename}"}


@app.post("/api/gallery/upload")
async def upload_gallery_photo(request: Request, file: UploadFile = File(...)):
    check_admin(request)
    ext = Path(file.filename).suffix
    filename = f"gallery_{uuid.uuid4().hex[:8]}{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    gallery = load_gallery()
    entry = {
        "id": uuid.uuid4().hex[:8],
        "filename": filename,
        "path": f"/static/uploads/{filename}",
        "uploaded_at": datetime.now().isoformat(),
    }
    gallery.append(entry)
    save_gallery(gallery)
    return {"status": "ok", "photo": entry}


@app.delete("/api/gallery/{photo_id}")
async def delete_gallery_photo(request: Request, photo_id: str):
    check_admin(request)
    gallery = load_gallery()
    photo = next((p for p in gallery if p["id"] == photo_id), None)
    if photo:
        filepath = UPLOAD_DIR / photo["filename"]
        if filepath.exists():
            filepath.unlink()
    gallery = [p for p in gallery if p["id"] != photo_id]
    save_gallery(gallery)
    return {"status": "ok"}


@app.post("/api/messages")
async def add_message(request: Request):
    body = await request.json()
    name = body.get("name", "").strip()
    text = body.get("message", "").strip()
    status = body.get("status", "attend").strip() or "attend"
    if not name or not text:
        raise HTTPException(status_code=400, detail="Name and message are required")
    messages = load_messages()
    entry = {
        "id": uuid.uuid4().hex[:8],
        "name": name,
        "message": text,
        "status": status,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    messages.insert(0, entry)
    save_messages(messages)
    return {"status": "ok", "message": entry}


@app.get("/api/messages")
async def get_messages():
    messages = load_messages()
    return messages


@app.delete("/api/messages/{msg_id}")
async def delete_message(request: Request, msg_id: str):
    check_admin(request)
    messages = load_messages()
    messages = [m for m in messages if m["id"] != msg_id]
    save_messages(messages)
    return {"status": "ok"}


@app.get("/api/content")
async def get_content():
    return load_content()


@app.get("/api/gallery")
async def get_gallery():
    return load_gallery()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
