import React from 'react'

export default function Header() {
  return (
    <div className="card" style={{
      display:'flex', alignItems:'center', justifyContent:'space-between'
    }}>
      <div>
        <h1>Threat Intelligence Dashboard</h1>
        <div className="kbd">Connected to Django API via Vite proxy</div>
      </div>
      <img src="https://upload.wikimedia.org/wikipedia/commons/3/38/OOjs_UI_icon_eye.svg"
           alt="" width="36" height="36" style={{opacity:.6}}/>
    </div>
  )
}
