import { Link } from 'react-router-dom'
import { useAccounts } from '../accounts/useAccounts.js'
import { useAuth } from '../auth/useAuth.js'

function formatMoney(amount) {
  return `$${Number(amount).toFixed(2)}`
}

function OverviewPage() {
  const { user } = useAuth()
  const { accounts, selectedAccountId, selectAccount, totalBalance, isBusy } = useAccounts()

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="status-label">Overview</p>
          <h2>Hello, {user?.name}</h2>
          <p className="lede compact">Your accounts at a glance. Select one to use on Move Money and Details.</p>
        </div>
      </header>

      <div className="stat-row">
        <article className="stat-card">
          <span>Accounts</span>
          <strong>{accounts.length}</strong>
        </article>
        <article className="stat-card">
          <span>Total balance</span>
          <strong>{formatMoney(totalBalance)}</strong>
        </article>
        <article className="stat-card">
          <span>Selected</span>
          <strong>{selectedAccountId ? 'Ready' : 'None'}</strong>
        </article>
      </div>

      <div className="quick-links">
        <Link className="quick-link" to="/accounts/new">
          Open account
        </Link>
        <Link className="quick-link" to="/accounts/transfer">
          Move money
        </Link>
        <Link className="quick-link" to="/accounts/details">
          View details
        </Link>
      </div>

      <div className="account-list">
        <div className="account-list-header">
          <h3>My accounts</h3>
        </div>

        {accounts.length > 0 ? (
          <div className="account-cards">
            {accounts.map((account) => (
              <button
                key={account.id}
                type="button"
                className={account.id === selectedAccountId ? 'account-card active' : 'account-card'}
                onClick={() => selectAccount(account.id)}
                disabled={isBusy}
              >
                <strong>{account.account_type}</strong>
                <span>{account.id}</span>
                <span>Balance: {formatMoney(account.balance)}</span>
              </button>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            No accounts yet. <Link to="/accounts/new">Open a checking or savings account</Link> to get started.
          </div>
        )}
      </div>
    </section>
  )
}

export default OverviewPage
