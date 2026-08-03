# Career Copilot

Career Copilot is a locally hosted web application that helps job seekers evaluate how well their resume matches a specific job posting. Users upload a resume in PDF format and paste a job description into the application. A FastAPI backend extracts the resume text and securely sends both inputs to Claude AI for analysis. The application then returns a structured evaluation including an overall match score, matching and missing skills, resume improvement suggestions, interview questions, a personalized cover letter draft, and a recommended study plan through a modern React dashboard.

## Demo

(Screenshot of the dashboard with real results — drag the image into the
GitHub editor, or commit it to a docs/ folder.)

## How it works

User uploads a PDF resume and pastes a job description -> React frontend packages both inputs using FormData -> FastAPI receives the request -> PyPDF extracts the resume text -> Claude AI compares the resume against the job posting -> Structured JSON response -> React renders an interactive dashboard displaying:

- Match Score
- Matching Skills
- Missing Skills
- Resume Suggestions 
- Interview Questions
- Cover Letter Draft
- Study Plan

## Stack

- Python 3.12
- FastAPI
- Pydantic
- Anthropic SDK (claude-opus-5)
- React 18
- Vite
-JavaScript
- HTML/CSS

## Running locally

### Clone the repository

```bash
git clone https://github.com/yourusername/CareerCopilot.git
cd CareerCopilot
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file inside the backend directory:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

Start the API:

```bash
uvicorn main:app --reload
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Visit:

```
http://localhost:5173
```

## Design decisions

- **Structured AI output:** The application uses Pydantic models with Claude's structured output instead of parsing free-form text. This guarantees consistent JSON that the frontend can safely display.

- **Input validation before API calls:** Resume type, extracted text quality, and job description length are validated before contacting the AI model to reduce unnecessary API usage and cost.

- **Separate frontend and backend:** React handles the user interface while FastAPI manages business logic and AI communication, creating a clean separation of responsibilities.

- **User-focused error handling:** Network failures, invalid PDFs, missing inputs, and oversized job descriptions return clear messages instead of exposing technical errors or stack traces.

## Roadmap

- Deploy the application to a public cloud platform
- Store previous resume analyses using SQLite or PostgreSQL
- Support multiple uploaded resumes for side-by-side comparisons
- Add Retrieval-Augmented Generation (RAG) for personalized resume recommendations
- Stream AI responses to display results as they are generated
- User authentication and saved analysis history