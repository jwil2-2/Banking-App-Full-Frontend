import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AuthPanel from '../components/AuthPanel.jsx'
import StatusBanner from '../components/StatusBanner.jsx'
import { useAuth } from '../auth/useAuth.js'

const emptySignup = {
  name: '',
  email: '',
  password: '',
}

const emptyLogin = {
  email: '',
  password: '',
}

function AuthPage() {
  const { login, signup, isBusy } = useAuth()
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('login')
  const [signupForm, setSignupForm] = useState(emptySignup)
  const [loginForm, setLoginForm] = useState(emptyLogin)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('neutral')

  const handleSignupSubmit = async (event) => {
    event.preventDefault()
    try {
      const user = await signup(signupForm)
      setSignupForm(emptySignup)
      setMessage(`Welcome, ${user.name}.`)
      setMessageType('success')
      navigate('/overview', { replace: true })
    } catch (error) {
      setMessage(error.message)
      setMessageType('error')
    }
  }

  const handleLoginSubmit = async (event) => {
    event.preventDefault()
    try {
      const user = await login(loginForm.email, loginForm.password)
      setLoginForm(emptyLogin)
      setMessage(`Welcome back, ${user.name}.`)
      setMessageType('success')
      navigate('/overview', { replace: true })
    } catch (error) {
      setMessage(error.message)
      setMessageType('error')
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-hero">
        <p className="eyebrow">Ledgerline</p>
        <h1>Banking that starts with you.</h1>
        <p className="lede">
          Sign in or create an account to open checking and savings, move money, and review your activity.
        </p>
      </section>

      <section className="auth-card">
        <AuthPanel
          activeTab={activeTab}
          onTabChange={setActiveTab}
          signup={signupForm}
          onSignupChange={setSignupForm}
          login={loginForm}
          onLoginChange={setLoginForm}
          onSignupSubmit={handleSignupSubmit}
          onLoginSubmit={handleLoginSubmit}
          isBusy={isBusy}
        />
        <StatusBanner message={message} messageType={messageType} />
      </section>
    </main>
  )
}

export default AuthPage
