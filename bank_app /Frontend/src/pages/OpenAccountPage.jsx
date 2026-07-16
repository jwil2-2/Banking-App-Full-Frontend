import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAccounts } from '../accounts/useAccounts.js'

function OpenAccountPage() {
  const { createAccount, isBusy, showMessage } = useAccounts()
  const [accountType, setAccountType] = useState('Checking')
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()
    try {
      await createAccount(accountType)
      navigate('/overview')
    } catch (error) {
      showMessage(error.message, 'error')
    }
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <p className="status-label">Open account</p>
          <h2>Start a checking or savings account</h2>
          <p className="lede compact">New accounts begin at $0.00. You can fund them from Move Money.</p>
        </div>
      </header>

      <form className="auth-form page-form" onSubmit={handleSubmit}>
        <label>
          Account type
          <select value={accountType} onChange={(event) => setAccountType(event.target.value)}>
            <option value="Checking">Checking</option>
            <option value="Savings">Savings</option>
          </select>
        </label>

        <button type="submit" disabled={isBusy}>
          {isBusy ? 'Creating...' : 'Create account'}
        </button>
      </form>
    </section>
  )
}

export default OpenAccountPage
