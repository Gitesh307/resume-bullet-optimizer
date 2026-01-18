import { useMemo, useState } from "react";
import { optimizeBullet } from "./api";
import "./index.css";

export default function App() {
  const [bullet, setBullet] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const canSubmit = useMemo(() => {
    return bullet.trim().length >= 10 && jobDescription.trim().length >= 30;
  }, [bullet, jobDescription]);

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const data = await optimizeBullet({
        bullet: bullet.trim(),
        job_description: jobDescription.trim(),
      });
      setResult(data);
    } catch (err) {
      setError(err.message || "Something failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="card">
        <h1>AI Resume Bullet Optimizer</h1>
        <p className="sub">
          Uses spaCy + TF-IDF + cosine similarity + keyword gap to rewrite your bullet.
        </p>

        <form onSubmit={onSubmit} className="form">
          <label>
            Resume bullet
            <textarea
              value={bullet}
              onChange={(e) => setBullet(e.target.value)}
              placeholder="Example: Built REST APIs to validate healthcare claims data..."
              rows={3}
            />
          </label>

          <label>
            Job description
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste job description here..."
              rows={8}
            />
          </label>

          <button disabled={!canSubmit || loading}>
            {loading ? "Optimizing..." : "Optimize Bullet"}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {result && (
          <div className="results">
            <h2>Optimized bullet</h2>
            <div className="output">{result.optimized_bullet}</div>

            <div className="grid">
              <div className="box">
                <h3>Similarity</h3>
                <div className="big">{(result.similarity * 100).toFixed(1)}%</div>
              </div>

              <div className="box">
                <h3>Matched keywords</h3>
                <ul>
                  {result.matched_keywords.length ? (
                    result.matched_keywords.map((k) => <li key={k}>{k}</li>)
                  ) : (
                    <li>None yet</li>
                  )}
                </ul>
              </div>

              <div className="box">
                <h3>Missing keywords</h3>
                <ul>
                  {result.missing_keywords.length ? (
                    result.missing_keywords.map((k) => <li key={k}>{k}</li>)
                  ) : (
                    <li>None — strong match</li>
                  )}
                </ul>
              </div>
            </div>

            <p className="note">
              Don’t keyword-stuff. Use the missing list to guide what you genuinely did.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
