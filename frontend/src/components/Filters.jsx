import React from 'react'

export default function Filters({type, setType, source, setSource, search, setSearch, onRefresh}) {
  return (
    <div className="card">
      <h2>Filters</h2>
      <div className="row">
        <select value={type} onChange={e=>setType(e.target.value)}>
          <option value="">All types</option>
          <option value="ip">IP</option>
          <option value="domain">Domain</option>
          <option value="hash">Hash</option>
          <option value="url">URL</option>
        </select>
        <input className="input" placeholder="Filter by source name…" value={source} onChange={e=>setSource(e.target.value)} />
        <input className="input" placeholder="Search value contains…" value={search} onChange={e=>setSearch(e.target.value)} />
        <button className="input" onClick={onRefresh}>Refresh</button>
      </div>
    </div>
  )
}
