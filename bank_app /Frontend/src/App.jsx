import { useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL

const emptySignup = {
  name: '',
  email: '',
  password: '',
  role: 'user',
}

const emptyLogin = {
  email: '',
  password: '',
}

function App() {
  const [signup, setSignup] = useState(emptySignup)
  const [login, setLogin] = useState(emptyLogin)
  const [activeTab, setActiveTab] = useState('signup')
  const [accountType, setAccountType] = useState('Checking')
  const [currentUser, setCurrentUser] = useState(null)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('neutral')
  const [isBusy, setIsBusy] = useState(false)

  const showMessage = (nextMessage, nextType = 'neutral') => {
    setMessage(nextMessage)
    setMessageType(nextType)
  }

  const requestJson = async (path, options) => {
    if (!API_BASE) {
      throw new Error('Missing VITE_API_URL in the shared .env file')
    }

    const response = await fetch(`${API_BASE}${path}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    })

    const payload = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(payload.detail ?? 'Request failed')
    }

    return payload
  }

  const handleSignupSubmit = async (event) => {
    event.preventDefault()
    setIsBusy(true)

    try {
      const user = await requestJson('/api/users', {
        method: 'POST',
        body: JSON.stringify(signup),
      })

      setCurrentUser(user)
      showMessage(`Created ${user.name}. You can log in or create an account next.`, 'success')
      setSignup(emptySignup)
      setActiveTab('login')
    } catch (error) {
      showMessage(error.message, 'error')
    } finally {
      setIsBusy(false)
    }
  }

  const handleLoginSubmit = async (event) => {
    event.preventDefault()
    setIsBusy(true)

    try {
      const user = await requestJson('/api/users/login', {
        method: 'POST',
        body: JSON.stringify(login),
      })

      setCurrentUser(user)
      showMessage(`Welcome back, ${user.name}.`, 'success')
      setLogin(emptyLogin)
    } catch (error) {
      showMessage(error.message, 'error')
    } finally {
      setIsBusy(false)
    }
  }

  const handleCreateAccount = async (event) => {
    event.preventDefault()
    if (!currentUser?.id) {
      showMessage('Create or log in to a user first.', 'error')
      return
    }

    setIsBusy(true)

    try {
      const account = await requestJson(`/api/accounts?user_id=${currentUser.id}`, {
        method: 'POST',
        body: JSON.stringify({ account_type: accountType }),
      })

      showMessage(
        `${account.account_type} account created for ${currentUser.name}.`,
        'success',
      )
    } catch (error) {
      showMessage(error.message, 'error')
    } finally {
      setIsBusy(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">Bank app starter</p>
          <h1>Simple user onboarding for your banking flow.</h1>
          <p className="lede">
            Create a user, sign in, and then open the door to account creation.
            This is the smallest useful frontend for building the rest of the app.
          </p>

          <div className="feature-row">
            <article>
              <span>1</span>
              <strong>Create a user</strong>
              <p>Store a name, email, password, and role.</p>
            </article>
            <article>
              <span>2</span>
              <strong>Log in</strong>
              <p>Confirm the credentials and load the active user.</p>
            </article>
            <article>
              <span>3</span>
              <strong>Open accounts</strong>
              <p>Use the returned user id to begin checking or savings accounts.</p>
            </article>
          </div>
        </div>

        <aside className="status-card">
          <p className="status-label">Connection</p>
          <h2>{currentUser ? currentUser.name : 'No active user'}</h2>
          <p className="status-text">
            Backend target: <code>{API_BASE}</code>
          </p>
          <div className="status-grid">
            <div>
              <span>Mode</span>
              <strong>{activeTab}</strong>
            </div>
            <div>
              <span>Role</span>
              <strong>{currentUser?.role ?? 'guest'}</strong>
            </div>
          </div>
        </aside>
      </section>

      <section className="forms-grid">
        <div className="panel">
          <div className="tab-row" role="tablist" aria-label="Authentication modes">
            <button
              type="button"
              className={activeTab === 'signup' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('signup')}
            >
              Create user
            </button>
            <button
              type="button"
              className={activeTab === 'login' ? 'tab active' : 'tab'}
              onClick={() => setActiveTab('login')}
            >
              Log in
            </button>
          </div>

          {activeTab === 'signup' ? (
            <form className="auth-form" onSubmit={handleSignupSubmit}>
              <label>
                Full name
                <input
                  type="text"
                  value={signup.name}
                  onChange={(event) => setSignup({ ...signup, name: event.target.value })}
                  placeholder="Jordan Lee"
                  required
                />
              </label>

              <label>
                Email
                <input
                  type="email"
                  value={signup.email}
                  onChange={(event) => setSignup({ ...signup, email: event.target.value })}
                  placeholder="jordan@example.com"
                  required
                />
              </label>

              <label>
                Password
                <input
                  type="password"
                  value={signup.password}
                  onChange={(event) => setSignup({ ...signup, password: event.target.value })}
                  placeholder="Strong password"
                  required
                />
              </label>

              <label>
                Role
                <select
                  value={signup.role}
                  onChange={(event) => setSignup({ ...signup, role: event.target.value })}
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </label>

              <button type="submit" disabled={isBusy}>
                {isBusy ? 'Working...' : 'Create user'}
              </button>
            </form>
          ) : (
            <form className="auth-form" onSubmit={handleLoginSubmit}>
              <label>
                Email
                <input
                  type="email"
                  value={login.email}
                  onChange={(event) => setLogin({ ...login, email: event.target.value })}
                  placeholder="jordan@example.com"
                  required
                />
              </label>

              <label>
                Password
                <input
                  type="password"
                  value={login.password}
                  onChange={(event) => setLogin({ ...login, password: event.target.value })}
                  placeholder="Your password"
                  required
                />
              </label>

              <button type="submit" disabled={isBusy}>
                {isBusy ? 'Working...' : 'Log in'}
              </button>
            </form>
          )}
        </div>

        <div className="panel accent-panel">
          <div>
            <p className="status-label">Next step</p>
            <h2>Begin account creation</h2>
            <p className="lede compact">
              Once a user exists, this section can create the first bank account by
              sending the returned user id to the backend.
            </p>
          </div>

          <form className="auth-form" onSubmit={handleCreateAccount}>
            <label>
              Account type
              <select value={accountType} onChange={(event) => setAccountType(event.target.value)}>
                <option value="Checking">Checking</option>
                <option value="Savings">Savings</option>
              </select>
            </label>

            <button type="submit" disabled={isBusy || !currentUser}>
              Create account
            </button>
          </form>

          {currentUser ? (
            <div className="user-chip">
              <strong>{currentUser.name}</strong>
              <span>{currentUser.email}</span>
              <span>ID: {currentUser.id}</span>
            </div>
          ) : (
            <div className="empty-state">
              Log in first to unlock account creation.
            </div>
          )}
        </div>
      </section>

      {message ? (
        <section className={messageType === 'error' ? 'message error' : 'message success'}>
          {message}
        </section>
      ) : null}
    </main>
  )
}

export default App
