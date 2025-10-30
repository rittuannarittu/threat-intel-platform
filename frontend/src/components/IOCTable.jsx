import React from 'react'

export default function IOCTable({ data = [] }) {
  return (
    <div className="card">
      <h2>Latest IOCs</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Value</th>
            <th>Source</th>
            <th>Confidence</th>
            <th>Last Seen</th>
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.id}>
              <td><span className="badge">{row.ioc_type}</span></td>
              <td style={{maxWidth:420, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>{row.value}</td>
              <td>{row.source?.name || <span className="kbd">—</span>}</td>
              <td><span className="tag">{(row.confidence ?? 0).toFixed(2)}</span></td>
              <td className="kbd">{row.last_seen ? new Date(row.last_seen).toLocaleString() : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
