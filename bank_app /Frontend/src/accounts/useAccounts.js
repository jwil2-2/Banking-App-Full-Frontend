import { useContext } from 'react'
import { AccountContext } from './account-context.js'

export function useAccounts() {
  const context = useContext(AccountContext)
  if (!context) {
    throw new Error('useAccounts must be used within AccountProvider')
  }
  return context
}
