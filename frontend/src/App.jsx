import React, { Suspense, lazy } from 'react'
import { Routes, Route } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import Navbar from './components/Layout/Navbar'
import Sidebar from './components/Layout/Sidebar'

// Lazy-load pages for code splitting
const HomePage           = lazy(() => import('./pages/HomePage'))
const VoiceAssistantPage = lazy(() => import('./pages/VoiceAssistantPage'))
const CropAdvisoryPage   = lazy(() => import('./pages/CropAdvisoryPage'))
const SchemesPage        = lazy(() => import('./pages/SchemesPage'))
const MandiPage          = lazy(() => import('./pages/MandiPage'))
const WeatherPage        = lazy(() => import('./pages/WeatherPage'))
const HistoryPage        = lazy(() => import('./pages/HistoryPage'))
const AboutPage          = lazy(() => import('./pages/AboutPage'))

function PageLoader() {
  return (
    <div className="flex items-center justify-center h-48">
      <div className="animate-spin rounded-full h-10 w-10 border-4 border-green-600 border-t-transparent" />
    </div>
  )
}

export default function App() {
  return (
    <AppProvider>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 min-h-screen">
            <Suspense fallback={<PageLoader />}>
              <Routes>
                <Route path="/"              element={<HomePage />} />
                <Route path="/assistant"     element={<VoiceAssistantPage />} />
                <Route path="/crop-advisory" element={<CropAdvisoryPage />} />
                <Route path="/schemes"       element={<SchemesPage />} />
                <Route path="/mandi"         element={<MandiPage />} />
                <Route path="/weather"       element={<WeatherPage />} />
                <Route path="/history"       element={<HistoryPage />} />
                <Route path="/about"         element={<AboutPage />} />
                {/* 404 fallback */}
                <Route path="*" element={
                  <div className="p-8 text-center">
                    <h2 className="text-2xl font-bold text-gray-700">404 — पेज नहीं मिला</h2>
                    <p className="text-gray-500 mt-2">यह पेज उपलब्ध नहीं है।</p>
                  </div>
                } />
              </Routes>
            </Suspense>
          </main>
        </div>
      </div>
    </AppProvider>
  )
}

