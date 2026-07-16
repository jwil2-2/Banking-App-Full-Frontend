import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/useAuth.js'

export function ProtectedRoute() {
  const { isAuthenticated, isInitializing } = useAuth()
  const location = useLocation()

  if (isInitializing) {
    return <div className="loading-state">Restoring session...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  return <Outlet />
}

export function PublicOnlyRoute() {
  const { isAuthenticated, isInitializing } = useAuth()

  if (isInitializing) {
    return <div className="loading-state">Loading...</div>
  }

  if (isAuthenticated) {
    return <Navigate to="/overview" replace />
  }

  return <Outlet />
}

export function AdminRoute() {
  const { isAuthenticated, isAdmin, isInitializing } = useAuth()
  const location = useLocation()

  if (isInitializing) {
    return <div className="loading-state">Restoring session...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (!isAdmin) {
    return <Navigate to="/overview" replace />
  }

  return <Outlet />
}
