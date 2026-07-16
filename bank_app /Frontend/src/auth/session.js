const USER_KEY = 'bank_app_user'
const ACCESS_TOKEN_KEY = 'bank_app_access_token'

export function getUser() {
  try {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function setUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function setAccessToken(token) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token)
}

export function setSession({ user, accessToken }) {
  setUser(user)
  setAccessToken(accessToken)
}

export function clearUser() {
  localStorage.removeItem(USER_KEY)
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  try {
    sessionStorage.removeItem('bank_app_selected_account')
  } catch {
    // ignore
  }
}

export function isAuthenticated() {
  return Boolean(getAccessToken() && getUser()?.id)
}
