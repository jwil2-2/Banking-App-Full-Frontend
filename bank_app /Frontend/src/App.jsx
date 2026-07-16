import { useEffect, useMemo, useState } from 'react'
import AuthPanel from './components/AuthPanel.jsx'
import AccountPanel from './components/AccountPanel.jsx'
import StatusBanner from './components/StatusBanner.jsx'
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

const emptyAmount = ''

function App() {
  const [signup, setSignup] = useState(emptySignup)
  const [login, setLogin] = useState(emptyLogin)
  const [activeTab, setActiveTab] = useState('signup')
  const [accountType, setAccountType] = useState('Checking')
  const [depositAmount, setDepositAmount] = useState(emptyAmount)
  const [withdrawAmount, setWithdrawAmount] = useState(emptyAmount)
  const [currentUser, setCurrentUser] = useState(null)
  const [accounts, setAccounts] = useState([])
  const [selectedAccountId, setSelectedAccountId] = useState('')
  const [selectedAccount, setSelectedAccount] = useState(null)
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

  const loadAccounts = async (userId, preferredAccountId = '') => {
    if (!userId) {
      setAccounts([])
      setSelectedAccountId('')
      setSelectedAccount(null)
      return
    }

    const accountList = await requestJson(`/api/accounts?userId=${userId}`)
    setAccounts(accountList)

    const nextAccountId = preferredAccountId || accountList[0]?.id || ''
    setSelectedAccountId(nextAccountId)

    if (nextAccountId) {
      const accountDetail = await requestJson(`/api/accounts/${nextAccountId}`)
      setSelectedAccount(accountDetail)
    } else {
      setSelectedAccount(null)
    }
  }

  useEffect(() => {
    if (!currentUser?.id) {
      return
    }

    loadAccounts(currentUser.id).catch((error) => showMessage(error.message, 'error'))
  }, [currentUser?.id])

  const selectedAccountSummary = useMemo(() => {
    if (!selectedAccount) {
      return null
    }

    return {
      id: selectedAccount.id,
      account_type: selectedAccount.account_type,
      user_id: selectedAccount.user_id,
      balance: selectedAccount.balance,
      transactions: selectedAccount.transactions ?? [],
    }
  }, [selectedAccount])

  const handleSignupSubmit = async (event) => {
    event.preventDefault()
    setIsBusy(true)

    try {
      const user = await requestJson('/api/users', {
        method: 'POST',
        body: JSON.stringify(signup),
      })

      setCurrentUser(user)
      showMessage(`Created ${user.name}. You can start opening accounts now.`, 'success')
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
      const account = await requestJson(`/api/accounts?userId=${currentUser.id}`, {
        method: 'POST',
        body: JSON.stringify({ account_type: accountType }),
      })

      await loadAccounts(currentUser.id, account.id)
      showMessage(`${account.account_type} account created for ${currentUser.name}.`, 'success')
    } catch (error) {
      showMessage(error.message, 'error')
    } finally {
      setIsBusy(false)
    }
  }

  const handleSelectAccount = async (accountId) => {
    setSelectedAccountId(accountId)

    try {
      const accountDetail = await requestJson(`/api/accounts/${accountId}`)
      setSelectedAccount(accountDetail)
    } catch (error) {
      showMessage(error.message, 'error')
    }
  }

  const handleDeposit = async (event) => {
    event.preventDefault()

    if (!selectedAccountId) {
      showMessage('Select an account first.', 'error')
      return
    }

    setIsBusy(true)

    try {
      await requestJson(`/api/accounts/${selectedAccountId}/deposit`, {
        method: 'POST',
        body: JSON.stringify({ amount: depositAmount }),
      })

      await loadAccounts(currentUser.id, selectedAccountId)
      setDepositAmount(emptyAmount)
      showMessage('Deposit completed.', 'success')
    } catch (error) {
      showMessage(error.message, 'error')
    } finally {
      setIsBusy(false)
    }
  }

  const handleWithdraw = async (event) => {
    event.preventDefault()

    if (!selectedAccountId) {
      showMessage('Select an account first.', 'error')
      return
    }

    setIsBusy(true)

    try {
      await requestJson(`/api/accounts/${selectedAccountId}/withdraw`, {
        method: 'POST',
        body: JSON.stringify({ amount: withdrawAmount }),
      })

      await loadAccounts(currentUser.id, selectedAccountId)
      setWithdrawAmount(emptyAmount)
      showMessage('Withdrawal completed.', 'success')
    } catch (error) {
      showMessage(error.message, 'error')
    } finally {
      setIsBusy(false)
    }
  }

  const handleRefreshAccount = async () => {
    if (!currentUser?.id || !selectedAccountId) {
      return
    }

    setIsBusy(true)

    try {
      await loadAccounts(currentUser.id, selectedAccountId)
      showMessage('Account data refreshed.', 'success')
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
          <h1>Simple banking flow, now with accounts and transactions.</h1>
          <p className="lede">
            Create a user, log in, open accounts, and run deposits or withdrawals.
            The page is split into small components so each step stays easy to follow.
          </p>

          <div className="feature-row">
            <article>
              <span>1</span>
              <strong>Create a user</strong>
              <p>Store a name, email, password, and role.</p>
            </article>
            <article>
              <span>2</span>
              <strong>Open an account</strong>
              <p>Create checking or savings accounts for the logged-in user.</p>
            </article>
            <article>
              <span>3</span>
              <strong>Move money</strong>
              <p>Deposit, withdraw, and inspect the live transaction history.</p>
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
              <span>Accounts</span>
              <strong>{accounts.length}</strong>
            </div>
            <div>
              <span>Role</span>
              <strong>{currentUser?.role ?? 'guest'}</strong>
            </div>
          </div>
        </aside>
      </section>

      <section className="forms-grid">
        <AuthPanel
          activeTab={activeTab}
          onTabChange={setActiveTab}
          signup={signup}
          onSignupChange={setSignup}
          login={login}
          onLoginChange={setLogin}
          onSignupSubmit={handleSignupSubmit}
          onLoginSubmit={handleLoginSubmit}
          isBusy={isBusy}
        />

        <AccountPanel
          currentUser={currentUser}
          accounts={accounts}
          selectedAccountId={selectedAccountId}
          selectedAccount={selectedAccountSummary}
          accountType={accountType}
          onAccountTypeChange={setAccountType}
          depositAmount={depositAmount}
          onDepositAmountChange={setDepositAmount}
          withdrawAmount={withdrawAmount}
          onWithdrawAmountChange={setWithdrawAmount}
          onCreateAccount={handleCreateAccount}
          onSelectAccount={handleSelectAccount}
          onDeposit={handleDeposit}
          onWithdraw={handleWithdraw}
          onRefreshAccount={handleRefreshAccount}
          isBusy={isBusy}
        />
      </section>

      <StatusBanner message={message} messageType={messageType} />
    </main>
  )
}

export default App
