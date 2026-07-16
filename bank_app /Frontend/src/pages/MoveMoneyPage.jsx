import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAccounts } from '../accounts/useAccounts.js'

function formatMoney(amount) {
  return `$${Number(amount).toFixed(2)}`
}

function MoveMoneyPage() {
  const {
    accounts,
    selectedAccountId,
    selectedAccount,
    selectAccount,
    deposit,
    withdraw,
    isBusy,
    showMessage,
  } = useAccounts()
  const [depositAmount, setDepositAmount] = useState('')
  const [withdrawAmount, setWithdrawAmount] = useState('')

  const handleDeposit = async (event) => {
    event.preventDefault()
    try {
      await deposit(depositAmount)
      setDepositAmount('')
    } catch (error) {
      showMessage(error.message, 'error')
    }
  }

  const handleWithdraw = async (event) => {
    event.preventDefault()
    try {
      await withdraw(withdrawAmount)
      setWithdrawAmount('')
    } catch (error) {
      showMessage(error.message, 'error')
    }
  }

  if (!accounts.length) {
    return (
      <section className="page">
        <header className="page-header">
          <div>
            <p className="status-label">Move money</p>
            <h2>Deposit or withdraw</h2>
          </div>
        </header>
        <div className="empty-state">
          Open an account first, then return here. <Link to="/accounts/new">Open account</Link>
        </div>
      </section>
    )
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="status-label">Move money</p>
          <h2>Deposit or withdraw</h2>
          <p className="lede compact">
            {selectedAccount
              ? `Working with ${selectedAccount.account_type} · ${formatMoney(selectedAccount.balance)}`
              : 'Select an account to continue.'}
          </p>
        </div>
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

      <div className="transaction-grid">
        <form className="auth-form compact-form" onSubmit={handleDeposit}>
          <label>
            Deposit amount
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={depositAmount}
              onChange={(event) => setDepositAmount(event.target.value)}
              placeholder="100.00"
              required
            />
          </label>
          <button type="submit" disabled={isBusy || !selectedAccountId}>
            Deposit
          </button>
        </form>

        <form className="auth-form compact-form" onSubmit={handleWithdraw}>
          <label>
            Withdraw amount
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={withdrawAmount}
              onChange={(event) => setWithdrawAmount(event.target.value)}
              placeholder="25.00"
              required
            />
          </label>
          <button type="submit" disabled={isBusy || !selectedAccountId}>
            Withdraw
          </button>
        </form>
      </div>
    </section>
  )
}

export default MoveMoneyPage
