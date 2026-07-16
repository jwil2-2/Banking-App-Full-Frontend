import { Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext.jsx'
import { useAuth } from './auth/useAuth.js'
import { AccountProvider } from './accounts/AccountContext.jsx'
import { ProtectedRoute, PublicOnlyRoute } from './auth/RouteGuards.jsx'
import DashboardLayout from './layout/DashboardLayout.jsx'
import AuthPage from './pages/AuthPage.jsx'
import OverviewPage from './pages/OverviewPage.jsx'
import OpenAccountPage from './pages/OpenAccountPage.jsx'
import MoveMoneyPage from './pages/MoveMoneyPage.jsx'
import AccountDetailsPage from './pages/AccountDetailsPage.jsx'
import './App.css'

function RootRedirect() {
  const { isAuthenticated } = useAuth()
  return <Navigate to={isAuthenticated ? '/overview' : '/login'} replace />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<RootRedirect />} />

      <Route element={<PublicOnlyRoute />}>
        <Route path="/login" element={<AuthPage />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route
          element={
            <AccountProvider>
              <DashboardLayout />
            </AccountProvider>
          }
        >
          <Route path="/overview" element={<OverviewPage />} />
          <Route path="/accounts/new" element={<OpenAccountPage />} />
          <Route path="/accounts/transfer" element={<MoveMoneyPage />} />
          <Route path="/accounts/details" element={<AccountDetailsPage />} />
        </Route>
      </Route>

      <Route path="*" element={<RootRedirect />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App
