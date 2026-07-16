import { useEffect, useState } from 'react'
import { requestJson } from '../api/client.js'
import { useAuth } from '../auth/useAuth.js'

const emptyAdminCreate = {
  name: '',
  email: '',
  password: '',
  role: 'user',
}

function AdminUsersPage() {
  const { user } = useAuth()
  const [users, setUsers] = useState([])
  const [form, setForm] = useState(emptyAdminCreate)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('neutral')
  const [isBusy, setIsBusy] = useState(false)

  const loadUsers = async () => {
    const list = await requestJson('/api/users')
    setUsers(list)
  }

  useEffect(() => {
    let cancelled = false

    ;(async () => {
      try {
        const list = await requestJson('/api/users')
        if (!cancelled) {
          setUsers(list)
        }
      } catch (error) {
        if (!cancelled) {
          setMessage(error.message)
          setMessageType('error')
        }
      }
    })()

    return () => {
      cancelled = true
    }
  }, [])

  const handleCreateUser = async (event) => {
    event.preventDefault()
    setIsBusy(true)
    try {
      await requestJson('/api/users/admin', {
        method: 'POST',
        body: JSON.stringify(form),
      })
      setForm(emptyAdminCreate)
      await loadUsers()
      setMessage('User created.')
      setMessageType('success')
    } catch (error) {
      setMessage(error.message)
      setMessageType('error')
    } finally {
      setIsBusy(false)
    }
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="status-label">Admin</p>
          <h2>User management</h2>
          <p className="lede compact">Signed in as {user?.name}. View all users and create accounts with specific roles.</p>
        </div>
      </header>

      {message ? (
        <div className={messageType === 'error' ? 'message error' : 'message success'}>{message}</div>
      ) : null}

      <form className="auth-form page-form" onSubmit={handleCreateUser}>
        <label>
          Full name
          <input
            type="text"
            value={form.name}
            onChange={(event) => setForm({ ...form, name: event.target.value })}
            required
          />
        </label>
        <label>
          Email
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
            required
          />
        </label>
        <label>
          Role
          <select value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </label>
        <button type="submit" disabled={isBusy}>
          {isBusy ? 'Creating...' : 'Create user'}
        </button>
      </form>

      <div className="admin-user-list">
        <div className="account-list-header">
          <h3>All users ({users.length})</h3>
          <button type="button" className="ghost-button" onClick={() => loadUsers()} disabled={isBusy}>
            Refresh
          </button>
        </div>

        {users.length ? (
          <div className="transaction-list">
            {users.map((entry) => (
              <article key={entry.id} className="transaction-item">
                <strong>{entry.name}</strong>
                <span>{entry.email}</span>
                <small>
                  {entry.role} · {entry.id}
                </small>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">No users found.</div>
        )}
      </div>
    </section>
  )
}

export default AdminUsersPage
