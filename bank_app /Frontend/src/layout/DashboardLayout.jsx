import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth.js'
import { useAccounts } from '../accounts/useAccounts.js'
import StatusBanner from '../components/StatusBanner.jsx'

const navItems = [
  { to: '/overview', label: 'Overview' },
  { to: '/accounts/new', label: 'Open Account' },
  { to: '/accounts/transfer', label: 'Move Money' },
  { to: '/accounts/details', label: 'Account Details' },
]

function DashboardLayout() {
  const { user, logout } = useAuth()
  const { message, messageType } = useAccounts()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="dashboard-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <p className="eyebrow">Ledgerline</p>
          <h1>Banking</h1>
        </div>

        <nav className="sidebar-nav" aria-label="Dashboard">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-user">
          <div>
            <strong>{user?.name}</strong>
            <span>{user?.role ?? 'user'}</span>
          </div>
          <button type="button" className="ghost-button" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </aside>

      <div className="dashboard-main">
        <StatusBanner message={message} messageType={messageType} />
        <Outlet />
      </div>
    </div>
  )
}

export default DashboardLayout
