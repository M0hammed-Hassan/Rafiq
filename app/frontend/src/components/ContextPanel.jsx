import React from 'react'

export default function ContextPanel({ doc, onClearDoc, uploading, uploadProgress, error, stats, open, onClose }) {
  return (
    <aside className={'context-panel' + (open ? ' context-panel-open' : '')}>
      <div className="context-header">
        <span>Context</span>
        <button className="icon-btn context-close" aria-label="Close panel" onClick={onClose}>
          ✕
        </button>
      </div>

      {error && <div className="context-error">{error}</div>}

      <div className="context-block">
        <div className="context-block-label">Active document</div>
        {doc ? (
          <div className="doc-card">
            <div className="doc-card-name">{doc.filename}</div>
            <div className="doc-card-sub">{doc.chunkCount} chunks indexed</div>
            <button className="doc-card-clear" onClick={onClearDoc}>
              Clear document
            </button>
          </div>
        ) : (
          <div className="doc-card doc-card-empty">None — Rafiq will decide direct vs. company kb on its own.</div>
        )}
        {uploading && (
          <div className="progress-track">
            <div className="progress-fill" style={{ width: uploadProgress + '%' }} />
          </div>
        )}
      </div>

      <div className="context-block">
        <div className="context-block-label">Session</div>
        <div className="stat-row">
          <span>Messages</span>
          <b>{stats.messageCount}</b>
        </div>
        <div className="stat-row">
          <span>Tokens used</span>
          <b>{stats.totalTokens}</b>
        </div>
      </div>

      <div className="context-block">
        <div className="context-block-label">Modes</div>
        <div className="legend-row">
          <span className="mode-pill mode-direct">direct</span> answered from general knowledge
        </div>
        <div className="legend-row">
          <span className="mode-pill mode-retrieved">company kb</span> pulled from indexed company docs
        </div>
        <div className="legend-row">
          <span className="mode-pill mode-strict_document">uploaded doc</span> answered only from your file
        </div>
      </div>
    </aside>
  )
}
