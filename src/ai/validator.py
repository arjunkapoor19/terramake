import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def validate_terraform(tf_code: str) -> str:
    prompt = f"""
You are an expert DevOps engineer.

Review the following Terraform code and provide:
- Security issues
- Best practice improvements
- Missing configurations

Be concise and practical.

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
        return f"⚠️ Groq API Error: {str(e)}"