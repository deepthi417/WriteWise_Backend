import google.generativeai as genai
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import FastAPI, HTTPException
import traceback
from fastapi.responses import JSONResponse

app = FastAPI()


# ✅ Fix CORS issue: Allow frontend (Netlify) to call backend (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["https://yourfrontend.netlify.app"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import logging
from fastapi import FastAPI, HTTPException

# Setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    logger.info(f"Received request for item with ID: {item_id}")  # Log the request
    return {"item_id": item_id}

@app.post("/items/")
def create_item(item: dict):
    logger.info(f"Creating new item: {item}")  # Log the creation
    return {"message": "Item created", "item": item}

@app.get("/cause-error")
def cause_error():
    try:
        # Simulate an error (ZeroDivisionError)
        1 / 0
    except ZeroDivisionError as e:
        logger.error(f"Error occurred: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
def home():
    return {"message": "WriteWise API is running!"}



# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("AIzaSyCFb0Vz1A2NtmK-oEzCHPXtQdFXgPDUswI")
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Define Request Model
class TextRequest(BaseModel):
    text: str

# Home Route
@app.get("/")
def read_root():
    return {"message": "WriteWise AI Agent is running!"}


# Your existing request model
class CorrectRequest(BaseModel):
    text: str
    tone: str
    style: str
    audience: str


# 1️⃣ Grammar & Spelling Correction
@app.post("/correct")
async def correct_text(request: CorrectRequest):
    try:
        logger.info(f"Received request: {request.dict()}")  # Log the incoming request

        # --- Your existing AI logic here ---
        corrected_text = request.text.upper()  # Example logic (Replace with actual AI processing)
        # ------------------------------------

        logger.info(f"Returning response: {corrected_text}")  # Log the response
        return {"corrected_text": corrected_text}
    
    except Exception as e:
        logger.error(f"Error in /correct endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 2️⃣ Content Structuring & Enhancement

app = FastAPI()

class EnhanceRequest(BaseModel):
    text: str
    tone: str = "Neutral"
    style: str = "Standard"

@app.post("/enhance")
async def enhance_text(request: EnhanceRequest):
    try:
        enhanced_text = f"Enhanced: '{request.text}' with {request.tone} tone and {request.style} style."
        return {"enhanced_text": enhanced_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3️⃣ Writing Style Analysis (Clarity, Tone, Readability)
class StyleAnalysisRequest(BaseModel):
     text: str

@app.post("/analyze_style/")
async def analyze_writing_style(request: StyleAnalysisRequest):
    try:
        logger.info(f"Received request: {request.dict()}")  # Log input request

        # Simulated style analysis logic (Replace with AI model)
        clarity_score = 85  # Mock clarity score
        tone_analysis = "Formal"  # Mock tone classification
        readability = "Grade 9 Level"  # Mock readability level

        logger.info(f"Returning style analysis: Clarity={clarity_score}, Tone={tone_analysis}, Readability={readability}")
        return {
            "clarity_score": clarity_score,
            "tone_analysis": tone_analysis,
            "readability": readability
        }

    except Exception as e:
        logger.error(f"Error in /analyze_style/: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
# 4️⃣ Summarization & Paraphrasing
class TextInput(BaseModel):
    text: str

@app.post("/summarize/")
def summarize_text(input_data: TextInput):
    if not input_data.text:
        raise HTTPException(status_code=422, detail="Text input is required")
    
    try:
        # Fake summarization logic for testing
        summary = "This is a summary: " + input_data.text
        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ParaphraseRequest(BaseModel):
    text: str

@app.post("/paraphrase/")
async def paraphrase_text(request: ParaphraseRequest):
    try:
        logger.info(f"Received request: {request.dict()}")  # Log input request

        # Simulate paraphrasing logic
        paraphrased_text = f"Paraphrased version of: {request.text}"

        logger.info(f"Returning paraphrased text: {paraphrased_text}")
        return {"paraphrased_text": paraphrased_text}

    except Exception as e:
        logger.error(f"Error in /paraphrase/: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

