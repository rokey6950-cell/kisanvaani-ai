import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  Home, Mic, Wheat, FileText, TrendingUp, Cloud, History, Info,
} from 'lucide-react'
import { useApp } from '../../context/AppContext'

const NAV_LINKS = [
  { to: '/',              label: 'होम',              labelEn: 'Home',          icon: Home },
  { to: '/assistant',     label: 'AI सहायक',          labelEn: 'AI Assistant',  icon: Mic },
  { to: '/crop-advisory', label: 'फसल सलाह',         labelEn: 'Crop Advisory', icon: Wheat },
  { to: '/schemes',       label: 'सरकारी योजनाएं',    labelEn: 'Schemes',       icon: FileText },
  { to: '/mandi',         label: 'मंडी भाव',          labelEn: 'Mandi Prices',  icon: TrendingUp },
  { to: '/weather',       label: 'मौसम',              labelEn: 'Weather',       icon: Cloud },
  { to: '/history',       label: 'बातचीत इतिहास',     labelEn: 'History',       icon: History },
  { to: '/about',         label: 'हमारे बारे में',      labelEn: 'About',         icon: Info },
]

/**
 * Desktop sidebar — shown at lg breakpoint and above alongside main content.
 * Hidden on mobile (Navbar handles mobile navigation via dropdown).
 */
export default function Sidebar() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  return (
    <aside className="hidden lg:flex flex-col w-56 min-h-screen bg-white border-r border-gray-200 pt-4">
      <nav className="flex flex-col gap-0.5 px-3">
        {NAV_LINKS.map(({ to, label, labelEn, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-green-50 text-green-700 border border-green-200'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <Icon className="w-4 h-4 flex-shrink-0" />
            <span>{isHindi ? label : labelEn}</span>
          </NavLink>
        ))}
      </nav>

      {/* Bottom credit */}
      <div className="mt-auto px-4 py-4 text-xs text-gray-400 border-t border-gray-100">
        <p className="font-medium text-gray-500">किसानवाणी AI</p>
        <p>अपनी भाषा, अपनी खेती</p>
        <p>Smart Faisle.</p>
      </div>
    </aside>
  )
}

