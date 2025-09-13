import os
import time
import uuid
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
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(colors=True) if ENV == "development" else structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
log = structlog.get_logger("llm-service")

# --- Uygulama Başlatma ---
app = FastAPI(title="Sentiric LLM Service")

llm_model = None

@app.on_event("startup")
def startup_event():
    global llm_model
    try:
        api_key = os.getenv("LLM_SERVICE_API_KEY")
        if not api_key or "YOUR" in api_key:
            raise ValueError("LLM_SERVICE_API_KEY ortam değişkeni bulunamadı veya geçerli değil.")
        genai.configure(api_key=api_key)
        model_name = os.getenv("LLM_SERVICE_MODEL_NAME", "gemini-2.0-flash")
        llm_model = genai.GenerativeModel(model_name)
        log.info("LLM adapter initialized successfully", model=model_name)
    except Exception as e:
        log.critical("LLM adapter initialization failed", error=str(e))
        llm_model = None

# --- Middleware ---
@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    clear_contextvars()
    start_time = time.perf_counter()
    
    trace_id = request.headers.get("X-Trace-ID") or f"llm-trace-{uuid.uuid4()}"
    bind_contextvars(trace_id=trace_id)

    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    
    log.info(
        "Request completed",
        http_method=request.method,
        http_path=request.url.path,
        http_status_code=response.status_code,
        duration_ms=round(process_time, 2),
    )
    return response

# --- API Modelleri ve Endpoint'ler ---
class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    text: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    if not llm_model:
        log.error("LLM service is not available due to initialization failure.")
        raise HTTPException(status_code=503, detail="LLM service not available")

    log.info("Generate request received", prompt_length=len(request.prompt))
    try:
        response = llm_model.generate_content(request.prompt)
        response_text = response.text
        log.info("Generate response successful", response_length=len(response_text))
        return GenerateResponse(text=response_text)
    except Exception as e:
        log.error("LLM API error", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal LLM provider error")

@app.get("/health", tags=["Health"])
@app.head("/health")
async def health_check():
    return {"status": "ok", "llm_model_loaded": bool(llm_model)}