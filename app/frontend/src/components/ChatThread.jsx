import React, { useEffect, useRef } from 'react'
import Wordmark from './Wordmark.jsx'
import { StreamingText, CountUp } from './StreamingText.jsx'

const MODE_LABEL = { direct: 'direct', retrieved: 'company kb', strict_document: 'uploaded doc' }

const SUGGESTIONS = [
  { q: 'Explain what an API is in simple terms.', mode: 'direct' },
  { q: "What's our annual leave policy?", mode: 'retrieved' },
  { q: 'Can I expense alcohol with a client dinner?', mode: 'retrieved' },
]

function Meta({ mode, tokens, latency, sources }) {
  return (
    <div className="meta-row">
      <span className={'mode-pill mode-' + mode}>{MODE_LABEL[mode] || mode}</span>
      <span>
        <CountUp to={tokens} /> tokens
      </span>
      <span>
        <CountUp to={latency} suffix="ms" />
      </span>
      <span>
        sources: <b>{sources && sources.length ? sources.join(', ') : 'none'}</b>
      </span>
    </div>
  )
}

export default function ChatThread({ messages, thinking, onSuggestion }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current && endRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, thinking])

  if (messages.length === 0) {
    return (
      <div className="thread">
        <div className="empty-state">
          <Wordmark size={62} />
          <div className="empty-tagline">رفيق العمل الذكي</div>
          <p>
            Ask anything — Rafiq decides on its own whether to answer directly, search company documents, or ask
            you to upload one. Upload a file from the context panel to make it answer from that document only.
          </p>
          <div className="suggestion-list">
            {SUGGESTIONS.map((s, i) => (
              <button className="suggestion" key={i} onClick={() => onSuggestion(s.q)}>
                <span className={'mode-pill mode-' + s.mode}>{MODE_LABEL[s.mode]}</span>
                {s.q}
              </button>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="thread">
      {messages.map((m) =>
        m.role === 'user' ? (
          <div className="entry entry-user" key={m.id}>
            <div className="entry-label">You</div>
            <div className="entry-body user-body">{m.text}</div>
          </div>
        ) : (
          <div className="entry entry-assistant" key={m.id}>
            <div className="entry-label">
              <Wordmark size={11} />
            </div>
            <div className={'entry-body assistant-body' + (m.needsUpload ? ' assistant-body-flag' : '')}>
              <StreamingText text={m.text} />
            </div>
            {m.mode && <Meta mode={m.mode} tokens={m.tokens} latency={m.latency} sources={m.sources} />}
          </div>
        )
      )}

      {thinking && (
        <div className="entry entry-assistant">
          <div className="entry-label">
            <Wordmark size={11} thinking />
          </div>
          <div className="thinking-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      <div ref={endRef} />
    </div>
  )
}
