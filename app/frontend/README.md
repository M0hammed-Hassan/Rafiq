# Rafiq — Frontend

A complete React app (Vite) for the Rafiq assistant. Talks to your existing
backend with no changes required:

- `POST {API_BASE}/ask` — body `{ question, document_id }` → `{ answer, usage:{total_tokens}, latency_ms, finish_reason, sources, mode, needs_upload }`
- `POST {API_BASE}/upload` — multipart `file` → `{ document_id, filename, chunk_count }`

## Run it

```bash
npm install
npm run dev
```

Opens on `http://localhost:5173`. By default it calls your backend at
`http://localhost:8000/api`.

## Build for production

```bash
npm run build
npm run preview
```

## Structure

```
src/
  api.js                  backend calls (ask + upload)
  App.jsx                 app state: conversations, active doc, sending/uploading
  index.css               design system (colors, type, layout)
  components/
    Mark.jsx              animated brand mark
    Sidebar.jsx           conversation history + new chat
    ChatThread.jsx        message stream + empty state + suggestions
    Composer.jsx          input box, upload button, drag & drop
    ContextPanel.jsx      active document, session stats, mode legend
    StreamingText.jsx     word-reveal + count-up animation helpers
```

Conversations persist to `localStorage` per browser, so refreshing keeps
history. Clear it by wiping site data or deleting the `rafiq.conversations.v1` key.
