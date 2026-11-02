import React, { useEffect, useState } from 'react'
import {
  FileText, Loader, AlertCircle, ExternalLink, ChevronDown, ChevronUp,
  Search, PhoneCall, ShieldAlert, CheckCircle2, XCircle, Info, Landmark
} from 'lucide-react'
import { useApp } from '../context/AppContext'
import { getSchemes } from '../services/api'

const CATEGORIES = [
  { id: 'all', labelHi: 'सभी योजनाएं', labelEn: 'All Schemes' },
  { id: 'financial_support', labelHi: 'वित्तीय सहायता (PM-KISAN)', labelEn: 'Income Support' },
  { id: 'crop_insurance', labelHi: 'फसल बीमा (PMFBY)', labelEn: 'Crop Insurance' },
  { id: 'irrigation', labelHi: 'सिंचाई अनुदान (PMKSY)', labelEn: 'Irrigation' },
  { id: 'soil_health', labelHi: 'मृदा स्वास्थ्य (Soil Health)', labelEn: 'Soil Health' },
  { id: 'farm_machinery', labelHi: 'कृषि मशीनरी (SMAM)', labelEn: 'Farm Machinery' },
]

function SchemeCard({ scheme, isHindi, onExpand, expanded }) {
  const nameObj = typeof scheme.name === 'object' && scheme.name !== null ? scheme.name : { hi: scheme.name, en: scheme.name }
  const title = isHindi ? (nameObj.hi || nameObj.en) : (nameObj.en || nameObj.hi)
  const subtitle = isHindi ? nameObj.en : nameObj.hi

  const purposeObj = typeof scheme.purpose === 'object' && scheme.purpose !== null ? scheme.purpose : { hi: scheme.purpose, en: scheme.purpose }
  const purposeText = isHindi ? (purposeObj.hi || purposeObj.en) : (purposeObj.en || purposeObj.hi)

  const benefitsObj = typeof scheme.benefits === 'object' && scheme.benefits !== null ? scheme.benefits : { hi: scheme.benefits, en: scheme.benefits }
  const benefitsText = isHindi ? (benefitsObj.hi || benefitsObj.en) : (benefitsObj.en || benefitsObj.hi)

  const eligObj = typeof scheme.eligibility === 'object' && scheme.eligibility !== null ? scheme.eligibility : { hi: scheme.eligibility, en: scheme.eligibility }
  const eligText = isHindi ? (eligObj.hi || eligObj.en) : (eligObj.en || eligObj.hi)

  const applyObj = typeof scheme.application_process === 'object' && scheme.application_process !== null ? scheme.application_process : { hi: scheme.application_process, en: scheme.application_process }
  const applyText = isHindi ? (applyObj.hi || applyObj.en) : (applyObj.en || applyObj.hi)

  const helpline = scheme.helpline || {}
  const tollFreeNumber = helpline.toll_free || (Array.isArray(helpline.numbers) ? helpline.numbers[0] : null)

  return (
    <div className={`bg-white border rounded-2xl overflow-hidden transition-all shadow-sm ${
      expanded ? 'border-green-400 ring-2 ring-green-50' : 'border-gray-200 hover:border-green-200'
    }`}>
      {/* Header Accordion Click */}
      <button
        onClick={onExpand}
        className="w-full flex items-start gap-4 p-5 hover:bg-gray-50/80 transition-colors text-left"
      >
        <div className="bg-green-100 rounded-xl p-3 flex-shrink-0 text-green-700">
          <Landmark className="w-6 h-6" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-bold text-gray-900 text-base sm:text-lg">
              {title}
            </h3>
            <span className="text-xs bg-green-50 text-green-700 border border-green-200 px-2 py-0.5 rounded-full font-medium">
              {scheme.scope || 'National'}
            </span>
          </div>

          {subtitle && (
            <p className="text-xs text-gray-500 mt-0.5">{subtitle}</p>
          )}

          {purposeText && (
            <p className="text-xs sm:text-sm text-gray-600 mt-2 line-clamp-2 leading-relaxed">
              {purposeText}
            </p>
          )}
        </div>

        <div className="p-2 text-gray-400 hover:text-gray-600 flex-shrink-0">
          {expanded ? <ChevronUp className="w-5 h-5 text-green-600" /> : <ChevronDown className="w-5 h-5" />}
        </div>
      </button>

      {/* Expanded Scheme Details */}
      {expanded && (
        <div className="px-5 pb-6 border-t border-gray-100 bg-white space-y-4 pt-4">
          {/* Benefits Box */}
          {benefitsText && (
            <div className="bg-green-50/70 border border-green-200 rounded-xl p-4">
              <h4 className="text-xs font-bold text-green-800 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-green-600" />
                {isHindi ? '💰 वित्तीय लाभ व सहायता:' : '💰 Financial Benefits:'}
              </h4>
              <p className="text-xs sm:text-sm text-green-900 leading-relaxed font-medium">
                {benefitsText}
              </p>
            </div>
          )}

          {/* Eligibility & Exclusions Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Eligibility */}
            {eligText && (
              <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-blue-600" />
                  {isHindi ? '👤 पात्रता (Eligibility):' : '👤 Eligibility:'}
                </h4>
                <p className="text-xs text-gray-700 leading-relaxed">
                  {eligText}
                </p>
              </div>
            )}

            {/* Exclusions */}
            {scheme.exclusion_criteria && scheme.exclusion_criteria.length > 0 && (
              <div className="bg-red-50/60 border border-red-200 rounded-xl p-4">
                <h4 className="text-xs font-bold text-red-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <XCircle className="w-4 h-4 text-red-600" />
                  {isHindi ? '🚫 अपात्र श्रेणियां (Exclusions):' : '🚫 Exclusions:'}
                </h4>
                <ul className="space-y-1 text-xs text-red-900">
                  {scheme.exclusion_criteria.map((ex, idx) => (
                    <li key={idx} className="flex items-start gap-1.5">
                      <span className="text-red-500 font-bold">•</span>
                      <span>{ex}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Required Documents Checklist */}
          {scheme.required_documents && scheme.required_documents.length > 0 && (
            <div className="bg-white border border-gray-200 rounded-xl p-4">
              <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-gray-600" />
                {isHindi ? '📄 आवश्यक दस्तावेज़ (Required Documents):' : '📄 Required Documents:'}
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                {scheme.required_documents.map((doc, idx) => (
                  <div key={idx} className="bg-gray-50 p-2.5 rounded-lg border border-gray-100 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{doc}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Application Process */}
          {applyText && (
            <div className="bg-blue-50/60 border border-blue-200 rounded-xl p-4">
              <h4 className="text-xs font-bold text-blue-900 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                <Info className="w-4 h-4 text-blue-600" />
                {isHindi ? '📝 आवेदन कैसे करें (Application Process):' : '📝 How to Apply:'}
              </h4>
              <p className="text-xs sm:text-sm text-blue-950 leading-relaxed">
                {applyText}
              </p>
            </div>
          )}

          {/* Action Row: Official Portal + Official Helpline */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-2">
            {/* Official Helpline Button */}
            {tollFreeNumber && (
              <a
                href={`tel:${tollFreeNumber}`}
                className="inline-flex items-center justify-center gap-2 bg-green-700 hover:bg-green-800 text-white font-semibold text-xs px-4 py-2.5 rounded-xl transition-colors shadow-sm"
              >
                <PhoneCall className="w-4 h-4" />
                <span>{isHindi ? 'आधिकारिक हेल्पलाइन:' : 'Helpline:'} {tollFreeNumber}</span>
              </a>
            )}

            {/* Official Portal External Link */}
            {scheme.official_portal && (
              <a
                href={scheme.official_portal}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 bg-white hover:bg-gray-50 text-blue-600 border border-blue-300 font-semibold text-xs px-4 py-2.5 rounded-xl transition-colors"
              >
                <span>{isHindi ? 'आधिकारिक पोर्टल पर जाएं' : 'Visit Official Portal'}</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            )}
          </div>

          {/* Security Notice */}
          <div className="text-xs text-amber-800 bg-amber-50 border border-amber-200 rounded-xl p-3 flex items-start gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
            <span>
              {isHindi
                ? 'किसान सुरक्षा चेतावनी: आधार कार्ड, बैंक खाता या ओटीपी कभी भी किसी अनधिकृत व्यक्ति या फर्जी वेबसाइट पर साझा न करें। केवल आधिकारिक सरकारी पोर्टल (.gov.in / .nic.in) या सीएससी सेंटर का उपयोग करें।'
                : 'Security Warning: Only enter your Aadhaar or bank details on verified official government portals (.gov.in / .nic.in) or at authorized CSC centers.'}
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default function SchemesPage() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  const [schemes, setSchemes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expanded, setExpanded] = useState('pm-kisan')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  const loadSchemes = async (cat = 'all', q = '') => {
    setLoading(true)
    setError(null)
    try {
      const params = {}
      if (cat !== 'all') params.category = cat
      if (q.trim()) params.q = q.trim()
      const data = await getSchemes(params)
      setSchemes(data.schemes || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSchemes(selectedCategory, searchQuery)
  }, [selectedCategory]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleSearchSubmit = (e) => {
    e.preventDefault()
    loadSchemes(selectedCategory, searchQuery)
  }

  const toggleExpand = (id) => setExpanded(prev => prev === id ? null : id)

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Page Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2.5 bg-blue-100 rounded-xl text-blue-700">
          <FileText className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
            {isHindi ? 'सरकारी कृषि योजना नेविगेटर' : 'Government Scheme Navigator'}
          </h1>
          <p className="text-xs sm:text-sm text-gray-500">
            {isHindi
              ? 'PM-KISAN, PMFBY, PMKSY व अन्य केंद्रीय योजनाओं की प्रामाणिक जानकारी'
              : 'Verified guidance on PM-KISAN, PMFBY, PMKSY and agricultural welfare schemes'}
          </p>
        </div>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearchSubmit} className="mb-4">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder={isHindi ? 'योजना का नाम, लाभ अथवा कीवर्ड खोजें (उदा. 6000, बीमा, ड्रिप, ट्रैक्टर)…' : 'Search scheme name, benefit or keyword…'}
              className="w-full pl-10 pr-4 py-2.5 text-sm border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 bg-white"
            />
          </div>
          <button
            type="submit"
            className="bg-green-700 hover:bg-green-800 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors shadow-sm"
          >
            {isHindi ? 'खोजें' : 'Search'}
          </button>
        </div>
      </form>

      {/* Category Pills Filter */}
      <div className="flex gap-2 overflow-x-auto pb-2 mb-6 scrollbar-none">
        {CATEGORIES.map(cat => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            className={`text-xs font-semibold px-3.5 py-1.5 rounded-full whitespace-nowrap transition-colors border ${
              selectedCategory === cat.id
                ? 'bg-green-700 text-white border-green-700'
                : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'
            }`}
          >
            {isHindi ? cat.labelHi : cat.labelEn}
          </button>
        ))}
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center py-16">
          <Loader className="w-8 h-8 text-green-600 animate-spin" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 flex items-center gap-3 text-sm text-red-700 mb-6">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{isHindi ? 'योजनाएं लोड नहीं हो सकीं:' : 'Could not load schemes:'} {error}</span>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && schemes.length === 0 && (
        <div className="text-center text-gray-400 py-16 bg-white border border-gray-200 rounded-2xl">
          <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p className="text-base font-semibold text-gray-600">
            {isHindi ? 'कोई योजना नहीं मिली' : 'No schemes match your criteria'}
          </p>
          <button
            onClick={() => { setSelectedCategory('all'); setSearchQuery(''); loadSchemes('all', '') }}
            className="mt-3 text-xs text-green-700 underline font-medium"
          >
            {isHindi ? 'सभी योजनाएं देखें' : 'View all schemes'}
          </button>
        </div>
      )}

      {/* Schemes List */}
      <div className="space-y-4">
        {schemes.map((scheme, i) => (
          <SchemeCard
            key={scheme.scheme_id || scheme.id || i}
            scheme={scheme}
            isHindi={isHindi}
            expanded={expanded === (scheme.scheme_id || scheme.id)}
            onExpand={() => toggleExpand(scheme.scheme_id || scheme.id)}
          />
        ))}
      </div>

      {/* Bottom Disclaimer */}
      {schemes.length > 0 && (
        <div className="mt-8 bg-gray-50 border border-gray-200 rounded-2xl p-5 text-xs text-gray-500 space-y-1.5">
          <p className="font-bold text-gray-700 flex items-center gap-1.5">
            <Info className="w-4 h-4 text-blue-600" />
            {isHindi ? 'आधिकारिक सरकारी स्रोत प्रकटीकरण:' : 'Official Government Source Disclosure:'}
          </p>
          <p className="leading-relaxed">
            {isHindi
              ? 'किसानवाणी AI पर प्रदर्शित योजना विवरण आधिकारिक सरकारी राजपत्रों, पोर्टल दिशानिर्देशों (pmkisan.gov.in, pmfby.gov.in, pmksy.gov.in) तथा कृषि मंत्रालय की अधिसूचनाओं पर आधारित हैं। हम कभी भी नकली किस्त तिथि या असत्यापित सब्सिडी का दावा नहीं करते।'
              : 'Scheme information displayed on KisanVaani AI is sourced strictly from official government operational guidelines (pmkisan.gov.in, pmfby.gov.in, pmksy.gov.in). Never rely on unofficial announcements.'}
          </p>
        </div>
      )}
    </div>
  )
}
