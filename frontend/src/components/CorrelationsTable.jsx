import React from 'react'

export default function CorrelationsTable({ data = [] }) {
  return (
    <div className="card">
      <h2>Correlations</h2>
      <table className="table">
        <thead>
          <tr>
            <th>IOC 1</th>
            <th>IOC 2</th>
            <th>Match</th>
            <th>Confidence</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.id}>
              <td style={{maxWidth:320, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>{row.ioc1?.value}</td>
              <td style={{maxWidth:320, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>{row.ioc2?.value}</td>
              <td><span className="badge">{row.match_type}</span></td>
              <td><span className="tag">{(row.confidence ?? 0).toFixed(2)}</span></td>
              <td className="kbd">{row.created_at ? new Date(row.created_at).toLocaleString() : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
