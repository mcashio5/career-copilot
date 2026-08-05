import { useEffect, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.PROD ? "" : "http://localhost:8000";

function App() {
  // analyze | history
  const [page, setPage] = useState("analyze");

  // Data entered into the job-description box
  const [jobDescription, setJobDescription] = useState("");

  // Shared password used to access the app
  const [accessKey, setAccessKey] = useState(
    localStorage.getItem("accessKey") || ""
  );

  // idle | loading | done | error
  const [status, setStatus] = useState("idle");

  // Stores the completed analysis returned by FastAPI
  const [result, setResult] = useState(null);

  // Stores an error message when something fails
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    // Prevent the browser from reloading the entire page
    e.preventDefault();

    const file = e.target.elements.resume.files[0];

    if (!file || !jobDescription.trim()) {
      setError("Please choose a PDF and paste a job description.");
      setStatus("error");
      return;
    }

    setStatus("loading");
    setError("");
    setResult(null);

    // Package the PDF and text together for FastAPI
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        headers: {
          "X-Access-Key": accessKey,
        },
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json();
        const detail = data.detail ?? "Analysis failed.";
        throw new Error(detail);
      }

      const data = await response.json();
      setResult(data);
      setStatus("done");
    } catch (err) {
      if (err instanceof TypeError) {
        setError("Can't reach the analysis server — is the backend running?");
      } else {
        setError(err.message || "Something went wrong during analysis.");
      }

      setStatus("error");
    }
  }

  if (page === "history") {
    return (
      <HistoryPage onBack={() => setPage("analyze")} accessKey={accessKey} />
    );
  }

  return (
    <main className="container">
      <h1>Career Copilot</h1>

      <p className="tagline">
        Upload a resume, paste a job posting, get a plan.
      </p>

      <button
        type="button"
        className="nav-button"
        onClick={() => setPage("history")}
      >
        History
      </button>

      <form onSubmit={handleSubmit}>
        <label>
          Resume (PDF)
          <input
            type="file"
            name="resume"
            accept="application/pdf"
          />
        </label>

        <label>
          Job description
          <textarea
            rows={10}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the full job posting here..."
          />
        </label>

        <label>
          Access key
          <input
            type="password"
            value={accessKey}
            onChange={(e) => {
              setAccessKey(e.target.value);
              localStorage.setItem("accessKey", e.target.value);
            }}
            placeholder="Ask Michael for the key"
          />
        </label>

        <button
          type="submit"
          disabled={status === "loading"}
        >
          {status === "loading"
            ? "Analyzing… (30–60s)"
            : "Analyze"}
        </button>
      </form>

      {status === "error" && (
        <p className="error">{error}</p>
      )}

      {status === "done" && result && (
        <Results data={result} />
      )}
    </main>
  );
}

function Results({ data }) {
  return (
    <section className="results">
      <h2>Analysis Results</h2>

      <h3>Job Title</h3>
      <p>{data.job_title}</p>

      <h3>Match Score</h3>
      <p>{data.match_score}/100</p>

      <h3>Summary</h3>
      <p>{data.match_summary}</p>

      <h3>Matching Skills</h3>
      <ul>
        {data.matching_skills?.map((skill) => (
          <li key={skill}>{skill}</li>
        ))}
      </ul>

      <h3>Missing Skills</h3>
      <ul>
        {data.missing_skills?.map((skill) => (
          <li key={skill}>{skill}</li>
        ))}
      </ul>

      <h3>Resume Suggestions</h3>
      <ul>
        {data.resume_suggestions?.map((suggestion) => (
          <li key={suggestion}>{suggestion}</li>
        ))}
      </ul>

      <h3>Interview Questions</h3>
      <ol>
        {data.interview_questions?.map((question) => (
          <li key={question}>{question}</li>
        ))}
      </ol>

      <h3>Cover Letter</h3>
      <p className="cover-letter">{data.cover_letter}</p>

      <h3>Study Plan</h3>
      <ol>
        {data.study_plan?.map((topic) => (
          <li key={topic}>{topic}</li>
        ))}
      </ol>
    </section>
  );
}

function HistoryPage({ onBack, accessKey }) {
  // loading | done | error
  const [status, setStatus] = useState("loading");
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await fetch(`${API_URL}/api/history`, {
          headers: { "X-Access-Key": accessKey },
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail ?? "Couldn't load history.");
        }

        setHistory(await response.json());
        setStatus("done");
      } catch (err) {
        setError(err.message || "Couldn't load history.");
        setStatus("error");
      }
    }

    loadHistory();
  }, [accessKey]);

  return (
    <main className="container">
      <h1>History</h1>

      <p className="tagline">Past analyses, most recent first.</p>

      <button type="button" className="nav-button" onClick={onBack}>
        Back to Analyzer
      </button>

      {status === "loading" && <p className="tagline">Loading…</p>}

      {status === "error" && <p className="error">{error}</p>}

      {status === "done" && history.length === 0 && (
        <p className="tagline">No analyses yet.</p>
      )}

      {status === "done" && history.length > 0 && (
        <section className="results">
          <table className="history-table">
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Date</th>
                <th>Match Score</th>
                <th>Top Matching Skill</th>
                <th>Top Missing Skill</th>
              </tr>
            </thead>
            <tbody>
              {history.map((entry) => (
                <tr key={entry.id}>
                  <td>{entry.job_title}</td>
                  <td>{new Date(entry.created_at).toLocaleDateString()}</td>
                  <td>{entry.match_score}/100</td>
                  <td>{entry.top_matching_skill}</td>
                  <td>{entry.top_missing_skill}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </main>
  );
}

export default App;