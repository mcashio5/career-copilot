from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    """Everything the dashboard displays, in one validated shape."""

    match_score: int = Field(description="0-100 fit between resume and job")
    match_summary: str = Field(
        description="Two-sentence explanation of the score"
    )
    matching_skills: list[str] = Field(
        description="Skills present in BOTH resume and job posting"
    )
    missing_skills: list[str] = Field(
        description="Skills the job wants that the resume lacks"
    )
    resume_suggestions: list[str] = Field(
        description="Specific, actionable resume improvements"
    )
    interview_questions: list[str] = Field(
        description="8-10 questions this employer would likely ask"
    )
    cover_letter: str = Field(
        description="A complete first-draft cover letter"
    )
    study_plan: list[str] = Field(
        description="Ordered topics to study, based on the gaps"
    )