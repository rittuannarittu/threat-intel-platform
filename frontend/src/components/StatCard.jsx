import React from 'react'

export default function StatCard({label, value, hint}) {
  return (
    <div className="card">
      <div style={{fontSize:12, color:'#8aa0c6', marginBottom:6}}>{label}</div>
      <div style={{fontSize:26, fontWeight:700}}>{value ?? '—'}</div>
      {hint && <div className="kbd" style={{marginTop:6}}>{hint}</div>}
    </div>
  )
}
