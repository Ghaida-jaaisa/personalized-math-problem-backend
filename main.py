from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = genai.GenerativeModel("models/gemini-pro")

class ProblemRequest(BaseModel):
    problem: str
    theme: str

def rewrite_math_problem(problem: str, theme: str) -> str:
    system_message = (
        "You are a helpful assistant that rewrites math word problems by changing only the context "
        "to match a student's interest. You must strictly follow these rules:\n"
        "- Do NOT start with 'Sure!', 'Let's', 'Imagine', or any similar introduction.\n"
        "- Do NOT add any preamble, explanation, commentary, or formatting (no bold, markdown, or newlines).\n"
        "- Only return the rewritten math problem sentence, nothing more.\n"
        "- Preserve the original structure and difficulty of the problem."
    )

    prompt = (
        f"{system_message}\nRewrite the following math problem using the theme '{theme}': {problem}"
    )

    response = model.generate_content(prompt)
    return response.text.strip()

@app.post("/api/rewrite-problem")
async def rewrite_problem(request: ProblemRequest):
    try:
        rewritten = rewrite_math_problem(request.problem, request.theme)
        return {"rewritten_problem": rewritten}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
