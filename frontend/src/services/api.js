import axios from 'axios'

const api = axios.create({
  // vite proxy sends /api → 127.0.0.1:8000
  baseURL: '/api'
})

export async function listSources() {
  const { data } = await api.get('/ioc/sources/')
  return data
}

export async function listIocs(params = {}) {
  const { data } = await api.get('/ioc/iocs/', { params })
  return data
}

export async function listCorrelations() {
  const { data } = await api.get('/ioc/correlations/')
  return data
}

// Utility: trigger server-side correlation pass
export async function correlateNow() {
  const { data } = await api.post('/ioc/correlate/')
  return data
}
