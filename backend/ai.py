import anthropic
from dotenv import load_dotenv

from models import AnalysisResult

load_dotenv()  # must run before the client is created

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

SYSTEM_PROMPT = """You are an experienced technical recruiter and career coach.
You analyze how well a resume fits a specific job posting.

Rules:
- Be honest: a weak fit gets a low score. Inflated scores help nobody.
- Ground every claim in the actual documents. Never invent experience
  that is not in the resume.
- Resume suggestions must be specific and actionable, not generic advice.
- Interview questions should mix technical (based on the job's stack) and
  behavioral, and reflect what THIS employer would plausibly ask.
- The cover letter uses only real facts from the resume, in a confident,
  concise voice. No filler phrases.
- The study plan orders topics by interview impact: what to learn first."""


def analyze(resume_text: str, job_description: str) -> AnalysisResult:
    response = client.messages.parse(
        model="claude-opus-5",
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"<resume>\n{resume_text}\n</resume>\n\n"
                    f"<job_description>\n{job_description}"
                    f"\n</job_description>\n\n"
                    "Analyze this resume against this job description."
                ),
            }
        ],
        output_format=AnalysisResult,
    )

    usage = response.usage
    print(f"tokens: in={usage.input_tokens} out={usage.output_tokens}")

    return response.parsed_output