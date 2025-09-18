import os
import uuid
import structlog
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import google.generativeai as genai
from structlog.contextvars import bind_contextvars, clear_contextvars
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import setup_logging

SERVICE_NAME = "llm-service"
llm_model = None
log = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm_model, log
    
    setup_logging(log_level=settings.LOG_LEVEL, env=settings.ENV)
    log = structlog.get_logger().bind(service=SERVICE_NAME)
    
    # --- DEĞİŞİKLİK: Log Mesajları Türkçeleştirildi ---
    log.info(
        "Uygulama başlatılıyor...", 
        project=settings.PROJECT_NAME,
        version=settings.SERVICE_VERSION,
        commit=settings.GIT_COMMIT,
        build_date=settings.BUILD_DATE,
    )
    
    try:
        api_key = os.getenv("LLM_SERVICE_API_KEY")
        if not api_key or "YOUR" in api_key:
            raise ValueError("LLM_SERVICE_API_KEY ortam değişkeni bulunamadı veya geçerli değil.")
        genai.configure(api_key=api_key)
        model_name = os.getenv("LLM_SERVICE_MODEL_NAME", "gemini-1.5-flash")
        llm_model = genai.GenerativeModel(model_name)
        log.info("LLM adaptörü başarıyla başlatıldı", model=model_name)
    except Exception as e:
        log.critical("KRİTİK HATA: LLM adaptörü başlatılamadı", error=str(e), exc_info=True)
        llm_model = None
        
    yield
    log.info("Uygulama kapatılıyor...")
    # --- DEĞİŞİKLİK SONU ---

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    clear_contextvars()
    
    if request.url.path in ["/health", "/healthz"]:
        return await call_next(request)
    
    trace_id = request.headers.get("X-Trace-ID") or f"llm-trace-{uuid.uuid4()}"
    bind_contextvars(trace_id=trace_id)

    # --- DEĞİŞİKLİK: Log Mesajları Türkçeleştirildi ---
    log.info("İstek alındı", http_method=request.method, http_path=request.url.path)
    response = await call_next(request)
    log.info("İstek tamamlandı", http_status_code=response.status_code)
    # --- DEĞİŞİKLİK SONU ---
    return response

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    text: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    if not llm_model:
        log.error("LLM servisi başlatma hatası nedeniyle kullanılamıyor.")
        raise HTTPException(status_code=503, detail="LLM servisi mevcut değil")

    # --- DEĞİŞİKLİK: Log Mesajları Türkçeleştirildi ---
    log.info("Metin üretme isteği alındı", prompt_length=len(request.prompt))
    log.debug("Alınan tam prompt", prompt=request.prompt)
    
    try:
        response = llm_model.generate_content(request.prompt)
        response_text = response.text
        log.info("Metin başarıyla üretildi", response_length=len(response_text))
        log.debug("Üretilen tam metin", response_text=response_text)
        return GenerateResponse(text=response_text)
    except Exception as e:
        log.error("LLM API hatası", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Dahili LLM sağlayıcı hatası")
    # --- DEĞİŞİKLİK SONU ---

@app.get("/health", tags=["Health"])
@app.head("/health")
async def health_check():
    return {"status": "ok", "llm_model_loaded": bool(llm_model)}

@app.get("/healthz", include_in_schema=False)
async def healthz_check():
    return Response(status_code=200)