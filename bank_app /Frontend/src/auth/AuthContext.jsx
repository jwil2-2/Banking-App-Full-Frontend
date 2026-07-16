import { useCallback, useMemo, useState } from 'react'
import { clearUser, getUser, setUser as persistUser } from './session.js'
import { requestJson } from '../api/client.js'
import { AuthContext } from './auth-context.js'

export function AuthProvider({ children }) {
  const [user, setUserState] = useState(() => getUser())
  const [isBusy, setIsBusy] = useState(false)

  const login = useCallback(async (email, password) => {
    setIsBusy(true)
    try {
      const nextUser = await requestJson('/api/users/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      // TODO(auth): persist tokens from the login response instead of (or in addition to) the user.
      persistUser(nextUser)
      setUserState(nextUser)
      return nextUser
    } finally {
      setIsBusy(false)
    }
  }, [])

  const signup = useCallback(async ({ name, email, password, role }) => {
    setIsBusy(true)
    try {
      const nextUser = await requestJson('/api/users', {
        method: 'POST',
        body: JSON.stringify({ name, email, password, role }),
      })
      persistUser(nextUser)
      setUserState(nextUser)
      return nextUser
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
      isAuthenticated: Boolean(user?.id),
      isBusy,
      login,
      signup,
      logout,
    }),
    [user, isBusy, login, signup, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
