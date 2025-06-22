from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# إعداد مفتاح Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# إنشاء التطبيق
app = FastAPI()

# تفعيل CORS (مفيد عند الربط مع الواجهة الأمامية)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكن تقييدها لاحقاً لأمان أفضل
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تهيئة نموذج Gemini
model = genai.GenerativeModel("models/gemini-pro")

# نموذج البيانات المرسلة من المستخدم
class ProblemRequest(BaseModel):
    problem: str
    theme: str

# نقطة النهاية لإعادة صياغة السؤال
@app.post("/api/rewrite-problem")
async def rewrite_problem(request: ProblemRequest):
    try:
        prompt = f"Rewrite the following math problem using the theme '{request.theme}': {request.problem}"
        response = model.generate_content(prompt)
        rewritten = response.text
        return {"rewritten_problem": rewritten}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
