import os
from dotenv import load_dotenv
from google.ai import generativelanguage as gl

load_dotenv()

# إنشاء العميل
client = gl.TextServiceClient()

def rewrite_math_problem(problem: str, theme: str) -> str:
    system_message = (
        "You are a helpful assistant that rewrites math word problems by changing only the context "
        "to match a student's interest. You must strictly follow these rules:\n"
        "- Do NOT start with 'Sure!', 'Let's', 'Imagine', or any similar introduction.\n"
        "- Do NOT add any preamble, explanation, commentary, or formatting (no bold, markdown, or newlines).\n"
        "- Only return the rewritten math problem sentence, nothing more.\n"
        "- Preserve the original structure and difficulty of the problem."
    )

    user_prompt = (
        f"Rewrite this math problem using the theme '{theme}'. "
        f"Only return the final rewritten sentence, and nothing else.\n\n"
        f"Original: {problem}\nRewritten:"
    )

    prompt_text = f"{system_message}\n\n{user_prompt}"

    response = client.generate_text(
        model="gpt-4o-mini",  # استخدم اسم النموذج الصحيح من Google
        prompt=gl.TextPrompt(text=prompt_text),
        temperature=0.7,
        max_tokens=256,
    )

    return response.result.strip()
