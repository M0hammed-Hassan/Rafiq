import React, { useRef, useState } from 'react'

export default function Composer({ onSend, onUpload, thinking, activeDocName }) {
  const [value, setValue] = useState('')
  const [dragOver, setDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const submit = () => {
    const v = value.trim()
    if (!v || thinking) return
    onSend(v)
    setValue('')
  }

  return (
    <div
      className={'composer-shell' + (dragOver ? ' composer-dragover' : '')}
      onDragOver={(e) => {
        e.preventDefault()
        setDragOver(true)
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDragOver(false)
        if (e.dataTransfer.files && e.dataTransfer.files[0]) onUpload(e.dataTransfer.files[0])
      }}
    >
      <form
        onSubmit={(e) => {
          e.preventDefault()
          submit()
        }}
      >
        <button
          type="button"
          className="icon-btn"
          aria-label="Upload document"
          onClick={() => fileInputRef.current.click()}
        >
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
            <path
              d="M8 2V11M8 2L4.5 5.5M8 2L11.5 5.5M3 11.5V13.5H13V11.5"
              stroke="currentColor"
              strokeWidth="1.4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
        <input
          type="file"
          ref={fileInputRef}
          accept=".pdf,.txt,.md"
          style={{ display: 'none' }}
          onChange={(e) => {
            if (e.target.files[0]) onUpload(e.target.files[0])
            e.target.value = ''
          }}
        />
        <textarea
          value={value}
          placeholder="Message Rafiq..."
          rows={1}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              submit()
            }
          }}
        />
        <button type="submit" className="send-btn" disabled={!value.trim() || thinking} aria-label="Send">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
            <path
              d="M14 2L2 7.5L7.5 9M14 2L9.5 14L7.5 9M14 2L7.5 9"
              stroke="#faf8f4"
              strokeWidth="1.4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </form>
      <div className="composer-hint">
        {activeDocName
          ? `Strict mode — Rafiq answers only from ${activeDocName}`
          : 'Rafiq decides on its own whether to answer directly or search company documents. Drop a file here to index it.'}
      </div>
    </div>
  )
}
