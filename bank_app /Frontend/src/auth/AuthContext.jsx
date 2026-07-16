import { useCallback, useEffect, useMemo, useState } from 'react'
import { clearUser, getAccessToken, getUser, setSession } from './session.js'
import { requestJson } from '../api/client.js'
import { AuthContext } from './auth-context.js'

export function AuthProvider({ children }) {
  const [user, setUserState] = useState(() => getUser())
  const [isInitializing, setIsInitializing] = useState(() => Boolean(getAccessToken()))
  const [isBusy, setIsBusy] = useState(false)

  useEffect(() => {
    const token = getAccessToken()
    if (!token) {
      return
    }

    let cancelled = false

    ;(async () => {
      try {
        const profile = await requestJson('/api/users/me')
        if (!cancelled) {
          setUserState(profile)
          setSession({ user: profile, accessToken: token })
        }
      } catch {
        if (!cancelled) {
          clearUser()
          setUserState(null)
        }
      } finally {
        if (!cancelled) {
          setIsInitializing(false)
        }
      }
    })()

    return () => {
      cancelled = true
    }
  }, [])

  const login = useCallback(async (email, password) => {
    setIsBusy(true)
    try {
      const response = await requestJson('/api/users/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      setSession({ user: response.user, accessToken: response.access_token })
      setUserState(response.user)
      return response.user
    } finally {
      setIsBusy(false)
    }
  }, [])

  const signup = useCallback(async ({ name, email, password }) => {
    setIsBusy(true)
    try {
      const response = await requestJson('/api/users', {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      })
      setSession({ user: response.user, accessToken: response.access_token })
      setUserState(response.user)
      return response.user
    } finally {
      setIsBusy(false)
    }
  }, [])

  const logout = useCallback(() => {
    clearUser()
    setUserState(null)
  }, [])

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(getAccessToken() && user?.id),
      isInitializing,
      isBusy,
      isAdmin: user?.role === 'admin',
      login,
      signup,
      logout,
    }),
    [user, isInitializing, isBusy, login, signup, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
