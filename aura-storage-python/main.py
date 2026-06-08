import os
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from services.analysis_service import AnalysisService
from services.health_service import HealthService
from services.power_service import PowerService
from services.security_service import SecurityService

app = FastAPI(title="AURA STORAGE", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

analysis_svc = AnalysisService()
health_svc   = HealthService()
power_svc    = PowerService()
security_svc = SecurityService()

# ── Page Routes ──────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/module/1", response_class=HTMLResponse)
async def module1(request: Request):
    return templates.TemplateResponse("module1.html", {"request": request})

@app.get("/module/2", response_class=HTMLResponse)
async def module2(request: Request):
    return templates.TemplateResponse("module2.html", {"request": request})

@app.get("/module/3", response_class=HTMLResponse)
async def module3(request: Request):
    return templates.TemplateResponse("module3.html", {"request": request})

@app.get("/module/4", response_class=HTMLResponse)
async def module4(request: Request):
    return templates.TemplateResponse("module4.html", {"request": request})

# ── Module 1 API ─────────────────────────────────────────────────────────────

@app.post("/api/module1/analyze")
async def analyze_video(
    file: UploadFile = File(...),
    yolo_threshold: float = Form(0.5),
    ssim_threshold: float = Form(0.97),
):
    content = await file.read()
    result = analysis_svc.analyze(
        file.filename or "video.mp4", len(content), yolo_threshold, ssim_threshold
    )
    return JSONResponse(result)

@app.get("/api/module1/stats")
async def analysis_stats():
    return JSONResponse(analysis_svc.get_stats())

# ── Module 2 API ─────────────────────────────────────────────────────────────

@app.get("/api/module2/health")
async def drive_health(scenario: str = "healthy"):
    return JSONResponse(health_svc.generate_health_data(scenario))

@app.get("/api/module2/predict")
async def predict_failure(scenario: str = "healthy", days: int = 14):
    return JSONResponse(health_svc.predict_failure(scenario, days))

# ── Module 3 API ─────────────────────────────────────────────────────────────

@app.post("/api/module3/encrypt")
async def encrypt_data(payload: dict):
    result = security_svc.encrypt_and_shard(
        payload.get("data", "sample"),
        int(payload.get("threshold", 3)),
        int(payload.get("total", 5)),
    )
    return JSONResponse(result)

@app.post("/api/module3/reconstruct")
async def reconstruct_data(payload: dict):
    return JSONResponse(security_svc.reconstruct(payload))

@app.post("/api/module3/demo")
async def run_demo(payload: dict):
    return JSONResponse(security_svc.run_demo(
        int(payload.get("secret", 42)),
        int(payload.get("threshold", 3)),
        int(payload.get("total", 5)),
    ))

# ── Module 4 API ─────────────────────────────────────────────────────────────

@app.post("/api/module4/write")
async def simulate_write(payload: dict):
    return JSONResponse(power_svc.simulate_write(int(payload.get("sizeKb", 1))))

@app.get("/api/module4/stats")
async def power_stats():
    return JSONResponse(power_svc.get_stats())

@app.post("/api/module4/reset")
async def reset_power():
    power_svc.reset()
    return JSONResponse({"status": "reset"})

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
