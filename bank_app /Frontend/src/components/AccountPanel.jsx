function AccountPanel({
  currentUser,
  accounts,
  selectedAccountId,
  selectedAccount,
  accountType,
  onAccountTypeChange,
  depositAmount,
  onDepositAmountChange,
  withdrawAmount,
  onWithdrawAmountChange,
  onCreateAccount,
  onSelectAccount,
  onDeposit,
  onWithdraw,
  onRefreshAccount,
  isBusy,
}) {
  return (
    <section className="panel accent-panel">
      <div className="panel-stack">
        <div>
          <p className="status-label">Accounts</p>
          <h2>Begin account activity</h2>
          <p className="lede compact">
            Create the first account, then deposit, withdraw, and inspect the current balance and history.
          </p>
        </div>

        <form className="auth-form" onSubmit={onCreateAccount}>
          <label>
            Account type
            <select value={accountType} onChange={(event) => onAccountTypeChange(event.target.value)}>
              <option value="Checking">Checking</option>
              <option value="Savings">Savings</option>
            </select>
          </label>

          <button type="submit" disabled={isBusy || !currentUser}>
            Create account
          </button>
        </form>
      </div>

      <div className="account-shell">
        <div className="account-list">
          <div className="account-list-header">
            <h3>My accounts</h3>
            <button type="button" className="ghost-button" onClick={onRefreshAccount} disabled={!currentUser}>
              Refresh
            </button>
          </div>

          {accounts.length > 0 ? (
            <div className="account-cards">
              {accounts.map((account) => (
                <button
                  key={account.id}
                  type="button"
                  className={account.id === selectedAccountId ? 'account-card active' : 'account-card'}
                  onClick={() => onSelectAccount(account.id)}
                >
                  <strong>{account.account_type}</strong>
                  <span>{account.id}</span>
                  <span>Balance: ${Number(account.balance).toFixed(2)}</span>
                </button>
              ))}
            </div>
          ) : (
            <div className="empty-state">No accounts yet. Create one to continue.</div>
          )}
        </div>

        <div className="account-detail">
          {selectedAccount ? (
            <>
              <div className="user-chip">
                <strong>{selectedAccount.account_type}</strong>
                <span>Account ID: {selectedAccount.id}</span>
                <span>User ID: {selectedAccount.user_id}</span>
                <span>Balance: ${Number(selectedAccount.balance).toFixed(2)}</span>
              </div>

              <div className="transaction-grid">
                <form className="auth-form compact-form" onSubmit={onDeposit}>
                  <label>
                    Deposit amount
                    <input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={depositAmount}
                      onChange={(event) => onDepositAmountChange(event.target.value)}
                      placeholder="100.00"
                    />
                  </label>

                  <button type="submit" disabled={isBusy}>
                    Deposit
                  </button>
                </form>

                <form className="auth-form compact-form" onSubmit={onWithdraw}>
                  <label>
                    Withdraw amount
                    <input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={withdrawAmount}
                      onChange={(event) => onWithdrawAmountChange(event.target.value)}
                      placeholder="25.00"
                    />
                  </label>

                  <button type="submit" disabled={isBusy}>
                    Withdraw
                  </button>
                </form>
              </div>

              <div className="transaction-history">
                <div className="account-list-header">
                  <h3>Account details</h3>
                  <button type="button" className="ghost-button" onClick={onRefreshAccount} disabled={isBusy}>
                    Reload
                  </button>
                </div>

                <ul>
                  <li><strong>Account</strong><span>{selectedAccount.account_type}</span></li>
                  <li><strong>Balance</strong><span>${Number(selectedAccount.balance).toFixed(2)}</span></li>
                  <li><strong>User</strong><span>{selectedAccount.user_id}</span></li>
                </ul>

                <h4>Transaction history</h4>
                {selectedAccount.transactions?.length ? (
                  <div className="transaction-list">
                    {selectedAccount.transactions.map((transaction, index) => (
                      <article key={`${transaction.type}-${index}`} className="transaction-item">
                        <strong>{transaction.type}</strong>
                        <span>${Number(transaction.amount).toFixed(2)}</span>
                        <small>{transaction.created_at ?? 'Pending timestamp'}</small>
                      </article>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state">No transactions yet.</div>
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">Log in and select an account to see details, deposits, withdrawals, and history.</div>
          )}
        </div>
      </div>
    </section>
  )
}

export default AccountPanel
