import React, { useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router-dom'
import {
  Mic,
  Wheat,
  FileText,
  TrendingUp,
  Cloud,
  History,
  Info,
  Home,
  Menu,
  X,
  Leaf,
} from 'lucide-react'
import { useApp } from '../../context/AppContext'

const NAV_LINKS = [
  { to: '/',           label: 'होम',            labelEn: 'Home',        icon: Home },
  { to: '/assistant',  label: 'AI सहायक',        labelEn: 'AI Assistant', icon: Mic },
  { to: '/crop-advisory', label: 'फसल सलाह',   labelEn: 'Crop Advisory', icon: Wheat },
  { to: '/schemes',    label: 'सरकारी योजनाएं',  labelEn: 'Schemes',     icon: FileText },
  { to: '/mandi',      label: 'मंडी भाव',        labelEn: 'Mandi Prices', icon: TrendingUp },
  { to: '/weather',    label: 'मौसम',            labelEn: 'Weather',     icon: Cloud },
  { to: '/history',    label: 'बातचीत इतिहास',   labelEn: 'History',     icon: History },
  { to: '/about',      label: 'हमारे बारे में',    labelEn: 'About',       icon: Info },
]

export default function Navbar() {
  const { language, toggleLanguage, health, healthLoading } = useApp()
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()

  const isHindi = language === 'hi'

  const healthDot = () => {
    if (healthLoading) return 'bg-yellow-400'
    if (!health) return 'bg-red-500'
    if (health.status === 'healthy') return 'bg-green-400'
    return 'bg-yellow-400'
  }

  return (
    <>
      {/* Top navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-green-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 text-white font-bold text-xl">
              <Leaf className="w-7 h-7 text-yellow-300" />
              <span className="hidden sm:inline">किसानवाणी AI</span>
              <span className="sm:hidden">KV AI</span>
            </Link>

            {/* Desktop links */}
            <div className="hidden lg:flex items-center gap-1">
              {NAV_LINKS.map(({ to, label, labelEn, icon: Icon }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={to === '/'}
                  className={({ isActive }) =>
                    `flex items-center gap-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-green-900 text-white'
                        : 'text-green-100 hover:bg-green-600 hover:text-white'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{isHindi ? label : labelEn}</span>
                </NavLink>
              ))}
            </div>

            {/* Right controls */}
            <div className="flex items-center gap-3">
              {/* Backend health indicator */}
              <div className="hidden sm:flex items-center gap-1.5 text-xs text-green-200">
                <span className={`w-2 h-2 rounded-full ${healthDot()}`} />
                <span>{healthLoading ? '...' : health?.status === 'healthy' ? 'Online' : 'Offline'}</span>
              </div>

              {/* Language toggle */}
              <button
                onClick={toggleLanguage}
                className="bg-green-600 hover:bg-green-500 text-white text-sm font-medium px-3 py-1.5 rounded-md transition-colors border border-green-500"
                title="भाषा बदलें / Switch Language"
              >
                {isHindi ? 'EN' : 'हिं'}
              </button>

              {/* Mobile menu button */}
              <button
                onClick={() => setMobileOpen(o => !o)}
                className="lg:hidden text-white p-1"
                aria-label="Toggle menu"
              >
                {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile dropdown */}
        {mobileOpen && (
          <div className="lg:hidden bg-green-800 border-t border-green-600 pb-2">
            {NAV_LINKS.map(({ to, label, labelEn, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                onClick={() => setMobileOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-green-900 text-white'
                      : 'text-green-100 hover:bg-green-700'
                  }`
                }
              >
                <Icon className="w-5 h-5" />
                <span>{isHindi ? label : labelEn}</span>
              </NavLink>
            ))}
          </div>
        )}
      </nav>

      {/* Spacer so content doesn't hide behind fixed navbar */}
      <div className="h-16" />
    </>
  )
}

