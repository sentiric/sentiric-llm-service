# sentiric-llm-service/app.py
import os
import time
import uuid # YENİ
import structlog
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import logging
from structlog.contextvars import bind_contextvars, clear_contextvars

# --- Konfigürasyon ve Loglama Kurulumu ---
load_dotenv()
ENV = os.getenv("ENV", "production")
LOG_LEVEL = logging.INFO
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer() if ENV == "development" else structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)
log = structlog.get_logger(service="llm-service")

# --- Uygulama Başlatma ---
app = FastAPI()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or "YOUR" in api_key: # API key'in geçerli olup olmadığını kontrol et
        raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı veya geçerli değil.")
    genai.configure(api_key=api_key)
    llm_model = genai.GenerativeModel('gemini-1.5-flash')
    log.info("gemini_adapter.initialized_successfully")
except Exception as e:
    log.critical("gemini_adapter.initialization_failed", error=str(e))
    llm_model = None

# --- Middleware: Her istek için otomatik loglama ve trace_id ---
@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    clear_contextvars()
    start_time = time.perf_counter()
    
    # YENİ: Gelen header'dan trace_id'yi yakala, yoksa yeni bir tane oluştur.
    trace_id = request.headers.get("X-Trace-ID") or f"trace-llm-{uuid.uuid4()}"
    bind_contextvars(trace_id=trace_id)

    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    
    log.info(
        "http.request.completed",
        http_method=request.method,
        http_path=request.url.path,
        http_status_code=response.status_code,
        duration_ms=f"{process_time:.2f}",
    )
    return response

# --- API Modelleri ---
class GenerateRequest(BaseModel):
    prompt: str
    conversation_history: list = []

class GenerateResponse(BaseModel):
    text: str

# --- API Endpoint'leri ---
@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    if not llm_model:
        log.error("llm_service.not_available")
        raise HTTPException(status_code=503, detail="LLM service not available")

    log.info("llm_service.generate.request_received", prompt_length=len(request.prompt))
    try:
        response = llm_model.generate_content(request.prompt)
        response_text = response.text
        log.info("llm_service.generate.response_generated", response_length=len(response_text))
        return GenerateResponse(text=response_text)
    except Exception as e:
        log.error("gemini.api_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal LLM error")

@app.get("/health")
async def health_check():
    health_status = {"status": "ok", "llm_model_loaded": bool(llm_model)}
    log.info("health_check.performed", **health_status)
    return health_status