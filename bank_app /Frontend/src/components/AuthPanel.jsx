function AuthPanel({
  activeTab,
  onTabChange,
  signup,
  onSignupChange,
  login,
  onLoginChange,
  onSignupSubmit,
  onLoginSubmit,
  isBusy,
}) {
  return (
    <section className="panel">
      <div className="tab-row" role="tablist" aria-label="Authentication modes">
        <button
          type="button"
          className={activeTab === 'login' ? 'tab active' : 'tab'}
          onClick={() => onTabChange('login')}
        >
          Log in
        </button>
        <button
          type="button"
          className={activeTab === 'signup' ? 'tab active' : 'tab'}
          onClick={() => onTabChange('signup')}
        >
          Create account
        </button>
      </div>

      {activeTab === 'login' ? (
        <form className="auth-form" onSubmit={onLoginSubmit}>
          <label>
            Email
            <input
              type="email"
              value={login.email}
              onChange={(event) => onLoginChange({ ...login, email: event.target.value })}
              placeholder="jordan@example.com"
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={login.password}
              onChange={(event) => onLoginChange({ ...login, password: event.target.value })}
              placeholder="Your password"
              required
            />
          </label>

          <button type="submit" disabled={isBusy}>
            {isBusy ? 'Working...' : 'Log in'}
          </button>
        </form>
      ) : (
        <form className="auth-form" onSubmit={onSignupSubmit}>
          <label>
            Full name
            <input
              type="text"
              value={signup.name}
              onChange={(event) => onSignupChange({ ...signup, name: event.target.value })}
              placeholder="Jordan Lee"
              required
            />
          </label>

          <label>
            Email
            <input
              type="email"
              value={signup.email}
              onChange={(event) => onSignupChange({ ...signup, email: event.target.value })}
              placeholder="jordan@example.com"
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={signup.password}
              onChange={(event) => onSignupChange({ ...signup, password: event.target.value })}
              placeholder="Strong password"
              required
            />
          </label>

          <details className="role-details">
            <summary>Advanced: account role</summary>
            <label>
              Role
              <select
                value={signup.role}
                onChange={(event) => onSignupChange({ ...signup, role: event.target.value })}
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </label>
          </details>

          <button type="submit" disabled={isBusy}>
            {isBusy ? 'Working...' : 'Create account'}
          </button>
        </form>
      )}
    </section>
  )
}

export default AuthPanel
