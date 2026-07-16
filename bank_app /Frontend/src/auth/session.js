const USER_KEY = 'bank_app_user'
// TODO(auth): replace USER_KEY with access/refresh token keys when JWT arrives.

/**
 * Local session helpers. Today we store the user object from login/signup.
 * Later: store tokens only and fetch the user profile from a protected endpoint.
 */
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

export function clearUser() {
  localStorage.removeItem(USER_KEY)
  // TODO(auth): also clear access/refresh tokens here.
  try {
    sessionStorage.removeItem('bank_app_selected_account')
  } catch {
    // ignore
  }
}

export function getAccessToken() {
  // TODO(auth): return localStorage.getItem('bank_app_access_token')
  return null
}
