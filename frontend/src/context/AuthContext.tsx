import React, { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../services/api'

interface AuthContextValue {
  token: string | null
  login: (username: string, password: string) => Promise<void>
  register: (data: { email: string; username: string; full_name: string; password: string }) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  async function login(username: string, password: string) {
    const form = new FormData()
    form.append('username', username)
    form.append('password', password)
    const res = await api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    setToken(res.data.access_token)
  }

  async function register(data: { email: string; username: string; full_name: string; password: string }) {
    const res = await api.post('/auth/register', data)
    setToken(res.data.access_token)
  }

  function logout() {
    setToken(null)
  }

  return <AuthContext.Provider value={{ token, login, register, logout }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
