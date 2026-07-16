import { Link } from 'react-router-dom'
import { useAccounts } from '../accounts/useAccounts.js'

function formatMoney(amount) {
  return `$${Number(amount).toFixed(2)}`
}

function AccountDetailsPage() {
  const {
    accounts,
    selectedAccountId,
    selectedAccount,
    selectAccount,
    refreshAccount,
    isBusy,
  } = useAccounts()

  if (!accounts.length) {
    return (
      <section className="page">
        <header className="page-header">
          <div>
            <p className="status-label">Account details</p>
            <h2>Balance and history</h2>
          </div>
        </header>
        <div className="empty-state">
          No accounts yet. <Link to="/accounts/new">Open an account</Link> to see details.
        </div>
      </section>
    )
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="status-label">Account details</p>
          <h2>Balance and history</h2>
          <p className="lede compact">Inspect the selected account and its transaction history.</p>
        </div>
        <button type="button" className="ghost-button" onClick={refreshAccount} disabled={isBusy}>
          Refresh
        </button>
      </header>

      <label className="inline-select">
        Account
        <select
          value={selectedAccountId}
          onChange={(event) => selectAccount(event.target.value)}
          disabled={isBusy}
        >
          {accounts.map((account) => (
            <option key={account.id} value={account.id}>
              {account.account_type} — {formatMoney(account.balance)}
            </option>
          ))}
        </select>
      </label>

      {selectedAccount ? (
        <div className="account-detail">
          <div className="user-chip">
            <strong>{selectedAccount.account_type}</strong>
            <span>Account ID: {selectedAccount.id}</span>
            <span>User ID: {selectedAccount.user_id}</span>
            <span>Balance: {formatMoney(selectedAccount.balance)}</span>
          </div>

          <div className="transaction-history">
            <div className="account-list-header">
              <h3>Transaction history</h3>
            </div>

            {selectedAccount.transactions?.length ? (
              <div className="transaction-list">
                {selectedAccount.transactions.map((transaction, index) => (
                  <article key={`${transaction.type}-${transaction.created_at}-${index}`} className="transaction-item">
                    <strong>{transaction.type}</strong>
                    <span>{formatMoney(transaction.amount)}</span>
                    <small>{transaction.created_at ?? 'Pending timestamp'}</small>
                  </article>
                ))}
              </div>
            ) : (
              <div className="empty-state">No transactions yet.</div>
            )}
          </div>
        </div>
      ) : (
        <div className="empty-state">Select an account to view details.</div>
      )}
    </section>
  )
}

export default AccountDetailsPage
