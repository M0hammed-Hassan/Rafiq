import React from 'react'

// Pure typographic brand — no icon. The word itself shines: a light sweeps
// across the letters and settles, faster and brighter while Rafiq thinks.
export default function Wordmark({ size = 20, thinking = false }) {
  return (
    <span
      className={'wordmark' + (thinking ? ' wordmark-thinking' : '')}
      style={{ fontSize: size }}
    >
      Rafiq
    </span>
  )
}
