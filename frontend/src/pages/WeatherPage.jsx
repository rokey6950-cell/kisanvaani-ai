import React, { useState, useEffect } from 'react'
import {
  Cloud,
  Loader,
  AlertCircle,
  Search,
  Droplets,
  Wind,
  Info,
  ExternalLink,
  ShieldAlert,
  Sprout,
  SunMedium,
  CheckCircle2,
  Calendar,
  Compass,
  Eye,
  RefreshCw,
} from 'lucide-react'
import { useApp } from '../context/AppContext'
import { getWeather, getWeatherLocations, getWeatherStatus } from '../services/api'

export default function WeatherPage() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  const [location, setLocation] = useState('Karnal')
  const [customLocation, setCustomLocation] = useState('')
  const [stationLocations, setStationLocations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [weatherData, setWeatherData] = useState(null)
  const [imdStatus, setImdStatus] = useState(null)
  const [showImdModal, setShowImdModal] = useState(false)

  // Quick preset pills
  const quickLocations = [
    { label: isHindi ? 'करनाल (हरियाणा)' : 'Karnal (HR)', query: 'Karnal' },
    { label: isHindi ? 'हिसार (हरियाणा)' : 'Hisar (HR)', query: 'Hisar' },
    { label: isHindi ? 'लुधियाना (पंजाब)' : 'Ludhiana (PB)', query: 'Ludhiana' },
    { label: isHindi ? 'लखनऊ (उ.प्र.)' : 'Lucknow (UP)', query: 'Lucknow' },
    { label: isHindi ? 'जयपुर (राजस्थान)' : 'Jaipur (RJ)', query: 'Jaipur' },
    { label: isHindi ? 'शिमला (हि.प्र.)' : 'Shimla (HP)', query: 'Shimla' },
    { label: isHindi ? 'देहरादून (उत्तराखंड)' : 'Dehradun (UK)', query: 'Dehradun' },
    { label: isHindi ? 'दिल्ली NCR' : 'Delhi NCR', query: 'Delhi' },
  ]

  // Initial load
  useEffect(() => {
    fetchInitialData()
  }, [])

  const fetchInitialData = async () => {
    try {
      const [locsRes, statusRes] = await Promise.allSettled([
        getWeatherLocations(),
        getWeatherStatus(),
      ])
      if (locsRes.status === 'fulfilled') {
        setStationLocations(locsRes.value.locations || [])
      }
      if (statusRes.status === 'fulfilled') {
        setImdStatus(statusRes.value)
      }
    } catch (_) {
      // Non-critical background metadata
    }
    // Load default weather for Karnal
    loadWeather('Karnal')
  }

  const loadWeather = async (targetLoc) => {
    const loc = targetLoc || customLocation.trim() || location
    if (!loc) {
      setError(isHindi ? 'कृपया कोई स्थान चुनें या नाम लिखें।' : 'Please select or enter a location.')
      return
    }
    setError(null)
    setLoading(true)
    try {
      const data = await getWeather(loc)
      setWeatherData(data)
    } catch (err) {
      setError(err.message || 'मौसम डेटा लोड करने में त्रुटि')
    } finally {
      setLoading(false)
    }
  }

  const handleSelectChange = (e) => {
    const val = e.target.value
    setLocation(val)
    setCustomLocation('')
    loadWeather(val)
  }

  const handleQuickClick = (query) => {
    setLocation(query)
    setCustomLocation('')
    loadWeather(query)
  }

  const handleFormSubmit = (e) => {
    e.preventDefault()
    if (customLocation.trim()) {
      loadWeather(customLocation.trim())
    } else {
      loadWeather(location)
    }
  }

  const spray = weatherData?.spray_advisory || {}
  const irrigation = weatherData?.irrigation_advisory || {}
  const harvest = weatherData?.harvest_advisory || {}
  const forecast = weatherData?.forecast || []

  // Status styles for Spray Advisory
  const getSprayBadge = (status) => {
    if (status === 'good') {
      return {
        bg: 'bg-emerald-50 text-emerald-800 border-emerald-300',
        dot: 'bg-emerald-500',
        text: isHindi ? '✅ छिड़काव के लिए उत्तम' : '✅ Optimal for Spray',
      }
    }
    if (status === 'caution') {
      return {
        bg: 'bg-amber-50 text-amber-800 border-amber-300',
        dot: 'bg-amber-500',
        text: isHindi ? '⚠️ सावधानी से छिड़काव करें' : '⚠️ Spray with Caution',
      }
    }
    return {
      bg: 'bg-red-50 text-red-800 border-red-300',
      dot: 'bg-red-500',
      text: isHindi ? '🛑 आज छिड़काव न करें' : '🛑 Avoid Spray Today',
    }
  }

  const sprayBadge = getSprayBadge(spray.status)

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gradient-to-br from-sky-500 to-blue-600 text-white rounded-2xl shadow-sm">
            <Cloud className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {isHindi ? 'मौसम आधारित कृषि सलाह' : 'Weather-Based Agricultural Advisory'}
            </h1>
            <p className="text-sm text-gray-500">
              {isHindi
                ? 'IMD एग्रोमेट प्रारूप पर आधारित 7 राज्यों के लिए दैनिक मौसम व फसल सुरक्षा निर्देश'
                : 'Daily weather & farm advisory for 7 pilot states based on IMD Agromet format'}
            </p>
          </div>
        </div>

        {/* IMD Policy Notice Pill */}
        <button
          onClick={() => setShowImdModal(!showImdModal)}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-amber-100 text-amber-900 border border-amber-300 hover:bg-amber-200 transition-colors self-start sm:self-center"
        >
          <Info className="w-3.5 h-3.5 text-amber-700" />
          <span>{isHindi ? 'नमूना डेटा (IMD नीति)' : 'Sample Data (IMD Policy)'}</span>
        </button>
      </div>

      {/* IMD Disclosure Banner */}
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 mb-6 text-xs text-amber-900 leading-relaxed shadow-sm">
        <div className="flex items-start gap-2.5">
          <ShieldAlert className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <div className="font-semibold text-amber-950 mb-0.5 flex flex-wrap items-center gap-2">
              <span>{isHindi ? '⚠️ अनिवार्य प्रकटीकरण (IMD Agromet Data Policy):' : '⚠️ Mandatory Disclosure (IMD Agromet Data Policy):'}</span>
              <span className="bg-amber-200 text-amber-900 px-2 py-0.5 rounded text-[11px] font-mono">data_type: sample</span>
            </div>
            <p>
              {isHindi
                ? 'भारतीय मौसम विज्ञान विभाग (IMD) का API गैर-व्यावसायिक उपयोग के लिए उपलब्ध है, परंतु किसी भी व्यावसायिक या व्यापक सार्वजनिक उपयोग हेतु नोडल अधिकारी की पूर्व लिखित अनुमति अनिवार्य है। किसानवाणी AI में यह डेटा मानक बेंचमार्क नमूना है। वास्तविक एवं आधिकारिक पूर्वानुमान के लिए सरकारी पोर्टल mausam.imd.gov.in या मेघदूत (Meghdoot) मोबाइल ऐप देखें।'
                : 'India Meteorological Department (IMD) APIs require written permission from the nodal officer for commercial or public deployments. All data in KisanVaani AI is benchmark sample data. For real-time official forecasts, use mausam.imd.gov.in or the Meghdoot mobile app.'}
            </p>
            <div className="flex flex-wrap items-center gap-4 mt-2 font-medium">
              <a
                href="https://mausam.imd.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-700 hover:text-blue-900 inline-flex items-center gap-1 underline"
              >
                mausam.imd.gov.in <ExternalLink className="w-3 h-3" />
              </a>
              <a
                href="https://agromet.imd.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-700 hover:text-blue-900 inline-flex items-center gap-1 underline"
              >
                agromet.imd.gov.in <ExternalLink className="w-3 h-3" />
              </a>
              <a
                href="https://play.google.com/store/apps/details?id=com.imd.meghdoot"
                target="_blank"
                rel="noopener noreferrer"
                className="text-emerald-700 hover:text-emerald-900 inline-flex items-center gap-1 underline"
              >
                {isHindi ? 'मेघदूत ऐप (Google Play)' : 'Meghdoot App'} <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Location Selector Controls */}
      <div className="bg-white border border-gray-200 rounded-2xl p-5 mb-6 shadow-sm">
        <form onSubmit={handleFormSubmit} className="grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
          {/* Preset Dropdown */}
          <div className="md:col-span-5">
            <label className="block text-xs font-semibold text-gray-700 mb-1.5">
              {isHindi ? 'राज्य व जिला चुनें' : 'Select State & District'}
            </label>
            <select
              value={location}
              onChange={handleSelectChange}
              className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-sm bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-sky-500 font-medium text-gray-800"
            >
              {stationLocations.length > 0 ? (
                stationLocations.map((st) => (
                  <option key={st.id} value={st.location}>
                    {st.location} ({st.district}, {st.state})
                  </option>
                ))
              ) : (
                <>
                  <option value="Karnal">Karnal (Haryana)</option>
                  <option value="Hisar">Hisar (Haryana)</option>
                  <option value="Ludhiana">Ludhiana (Punjab)</option>
                  <option value="Lucknow">Lucknow (Uttar Pradesh)</option>
                  <option value="Jaipur">Jaipur (Rajasthan)</option>
                  <option value="Shimla">Shimla (Himachal Pradesh)</option>
                  <option value="Dehradun">Dehradun (Uttarakhand)</option>
                  <option value="Delhi">Delhi NCR</option>
                </>
              )}
            </select>
          </div>

          {/* Custom Search Input */}
          <div className="md:col-span-5">
            <label className="block text-xs font-semibold text-gray-700 mb-1.5">
              {isHindi ? 'या दूसरा जिला खोजें' : 'Or Search Other District'}
            </label>
            <div className="relative">
              <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
              <input
                type="text"
                value={customLocation}
                onChange={(e) => setCustomLocation(e.target.value)}
                placeholder={isHindi ? 'उदा. हिसार, आगरा, पटियाला, जोधपुर...' : 'e.g. Hisar, Agra, Patiala...'}
                className="w-full border border-gray-300 rounded-xl pl-10 pr-3.5 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 text-gray-800"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="md:col-span-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-sky-600 hover:bg-sky-700 text-white font-medium py-2.5 px-4 rounded-xl text-sm flex items-center justify-center gap-2 shadow-sm transition-colors disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader className="w-4 h-4 animate-spin" />
                  <span>{isHindi ? 'लोड हो रहा...' : 'Loading...'}</span>
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4" />
                  <span>{isHindi ? 'मौसम देखें' : 'Fetch'}</span>
                </>
              )}
            </button>
          </div>
        </form>

        {/* Quick Location Pills */}
        <div className="mt-4 pt-3 border-t border-gray-100 flex flex-wrap items-center gap-1.5">
          <span className="text-xs font-semibold text-gray-500 mr-1">
            {isHindi ? 'प्रमुख केंद्र:' : 'Key Stations:'}
          </span>
          {quickLocations.map((q) => (
            <button
              key={q.query}
              type="button"
              onClick={() => handleQuickClick(q.query)}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                location.toLowerCase().includes(q.query.toLowerCase())
                  ? 'bg-sky-100 text-sky-800 border border-sky-300'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {q.label}
            </button>
          ))}
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-xl p-4 mb-6 flex items-start gap-2 text-sm">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">{isHindi ? 'डेटा प्राप्त नहीं हो सका' : 'Failed to retrieve weather data'}</p>
            <p className="text-xs mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Main Weather Content */}
      {weatherData && (
        <div className="space-y-6">
          {/* Top Hero Card: Current Conditions */}
          <div className="bg-gradient-to-br from-sky-600 via-sky-700 to-blue-800 rounded-3xl p-6 text-white shadow-md relative overflow-hidden">
            <div className="absolute right-4 -bottom-6 opacity-10 pointer-events-none">
              <SunMedium className="w-64 h-64" />
            </div>

            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="bg-white/20 backdrop-blur-sm text-white px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {weatherData.state}
                  </span>
                  <span className="bg-amber-400 text-amber-950 px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider">
                    {weatherData.data_type}
                  </span>
                </div>
                <h2 className="text-3xl font-extrabold mt-2 flex items-baseline gap-2">
                  {weatherData.location}
                  {weatherData.district && weatherData.district !== weatherData.location && (
                    <span className="text-sm font-normal text-sky-200">({weatherData.district})</span>
                  )}
                </h2>
                <p className="text-sky-100 text-base mt-1 font-medium">
                  {isHindi ? weatherData.condition_hi : weatherData.condition}
                </p>
              </div>

              {/* Large Temperature Display */}
              <div className="text-left sm:text-right">
                <div className="text-5xl sm:text-6xl font-black tracking-tight">
                  {weatherData.temperature}°<span className="text-3xl font-light">C</span>
                </div>
                <p className="text-xs text-sky-200 mt-1">
                  {isHindi ? 'महसूस होता है:' : 'Feels like:'} {weatherData.feels_like}°C
                </p>
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-white/15 text-sm">
              <div className="flex items-center gap-2.5 bg-white/10 rounded-xl p-3">
                <Droplets className="w-5 h-5 text-sky-300 flex-shrink-0" />
                <div>
                  <p className="text-xs text-sky-200">{isHindi ? 'आर्द्रता (नमी)' : 'Humidity'}</p>
                  <p className="font-bold text-base">{weatherData.humidity}%</p>
                </div>
              </div>

              <div className="flex items-center gap-2.5 bg-white/10 rounded-xl p-3">
                <Wind className="w-5 h-5 text-sky-300 flex-shrink-0" />
                <div>
                  <p className="text-xs text-sky-200">{isHindi ? 'हवा की गति' : 'Wind Speed'}</p>
                  <p className="font-bold text-base">
                    {weatherData.wind_speed} <span className="text-xs font-normal">km/h</span>
                    {weatherData.wind_direction && (
                      <span className="ml-1 text-xs text-sky-200">({weatherData.wind_direction})</span>
                    )}
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2.5 bg-white/10 rounded-xl p-3">
                <Cloud className="w-5 h-5 text-sky-300 flex-shrink-0" />
                <div>
                  <p className="text-xs text-sky-200">{isHindi ? 'बारिश की संभावना' : 'Rain Prob.'}</p>
                  <p className="font-bold text-base">{weatherData.rainfall_prob}%</p>
                </div>
              </div>

              <div className="flex items-center gap-2.5 bg-white/10 rounded-xl p-3">
                <Eye className="w-5 h-5 text-sky-300 flex-shrink-0" />
                <div>
                  <p className="text-xs text-sky-200">{isHindi ? 'दृश्यता' : 'Visibility'}</p>
                  <p className="font-bold text-base">{weatherData.visibility_km ?? 8} km</p>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-white/10 flex flex-wrap items-center justify-between gap-2 text-[11px] text-sky-200">
              <span>📡 {weatherData.data_source}</span>
              <span>
                {isHindi ? 'निरीक्षण तिथि:' : 'Date:'} {weatherData.observation_date}
              </span>
            </div>
          </div>

          {/* 3 Specialized Agromet Farm Advisories */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Sprout className="w-5 h-5 text-emerald-600" />
              <h3 className="text-lg font-bold text-gray-900">
                {isHindi ? 'कृषि कार्य सलाह (Agromet Advisory)' : 'Agromet Farming Advisories'}
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* 1. Spray Advisory */}
              <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500">
                      {isHindi ? 'स्प्रे व कीटनाशक' : 'Pest/Foliar Spray'}
                    </span>
                    <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${sprayBadge.bg}`}>
                      {sprayBadge.text}
                    </span>
                  </div>
                  <h4 className="font-bold text-gray-900 text-sm mb-2">
                    {isHindi ? 'छिड़काव अनुकूलता' : 'Spray Feasibility'}
                  </h4>
                  <p className="text-xs text-gray-700 leading-relaxed">
                    {isHindi ? spray.message_hi : spray.message}
                  </p>

                  {spray.recommendation_hi && (
                    <div className="mt-3 bg-emerald-50 text-emerald-900 border border-emerald-100 rounded-xl p-2.5 text-xs">
                      <span className="font-semibold">{isHindi ? 'सिफारिश: ' : 'Tip: '}</span>
                      {spray.recommendation_hi}
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-gray-100 text-[11px] text-gray-500 flex justify-between">
                  <span>हवा: {weatherData.wind_speed} km/h</span>
                  <span>बारिश: {weatherData.rainfall_prob}%</span>
                </div>
              </div>

              {/* 2. Irrigation Advisory */}
              <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500">
                      {isHindi ? 'सिंचाई प्रबंधन' : 'Irrigation Need'}
                    </span>
                    <span
                      className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${
                        irrigation.needed
                          ? 'bg-blue-50 text-blue-800 border-blue-200'
                          : 'bg-gray-100 text-gray-800 border-gray-200'
                      }`}
                    >
                      {irrigation.needed
                        ? (isHindi ? '💧 सिंचाई अनुशंसित' : '💧 Irrigation Advised')
                        : (isHindi ? 'नमी पर्याप्त' : 'Moisture OK')}
                    </span>
                  </div>
                  <h4 className="font-bold text-gray-900 text-sm mb-2">
                    {isHindi ? 'खेत में नमी की स्थिति' : 'Soil Moisture Status'}
                  </h4>
                  <p className="text-xs text-gray-700 leading-relaxed">
                    {irrigation.message_hi}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-gray-100 text-[11px] text-gray-500">
                  {irrigation.disclaimer_hi}
                </div>
              </div>

              {/* 3. Harvest Advisory */}
              <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500">
                      {isHindi ? 'कटाई व गहाई' : 'Harvest & Threshing'}
                    </span>
                    <span
                      className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${
                        harvest.safe
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          : 'bg-amber-50 text-amber-800 border-amber-200'
                      }`}
                    >
                      {harvest.safe
                        ? (isHindi ? '🌾 कटाई सुरक्षित' : '🌾 Harvest Safe')
                        : (isHindi ? '⚠️ सावधानी रखें' : '⚠️ Use Caution')}
                    </span>
                  </div>
                  <h4 className="font-bold text-gray-900 text-sm mb-2">
                    {isHindi ? 'फसल कटाई सुरक्षा' : 'Harvesting Conditions'}
                  </h4>
                  <p className="text-xs text-gray-700 leading-relaxed">
                    {harvest.message_hi}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-gray-100 text-[11px] text-gray-500">
                  {harvest.disclaimer_hi}
                </div>
              </div>
            </div>
          </div>

          {/* 5-Day Forecast Strip */}
          {forecast.length > 0 && (
            <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-sky-600" />
                  <h3 className="text-base font-bold text-gray-900">
                    {isHindi ? '5-दिवसीय मौसम पूर्वानुमान' : '5-Day Benchmark Forecast'}
                  </h3>
                </div>
                <span className="text-xs text-gray-400 font-mono">sample model</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                {forecast.map((day, idx) => (
                  <div
                    key={idx}
                    className={`rounded-xl p-3.5 text-center border transition-all ${
                      idx === 0
                        ? 'bg-sky-50 border-sky-200 shadow-sm'
                        : 'bg-gray-50 border-gray-200 hover:bg-gray-100/80'
                    }`}
                  >
                    <p className="text-xs font-bold text-gray-700">
                      {isHindi ? day.day_hi : day.day}
                    </p>
                    <p className="text-xs text-sky-600 font-medium mt-1 truncate">
                      {isHindi ? day.condition_hi : day.condition}
                    </p>

                    <div className="my-2">
                      <p className="text-xl font-extrabold text-gray-900">
                        {day.temp_max}°
                      </p>
                      <p className="text-xs text-gray-500 font-medium">
                        {isHindi ? 'न्यूनतम: ' : 'Min: '}{day.temp_min}°
                      </p>
                    </div>

                    <div className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-700 bg-blue-100/60 px-2 py-0.5 rounded-full">
                      <Droplets className="w-3 h-3" />
                      <span>{day.rain_probability}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Agromet Indicators Reference Bar */}
          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
              {isHindi ? 'IMD एग्रोमेट मानक सूचकांक (Agromet Reference Standards)' : 'IMD Agromet Standards'}
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs text-slate-600">
              <div className="p-3 bg-white rounded-xl border border-slate-200">
                <p className="font-semibold text-slate-900 mb-1">
                  {isHindi ? 'हवा गति सीमा (Wind Speed):' : 'Wind Speed Threshold:'}
                </p>
                <p>{isHindi ? '• < 10 km/h: कीटनाशक स्प्रे के लिए सुरक्षित' : '• < 10 km/h: Safe for pesticide spray'}</p>
                <p>{isHindi ? '• > 15 km/h: छिड़काव स्थगित करें (हवा से बहाव)' : '• > 15 km/h: Postpone spray (drift risk)'}</p>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200">
                <p className="font-semibold text-slate-900 mb-1">
                  {isHindi ? 'आर्द्रता सीमा (Relative Humidity):' : 'Humidity Threshold:'}
                </p>
                <p>{isHindi ? '• > 80%: फफूंद (Fungus) रोग का खतरा' : '• > 80%: High fungal disease risk'}</p>
                <p>{isHindi ? '• < 40%: अधिक वाष्पीकरण, हल्की सिंचाई आवश्यक' : '• < 40%: High ET, light irrigation needed'}</p>
              </div>

              <div className="p-3 bg-white rounded-xl border border-slate-200">
                <p className="font-semibold text-slate-900 mb-1">
                  {isHindi ? 'सहायता व आधिकारिक सलाह:' : 'Helpline & Official Advisory:'}
                </p>
                <p>{isHindi ? '• किसान कॉल सेंटर: 1800-180-1551 (टोल-फ्री)' : '• Kisan Call Center: 1800-180-1551'}</p>
                <p>{isHindi ? '• ब्लॉक-स्तरीय सलाह: मेघदूत मोबाइल ऐप' : '• Block-level advice: Meghdoot App'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
