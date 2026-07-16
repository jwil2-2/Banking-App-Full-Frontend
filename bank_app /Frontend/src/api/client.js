import { getAccessToken } from '../auth/session.js'

const API_BASE = import.meta.env.VITE_API_URL

export async function requestJson(path, options = {}) {
  if (!API_BASE) {
    throw new Error('Missing VITE_API_URL in the shared .env file')
  }

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers ?? {}),
  }

  const token = getAccessToken()
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })

  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    const detail = payload.detail
    const message = typeof detail === 'string' ? detail : detail ? JSON.stringify(detail) : 'Request failed'
    const error = new Error(message)
    error.status = response.status
    throw error
  }

  return payload
}

export function getApiBase() {
  return API_BASE
}
