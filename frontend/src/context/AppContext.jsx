import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { getHealth } from '../services/api'

const AppContext = createContext(null)

/**
 * Global application state provider.
 * Provides: language toggle (hi/en), backend health status, loading flag.
 */
export function AppProvider({ children }) {
  // Default language: Hindi
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('kv_language') || 'hi'
  })

  const [health, setHealth] = useState(null)
  const [healthLoading, setHealthLoading] = useState(true)
  const [healthError, setHealthError] = useState(null)

  // Persist language preference
  const toggleLanguage = useCallback(() => {
    setLanguage(prev => {
      const next = prev === 'hi' ? 'en' : 'hi'
      localStorage.setItem('kv_language', next)
      return next
    })
  }, [])

  const fetchHealth = useCallback(async () => {
    setHealthLoading(true)
    setHealthError(null)
    try {
      const data = await getHealth()
      setHealth(data)
    } catch (err) {
      setHealthError(err.message)
      setHealth(null)
    } finally {
      setHealthLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchHealth()
    // Re-check health every 60 seconds
    const interval = setInterval(fetchHealth, 60000)
    return () => clearInterval(interval)
  }, [fetchHealth])

  const value = {
    language,
    setLanguage,
    toggleLanguage,
    health,
    healthLoading,
    healthError,
    refreshHealth: fetchHealth,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

/** Hook — consume app-wide context */
export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used inside AppProvider')
  return ctx
}

