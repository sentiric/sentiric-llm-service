import os
import structlog
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# --- Konfigürasyon ---
load_dotenv()
log = structlog.get_logger()
app = FastAPI()

# Gemini modelini başlatma
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı.")
    genai.configure(api_key=api_key)
    llm_model = genai.GenerativeModel('gemini-1.5-flash')
    log.info("gemini_adapter_initialized_successfully")
except Exception as e:
    log.critical("gemini_adapter_initialization_failed", error=str(e))
    llm_model = None

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
        raise HTTPException(status_code=503, detail="LLM service not available")

    log.info("llm_request_received", prompt_length=len(request.prompt))
    try:
        # TODO: Konuşma geçmişi (request.conversation_history) entegrasyonu eklenecek
        response = llm_model.generate_content(request.prompt)
        log.info("llm_response_generated", response_length=len(response.text))
        return GenerateResponse(text=response.text)
    except Exception as e:
        log.error("gemini_api_error", error=str(e))
        raise HTTPException(status_code=500, detail="Internal LLM error")

@app.get("/health")
async def health_check():
    return {"status": "ok", "llm_model_loaded": bool(llm_model)}