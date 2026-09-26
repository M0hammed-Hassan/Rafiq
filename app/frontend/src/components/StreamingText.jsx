import React, { useEffect, useState } from 'react'

export function StreamingText({ text }) {
  const [shown, setShown] = useState('')

  useEffect(() => {
    let i = 0
    const step = Math.max(1, Math.round(text.length / 90))
    const id = setInterval(() => {
      i += step
      setShown(text.slice(0, i))
      if (i >= text.length) clearInterval(id)
    }, 14)
    return () => clearInterval(id)
  }, [text])

  const streaming = shown.length < text.length
  return (
    <span>
      {shown}
      {streaming && <span className="type-cursor" />}
    </span>
  )
}

export function CountUp({ to = 0, suffix = '' }) {
  const [n, setN] = useState(0)
  useEffect(() => {
    let start = null
    let raf
    const dur = 500
    function tick(ts) {
      if (start === null) start = ts
      const p = Math.min(1, (ts - start) / dur)
      setN(Math.round(to * (1 - Math.pow(1 - p, 3))))
      if (p < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [to])
  return (
    <b>
      {n}
      {suffix}
    </b>
  )
}
