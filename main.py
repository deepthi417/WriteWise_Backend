import google.generativeai as genai
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSM
import logging
from fastapi import FastAPI, HTTPExceptioniddleware


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# ✅ Fix CORS issue: Allow frontend (Netlify) to call backend (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["https://yourfrontend.netlify.app"] if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.post("/enhance/")
async def enhance_text(request: TextRequest):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Improve the structure and readability of this text: {request.text}"
    response = model.generate_content(prompt)
    return {"enhanced_text": response.text}

# 3️⃣ Writing Style Analysis (Clarity, Tone, Readability)
@app.post("/analyze/")
async def analyze_text(request: TextRequest):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Analyze the following text and provide feedback on clarity, tone, and readability: {request.text}"
    response = model.generate_content(prompt)
    return {"analysis": response.text}

# 4️⃣ Summarization & Paraphrasing
@app.post("/summarize/")
async def summarize_text(request: TextRequest):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following text in a concise way: {request.text}"
    response = model.generate_content(prompt)
    return {"summary": response.text}

@app.post("/paraphrase/")
async def paraphrase_text(request: TextRequest):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Paraphrase this text while keeping the original meaning: {request.text}"
    response = model.generate_content(prompt)
    return {"paraphrased_text": response.text}

