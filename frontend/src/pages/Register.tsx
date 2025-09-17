import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [fullName, setFullName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await register({ email, username, full_name: fullName, password })
      navigate('/')
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <form className="card" onSubmit={onSubmit}>
        <h2>Create your account</h2>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="demo" />
        <label>Full Name</label>
        <input value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Demo User" />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Create Account'}</button>
        <p className="muted">Already have an account? <Link to="/login">Sign in</Link></p>
      </form>
    </div>
  )
}
