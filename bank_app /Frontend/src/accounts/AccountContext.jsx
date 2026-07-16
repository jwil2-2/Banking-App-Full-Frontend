import { useCallback, useEffect, useMemo, useState } from 'react'
import { requestJson } from '../api/client.js'
import { useAuth } from '../auth/useAuth.js'
import { AccountContext } from './account-context.js'

const SELECTED_ACCOUNT_KEY = 'bank_app_selected_account'

function readSelectedAccountId() {
  try {
    return sessionStorage.getItem(SELECTED_ACCOUNT_KEY) || ''
  } catch {
    return ''
  }
}

function writeSelectedAccountId(accountId) {
  try {
    if (accountId) {
      sessionStorage.setItem(SELECTED_ACCOUNT_KEY, accountId)
    } else {
      sessionStorage.removeItem(SELECTED_ACCOUNT_KEY)
    }
  } catch {
    // ignore storage failures
  }
}

export function AccountProvider({ children }) {
  const { user } = useAuth()
  const userId = user?.id
  const [accounts, setAccounts] = useState([])
  const [selectedAccountId, setSelectedAccountIdState] = useState(() => readSelectedAccountId())
  const [selectedAccount, setSelectedAccount] = useState(null)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('neutral')
  const [isBusy, setIsBusy] = useState(false)

  const showMessage = useCallback((nextMessage, nextType = 'neutral') => {
    setMessage(nextMessage)
    setMessageType(nextType)
  }, [])

  const clearMessage = useCallback(() => {
    setMessage('')
    setMessageType('neutral')
  }, [])

  const setSelectedAccountId = useCallback((accountId) => {
    setSelectedAccountIdState(accountId)
    writeSelectedAccountId(accountId)
  }, [])

  useEffect(() => {
    if (!userId) {
      return
    }

    let cancelled = false

    ;(async () => {
      try {
        const accountList = await requestJson('/api/accounts')
        if (cancelled) {
          return
        }

        setAccounts(accountList)

        const preferred = readSelectedAccountId()
        const nextAccountId =
          (preferred && accountList.some((account) => account.id === preferred) && preferred) ||
          accountList[0]?.id ||
          ''

        setSelectedAccountId(nextAccountId)

        if (nextAccountId) {
          const accountDetail = await requestJson(`/api/accounts/${nextAccountId}`)
          if (!cancelled) {
            setSelectedAccount(accountDetail)
          }
        } else if (!cancelled) {
          setSelectedAccount(null)
        }
      } catch (error) {
        if (!cancelled) {
          showMessage(error.message, 'error')
        }
      }
    })()

    return () => {
      cancelled = true
    }
  }, [userId, setSelectedAccountId, showMessage])

  const loadAccounts = useCallback(
    async (preferredAccountId = '') => {
      if (!userId) {
        setAccounts([])
        setSelectedAccountId('')
        setSelectedAccount(null)
        return []
      }

      const accountList = await requestJson('/api/accounts')
      setAccounts(accountList)

      const preferred = preferredAccountId || selectedAccountId || readSelectedAccountId()
      const nextAccountId =
        (preferred && accountList.some((account) => account.id === preferred) && preferred) ||
        accountList[0]?.id ||
        ''

      setSelectedAccountId(nextAccountId)

      if (nextAccountId) {
        const accountDetail = await requestJson(`/api/accounts/${nextAccountId}`)
        setSelectedAccount(accountDetail)
      } else {
        setSelectedAccount(null)
      }

      return accountList
    },
    [userId, selectedAccountId, setSelectedAccountId],
  )

  const selectAccount = useCallback(
    async (accountId) => {
      setSelectedAccountId(accountId)
      try {
        const accountDetail = await requestJson(`/api/accounts/${accountId}`)
        setSelectedAccount(accountDetail)
      } catch (error) {
        showMessage(error.message, 'error')
      }
    },
    [setSelectedAccountId, showMessage],
  )

  const createAccount = useCallback(
    async (accountType) => {
      if (!userId) {
        throw new Error('Create or log in to a user first.')
      }

      setIsBusy(true)
      try {
        const account = await requestJson('/api/accounts', {
          method: 'POST',
          body: JSON.stringify({ account_type: accountType }),
        })
        await loadAccounts(account.id)
        showMessage(`${account.account_type} account created.`, 'success')
        return account
      } finally {
        setIsBusy(false)
      }
    },
    [userId, loadAccounts, showMessage],
  )

  const deposit = useCallback(
    async (amount) => {
      if (!selectedAccountId) {
        throw new Error('Select an account first.')
      }

      setIsBusy(true)
      try {
        await requestJson(`/api/accounts/${selectedAccountId}/deposit`, {
          method: 'POST',
          body: JSON.stringify({ amount }),
        })
        await loadAccounts(selectedAccountId)
        showMessage('Deposit completed.', 'success')
      } finally {
        setIsBusy(false)
      }
    },
    [selectedAccountId, loadAccounts, showMessage],
  )

  const withdraw = useCallback(
    async (amount) => {
      if (!selectedAccountId) {
        throw new Error('Select an account first.')
      }

      setIsBusy(true)
      try {
        await requestJson(`/api/accounts/${selectedAccountId}/withdraw`, {
          method: 'POST',
          body: JSON.stringify({ amount }),
        })
        await loadAccounts(selectedAccountId)
        showMessage('Withdrawal completed.', 'success')
      } finally {
        setIsBusy(false)
      }
    },
    [selectedAccountId, loadAccounts, showMessage],
  )

  const refreshAccount = useCallback(async () => {
    if (!userId) {
      return
    }

    setIsBusy(true)
    try {
      await loadAccounts(selectedAccountId)
      showMessage('Account data refreshed.', 'success')
    } finally {
      setIsBusy(false)
    }
  }, [userId, selectedAccountId, loadAccounts, showMessage])

  const totalBalance = useMemo(
    () => accounts.reduce((sum, account) => sum + Number(account.balance ?? 0), 0),
    [accounts],
  )

  const value = useMemo(
    () => ({
      accounts,
      selectedAccountId,
      selectedAccount,
      totalBalance,
      message,
      messageType,
      isBusy,
      showMessage,
      clearMessage,
      selectAccount,
      createAccount,
      deposit,
      withdraw,
      refreshAccount,
      loadAccounts,
    }),
    [
      accounts,
      selectedAccountId,
      selectedAccount,
      totalBalance,
      message,
      messageType,
      isBusy,
      showMessage,
      clearMessage,
      selectAccount,
      createAccount,
      deposit,
      withdraw,
      refreshAccount,
      loadAccounts,
    ],
  )

  return <AccountContext.Provider value={value}>{children}</AccountContext.Provider>
}
