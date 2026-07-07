from pathlib import Path
import shutil
import uuid
import logging


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.pipeline import TreeDetectionPipeline

# -------------------------------------------------------
# Logging
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------
# App setup
# -------------------------------------------------------

app = FastAPI(
    title="Tree Detection API",
    description="Real-time and batch tree detection with YOLO + SAM2",
)

# CORS — allow browser dashboard to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Shared resources (loaded once at startup)
# -------------------------------------------------------

# Full pipeline (includes SAM2) — used for /detect and /capture
pipeline = TreeDetectionPipeline()



# -------------------------------------------------------
# Directories
# -------------------------------------------------------

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)


# -------------------------------------------------------
# Static mounts
# -------------------------------------------------------

# Serve pipeline outputs (annotated images, metadata, masks)
app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs",
)

# Serve dashboard static assets
app.mount(
    "/css",
    StaticFiles(directory="dashboard/css"),
    name="css",
)
app.mount(
    "/js",
    StaticFiles(directory="dashboard/js"),
    name="js",
)



# -------------------------------------------------------
# Dashboard (served at root — must be mounted last)
# -------------------------------------------------------

DASHBOARD_DIR = Path("dashboard")
if DASHBOARD_DIR.exists():
    # Mount assets static files
    if (DASHBOARD_DIR / "assets").exists():
        app.mount(
            "/assets",
            StaticFiles(directory=str(DASHBOARD_DIR / "assets")),
            name="assets",
        )

    # Serve index.html at root (dashboard)
    @app.get("/", response_class=FileResponse)
    async def serve_dashboard():
        return FileResponse(str(DASHBOARD_DIR / "index.html"))

    # Serve upload dashboard page
    @app.get("/upload", response_class=FileResponse)
    async def serve_upload_dashboard():
        return FileResponse(str(DASHBOARD_DIR / "index.html"))

    # Catch-all route to serve the React SPA
    @app.get("/{catchall:path}", response_class=FileResponse)
    async def serve_react_app(catchall: str):
        return FileResponse(str(DASHBOARD_DIR / "index.html"))


# -------------------------------------------------------
# Health check
# -------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------------------------------
# POST /detect — Full pipeline (existing, preserved)
# -------------------------------------------------------

@app.post("/detect")
async def detect_tree(
    file: UploadFile = File(...)
):
    extension = (
        Path(file.filename)
        .suffix
        .lower()
    )

    if extension not in [".jpg", ".jpeg", ".png", ".heic"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format",
        )

    image_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{image_id}{extension}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = pipeline.run(file_path)

    return {
        "image_id": image_id,
        **result,
    }


# -------------------------------------------------------
# GET /results — List metadata results (existing, preserved)
# -------------------------------------------------------

@app.get("/results")
def list_results():
    metadata_dir = Path("outputs/metadata")
    files = list(metadata_dir.glob("*.json"))
    return {
        "count": len(files),
        "files": [f.name for f in files],
    }


# -------------------------------------------------------
# GET /results/{file_name} — Get specific result (existing, preserved)
# -------------------------------------------------------

import json

@app.get("/results/{file_name}")
def get_result(file_name: str):
    file_path = Path("outputs/metadata") / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    with open(file_path) as f:
        return json.load(f)

