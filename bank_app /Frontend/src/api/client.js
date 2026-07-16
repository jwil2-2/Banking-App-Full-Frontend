const API_BASE = import.meta.env.VITE_API_URL

/**
 * Shared JSON fetch helper.
 * TODO(auth): when JWT/OAuth lands, read the token from session and send
 * `Authorization: Bearer <token>` here so every call is covered in one place.
 */
export async function requestJson(path, options = {}) {
  if (!API_BASE) {
    throw new Error('Missing VITE_API_URL in the shared .env file')
  }

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers ?? {}),
  }

  // TODO(auth): const token = getAccessToken(); if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })

  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    const detail = payload.detail
    const message = typeof detail === 'string' ? detail : detail ? JSON.stringify(detail) : 'Request failed'
    throw new Error(message)
  }

  return payload
}

export function getApiBase() {
  return API_BASE
}
