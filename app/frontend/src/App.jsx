import React, { useEffect, useMemo, useState } from 'react'
import Sidebar from './components/Sidebar.jsx'
import ChatThread from './components/ChatThread.jsx'
import Composer from './components/Composer.jsx'
import ContextPanel from './components/ContextPanel.jsx'
import Wordmark from './components/Wordmark.jsx'
import { askQuestion, uploadDocument } from './api.js'

const STORAGE_KEY = 'rafiq.conversations.v1'

function loadConversations() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    return JSON.parse(raw)
  } catch {
    return []
  }
}

function saveConversations(convs) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(convs))
  } catch {
    // storage unavailable — fail silently, app still works in-memory
  }
}

function makeConversation() {
  return { id: crypto.randomUUID(), title: 'New conversation', messages: [], doc: null }
}

export default function App() {
  const [conversations, setConversations] = useState(() => {
    const stored = loadConversations()
    return stored.length ? stored : [makeConversation()]
  })
  const [activeId, setActiveId] = useState(() => conversations[0].id)
  const [thinking, setThinking] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [contextOpen, setContextOpen] = useState(false)

  useEffect(() => saveConversations(conversations), [conversations])

  const active = useMemo(
    () => conversations.find((c) => c.id === activeId) || conversations[0],
    [conversations, activeId]
  )

  const updateActive = (fn) => {
    setConversations((cs) => cs.map((c) => (c.id === active.id ? fn(c) : c)))
  }

  const newConversation = () => {
    const c = makeConversation()
    setConversations((cs) => [c, ...cs])
    setActiveId(c.id)
    setError(null)
    setSidebarOpen(false)
  }

  const selectConversation = (id) => {
    setActiveId(id)
    setError(null)
    setSidebarOpen(false)
  }

  const send = async (question) => {
    setError(null)
    const userMsg = { id: crypto.randomUUID(), role: 'user', text: question }
    updateActive((c) => ({
      ...c,
      title: c.messages.length === 0 ? question.slice(0, 42) : c.title,
      messages: [...c.messages, userMsg],
    }))
    setThinking(true)

    try {
      const data = await askQuestion(question, active.doc ? active.doc.document_id : null)
      const assistantMsg = {
        id: crypto.randomUUID(),
        role: 'assistant',
        text: data.answer,
        mode: data.mode,
        sources: data.sources || [],
        needsUpload: data.needs_upload,
        tokens: data.usage ? data.usage.total_tokens : undefined,
        latency: data.latency_ms,
      }
      updateActive((c) => ({ ...c, messages: [...c.messages, assistantMsg] }))
    } catch (e) {
      const assistantMsg = { id: crypto.randomUUID(), role: 'assistant', text: e.message, mode: 'direct', sources: [] }
      updateActive((c) => ({ ...c, messages: [...c.messages, assistantMsg] }))
    } finally {
      setThinking(false)
    }
  }

  const upload = async (file) => {
    setError(null)
    setUploading(true)
    setUploadProgress(8)
    const tick = setInterval(() => setUploadProgress((p) => (p < 85 ? p + Math.random() * 10 : p)), 220)

    try {
      const data = await uploadDocument(file)
      setUploadProgress(100)
      setTimeout(() => {
        updateActive((c) => ({
          ...c,
          doc: { document_id: data.document_id, filename: data.filename, chunkCount: data.chunk_count },
        }))
        setUploadProgress(0)
      }, 250)
    } catch (e) {
      setError(e.message)
      setUploadProgress(0)
    } finally {
      clearInterval(tick)
      setUploading(false)
    }
  }

  const clearDoc = () => updateActive((c) => ({ ...c, doc: null }))

  const stats = useMemo(() => {
    const messageCount = active.messages.length
    const totalTokens = active.messages.reduce((sum, m) => sum + (m.tokens || 0), 0)
    return { messageCount, totalTokens }
  }, [active.messages])

  return (
    <div className="app-shell">
      <div className="ambient" aria-hidden="true">
        <span className="glow glow-a" />
        <span className="glow glow-b" />
      </div>

      <Sidebar
        conversations={conversations}
        activeId={active.id}
        onSelect={selectConversation}
        onNew={newConversation}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="main-column">
        <header className="topbar">
          <button className="icon-btn topbar-toggle" aria-label="Open menu" onClick={() => setSidebarOpen(true)}>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M2 4H14M2 8H14M2 12H14" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
            </svg>
          </button>
          <div className="topbar-title">
            <Wordmark size={14} /> <span className="topbar-title-sep">·</span> {active.title}
          </div>
          <button className="icon-btn topbar-toggle" aria-label="Open context panel" onClick={() => setContextOpen(true)}>
            ⓘ
          </button>
        </header>

        <ChatThread messages={active.messages} thinking={thinking} onSuggestion={send} />

        <Composer onSend={send} onUpload={upload} thinking={thinking} activeDocName={active.doc?.filename} />
      </div>

      <ContextPanel
        doc={active.doc}
        onClearDoc={clearDoc}
        uploading={uploading}
        uploadProgress={uploadProgress}
        error={error}
        stats={stats}
        open={contextOpen}
        onClose={() => setContextOpen(false)}
      />

      {(sidebarOpen || contextOpen) && (
        <div
          className="scrim"
          onClick={() => {
            setSidebarOpen(false)
            setContextOpen(false)
          }}
        />
      )}
    </div>
  )
}
