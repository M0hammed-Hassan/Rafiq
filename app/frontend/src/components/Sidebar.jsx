import React from 'react'
import Wordmark from './Wordmark.jsx'

export default function Sidebar({ conversations, activeId, onSelect, onNew, open, onClose }) {
  return (
    <aside className={'sidebar' + (open ? ' sidebar-open' : '')}>
      <div className="sidebar-header">
        <div className="brand">
          <div className="brand-text">
            <Wordmark size={21} />
            <div className="brand-tagline">رفيق العمل</div>
          </div>
        </div>
        <button className="icon-btn sidebar-close" aria-label="Close menu" onClick={onClose}>
          ✕
        </button>
      </div>

      <button className="new-chat-btn" onClick={onNew}>
        <span>+</span> New conversation
      </button>

      <div className="conv-list">
        <div className="conv-list-label">History</div>
        {conversations.length === 0 && <div className="conv-empty">No conversations yet</div>}
        {conversations.map((c) => (
          <div
            key={c.id}
            className={'conv-item' + (c.id === activeId ? ' conv-item-active' : '')}
            onClick={() => onSelect(c.id)}
          >
            <div className="conv-title">{c.title}</div>
            <div className="conv-sub">{c.messages.length} messages</div>
          </div>
        ))}
      </div>

      <div className="sidebar-footer">
        <span className="pulse-dot" /> connected
      </div>
    </aside>
  )
}
