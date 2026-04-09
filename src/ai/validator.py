import os
from dotenv import load_dotenv
from groq import Groq
from src.utils.analyzer import get_rejected_patterns, extract_patterns

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def review_terraform(tf_code: str) -> str:
    prompt = f"""
You are a senior DevOps engineer reviewing Terraform code.

Analyze the code and respond STRICTLY in the following format:

[SECURITY]
- issue 1
- issue 2

[BEST_PRACTICES]
- suggestion 1
- suggestion 2

[MISSING]
- missing config 1
- missing config 2

Rules:
- Be concise
- No explanations
- No paragraphs
- Only bullet points
- If nothing in a section, write: None

Terraform:
{tf_code}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {str(e)}"
    
raw_rejected = get_rejected_patterns()
patterns = extract_patterns(raw_rejected)
    
def suggest_fixes(tf_code: str) -> str:
    prompt = f"""
You are a senior DevOps engineer.

Avoid these known bad practices:
{patterns}

Rules:
- DO NOT rewrite entire resources
- ONLY suggest minimal fixes

Given Terraform code, suggest FIXES.

STRICT FORMAT:

[FIXES]
- Problem: ...
  Fix:
  <minimal change only>

Rules:
- DO NOT rewrite entire resources
- ONLY show the smallest possible change
- Mention WHERE to apply the fix
- Use short Terraform snippets
- No full files
- No duplication

Example:

- Problem: Missing tags
  Fix:
  Add inside aws_s3_bucket:
  tags = {{
    Environment = "dev"
  }}

Terraform:
{tf_code}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # fast + stable
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {str(e)}"
    
