const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function optimizeBullet({ bullet, job_description }) {
  const res = await fetch(`${API_BASE}/api/optimize/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ bullet, job_description }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail || `Request failed (${res.status})`);
  }

  return res.json();
}
