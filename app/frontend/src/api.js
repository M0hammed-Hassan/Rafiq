// Points at your existing backend. Override at build/run time with:
//   VITE_API_BASE=https://your-host/api npm run dev
export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

/**
 * POST {API_BASE}/ask
 * body: { question, document_id }
 * returns: { answer, usage:{total_tokens}, latency_ms, finish_reason, sources, mode, needs_upload }
 */
export async function askQuestion(question, documentId) {
  const res = await fetch(`${API_BASE}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, document_id: documentId || null }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Something went wrong. Please try again.')
  }
  return res.json()
}

/**
 * POST {API_BASE}/upload
 * multipart form field "file"
 * returns: { document_id, filename, chunk_count }
 */
export async function uploadDocument(file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Upload failed. Please try a different file.')
  }
  return res.json()
}
