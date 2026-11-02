import React, { useState, useEffect } from 'react'
import {
  Wheat, Loader, AlertCircle, Search, BookOpen, Sparkles,
  CheckCircle2, PhoneCall, ShieldAlert, Calendar, MapPin
} from 'lucide-react'
import { useApp } from '../context/AppContext'
import { getCropRecommendation, getDistricts, getSeedVarieties, getGlossary } from '../services/api'

const STATES = ['हरियाणा', 'पंजाब', 'उत्तर प्रदेश', 'राजस्थान', 'हिमाचल प्रदेश', 'उत्तराखंड', 'दिल्ली NCR']
const CROPS  = ['गेहूं', 'धान / चावल', 'बाजरा', 'मक्का', 'सरसों', 'गन्ना', 'कपास', 'चना', 'मसूर', 'आलू', 'प्याज', 'टमाटर']
const SEASONS = ['रबी (अक्टूबर–मार्च)', 'खरीफ (जून–अक्टूबर)', 'जायद (मार्च–जून)']
const TOPICS = [
  { id: 'sowing', labelHi: 'बुवाई का समय', labelEn: 'Sowing Time' },
  { id: 'seed_varieties', labelHi: 'प्रमाणित बीज किस्में', labelEn: 'Seed Varieties' },
  { id: 'soil_management', labelHi: 'खेत की तैयारी व मिट्टी', labelEn: 'Soil Preparation' },
  { id: 'irrigation', labelHi: 'सिंचाई प्रबंधन', labelEn: 'Irrigation' },
  { id: 'fertilizer', labelHi: 'उर्वरक व खाद', labelEn: 'Fertilizer' },
  { id: 'pest_disease', labelHi: 'कीट व रोग (IPM)', labelEn: 'Pests & Diseases (IPM)' },
  { id: 'harvesting', labelHi: 'कटाई व भंडारण', labelEn: 'Harvesting & Storage' },
]

export default function CropAdvisoryPage() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  const [activeTab, setActiveTab] = useState('advisory') // advisory | seeds | glossary
  const [form, setForm] = useState({ state: '', district: '', crop: '', season: '', topic: 'sowing' })
  const [districtsList, setDistrictsList] = useState([])
  const [districtsLoading, setDistrictsLoading] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [advice, setAdvice] = useState(null)

  // Seeds & Glossary State
  const [seedList, setSeedList] = useState([])
  const [seedLoading, setSeedLoading] = useState(false)
  const [glossaryList, setGlossaryList] = useState([])
  const [glossarySearch, setGlossarySearch] = useState('')

  useEffect(() => {
    // Load certified seed varieties
    setSeedLoading(true)
    getSeedVarieties()
      .then(res => setSeedList(res.varieties || []))
      .catch(() => {})
      .finally(() => setSeedLoading(false))

    // Load glossary
    getGlossary()
      .then(res => setGlossaryList(res.terms || []))
      .catch(() => {})
  }, [])

  // When state changes, dynamically load official districts
  useEffect(() => {
    if (!form.state) {
      setDistrictsList([])
      setForm(prev => ({ ...prev, district: '' }))
      return
    }
    setDistrictsLoading(true)
    getDistricts(form.state)
      .then(res => {
        setDistrictsList(res.districts || [])
      })
      .catch(() => {
        setDistrictsList([])
      })
      .finally(() => setDistrictsLoading(false))
  }, [form.state])

  const handleChange = (field, value) => setForm(prev => ({ ...prev, [field]: value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.crop) { setError(isHindi ? 'कृपया फसल चुनें।' : 'Please select a crop.'); return }
    setError(null)
    setLoading(true)
    setAdvice(null)

    try {
      const data = await getCropRecommendation({
        crop: form.crop,
        state: form.state || null,
        district: form.district || null,
        season: form.season || null,
        topic: form.topic || 'sowing'
      })
      setAdvice(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const filteredGlossary = glossaryList.filter(item => {
    if (!glossarySearch.trim()) return true
    const q = glossarySearch.toLowerCase()
    const hi = (item.term?.hi || '').toLowerCase()
    const en = (item.term?.en || '').toLowerCase()
    return hi.includes(q) || en.includes(q)
  })

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2.5 bg-yellow-100 rounded-xl text-yellow-700">
          <Wheat className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
            {isHindi ? 'स्मार्ट फसल सलाह व कृषि ज्ञान' : 'Smart Crop Advisory & Knowledge'}
          </h1>
          <p className="text-xs sm:text-sm text-gray-500">
            {isHindi
              ? 'विश्वविद्यालय प्रमाणित बुवाई, किस्में, सिंचाई और एकीकृत कीट प्रबंधन (IPM)'
              : 'University verified sowing periods, seed varieties, irrigation and IPM'}
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-6 gap-2">
        <button
          onClick={() => setActiveTab('advisory')}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === 'advisory'
              ? 'border-green-600 text-green-700'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <Wheat className="w-4 h-4" />
          <span>{isHindi ? 'फसल सलाह' : 'Crop Advisory'}</span>
        </button>
        <button
          onClick={() => setActiveTab('seeds')}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === 'seeds'
              ? 'border-green-600 text-green-700'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <Sparkles className="w-4 h-4" />
          <span>{isHindi ? 'प्रमाणित बीज किस्में' : 'Seed Varieties'}</span>
        </button>
        <button
          onClick={() => setActiveTab('glossary')}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === 'glossary'
              ? 'border-green-600 text-green-700'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>{isHindi ? 'कृषि शब्दावली' : 'Agricultural Glossary'}</span>
        </button>
      </div>

      {/* TAB 1: ADVISORY FORM */}
      {activeTab === 'advisory' && (
        <>
          {/* Important Farmer Safety Disclaimer Banner */}
          <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 mb-6 text-xs text-amber-800 flex items-start gap-3 shadow-sm">
            <ShieldAlert className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="leading-relaxed">
              <span className="font-bold">{isHindi ? 'किसान सुरक्षा दिशानिर्देश:' : 'Farmer Safety Principles:'}</span>{' '}
              {isHindi
                ? 'कीटनाशक व खाद की कोई भी मात्रा बिना मिट्टी जांच या कृषि विश्वविद्यालय के सत्यापित पैकेज के लागू न करें। किसानवाणी AI कभी भी अप्रमाणित रसायनों की खुराक नहीं बताता।'
                : 'Never apply unverified pesticide or fertilizer doses. KisanVaani AI provides only grounded, university-verified guidelines and directs to local KVKs for specific chemical prescriptions.'}
            </div>
          </div>

          {/* Form Card */}
          <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-2xl p-5 sm:p-6 shadow-sm mb-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-5">
              {/* State */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                  {isHindi ? 'राज्य (State)' : 'State'}
                </label>
                <select
                  value={form.state}
                  onChange={e => handleChange('state', e.target.value)}
                  className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-white"
                >
                  <option value="">{isHindi ? '-- राज्य चुनें --' : '-- Select State --'}</option>
                  {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              {/* District */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5 flex items-center justify-between">
                  <span>{isHindi ? 'जिला (District)' : 'District'}</span>
                  {districtsLoading && <span className="text-gray-400 font-normal">लोड हो रहा है…</span>}
                </label>
                <select
                  value={form.district}
                  onChange={e => handleChange('district', e.target.value)}
                  disabled={!form.state || districtsList.length === 0}
                  className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-white disabled:bg-gray-100 disabled:opacity-60"
                >
                  <option value="">
                    {form.state
                      ? (isHindi ? '-- जिला चुनें --' : '-- Select District --')
                      : (isHindi ? 'पहले राज्य चुनें' : 'Select state first')}
                  </option>
                  {districtsList.map(d => <option key={d} value={d}>{d}</option>)}
                </select>
              </div>

              {/* Crop */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                  {isHindi ? 'फसल (Crop) *' : 'Crop *'}
                </label>
                <select
                  value={form.crop}
                  onChange={e => handleChange('crop', e.target.value)}
                  required
                  className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-white"
                >
                  <option value="">{isHindi ? '-- फसल चुनें --' : '-- Select Crop --'}</option>
                  {CROPS.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>

              {/* Season */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                  {isHindi ? 'मौसम (Season)' : 'Season'}
                </label>
                <select
                  value={form.season}
                  onChange={e => handleChange('season', e.target.value)}
                  className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-white"
                >
                  <option value="">{isHindi ? '-- मौसम चुनें --' : '-- Select Season --'}</option>
                  {SEASONS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              {/* Topic */}
              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                  {isHindi ? 'कृषि विषय (Topic of Advice)' : 'Topic'}
                </label>
                <select
                  value={form.topic}
                  onChange={e => handleChange('topic', e.target.value)}
                  className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 bg-white"
                >
                  {TOPICS.map(t => (
                    <option key={t.id} value={t.id}>
                      {isHindi ? t.labelHi : t.labelEn}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {error && (
              <p className="text-xs text-red-600 mb-3 flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4" /> {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading || !form.crop}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-xl text-sm flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow transition-colors"
            >
              {loading ? (
                <><Loader className="w-4 h-4 animate-spin" /> {isHindi ? 'सत्यापित कृषि जानकारी ला रहे हैं…' : 'Retrieving guidance…'}</>
              ) : (
                <><Search className="w-4 h-4" /> {isHindi ? 'सत्यापित फसल सलाह देखें' : 'Get Verified Advisory'}</>
              )}
            </button>
          </form>

          {/* Advice Output Card */}
          {advice && (
            <div className="bg-white border border-green-200 rounded-2xl p-6 shadow-sm mb-6 space-y-5">
              {/* Card Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-gray-100">
                <div>
                  <h2 className="font-bold text-gray-900 text-lg flex items-center gap-2">
                    <CheckCircle2 className="w-5 h-5 text-green-600" />
                    <span>{advice.title}</span>
                  </h2>
                  <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500 mt-1">
                    <span className="font-medium text-gray-700">{advice.crop}</span>
                    {advice.state && <span>• {advice.state}</span>}
                    {advice.district && <span>• {advice.district}</span>}
                    {advice.season && <span>• {advice.season}</span>}
                  </div>
                </div>

                <span className={`text-xs px-2.5 py-1 rounded-full font-medium self-start sm:self-auto ${
                  advice.verification_status === 'verified'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {advice.verification_status === 'verified' ? '✓ सत्यापित (Verified)' : 'समीक्षाधीन (Review)'}
                </span>
              </div>

              {/* Advisory Text */}
              <div className="text-sm sm:text-base text-gray-800 leading-relaxed whitespace-pre-wrap bg-green-50/50 p-4 rounded-xl border border-green-100">
                {advice.advisory_hi}
              </div>

              {/* Verified Key Parameters */}
              {advice.verified_guidance && Object.keys(advice.verified_guidance).length > 0 && (
                <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                  <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2.5">
                    📋 {isHindi ? 'मुख्य सत्यापित बिंदु:' : 'Key Verified Guidance:'}
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    {Object.entries(advice.verified_guidance).map(([k, v]) => (
                      <div key={k} className="bg-white p-2.5 rounded-lg border border-gray-200">
                        <span className="font-semibold text-gray-700 block capitalize">
                          {k.replace(/_/g, ' ')}:
                        </span>
                        <span className="text-gray-600 mt-0.5 block">
                          {Array.isArray(v) ? v.join(', ') : String(v)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Safety Disclaimer */}
              {advice.safety_disclaimer && (
                <div className="text-xs text-amber-700 bg-amber-50 border border-amber-100 p-3 rounded-xl flex items-start gap-2">
                  <span className="font-bold">⚠️</span>
                  <span>{advice.safety_disclaimer}</span>
                </div>
              )}

              {/* Direct KVK Referral Box */}
              {advice.kvk_referral && (
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-blue-900">
                  <div className="space-y-1">
                    <p className="font-bold flex items-center gap-1.5 text-blue-800 text-sm">
                      <PhoneCall className="w-4 h-4 text-blue-600" />
                      {advice.kvk_referral.helpline_name}
                    </p>
                    <p className="text-blue-700">{advice.kvk_referral.advice}</p>
                    <p className="text-blue-500">{advice.kvk_referral.hours}</p>
                  </div>
                  <a
                    href={`tel:${advice.kvk_referral.toll_free}`}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded-xl text-center flex-shrink-0 transition-colors inline-block"
                  >
                    📞 {advice.kvk_referral.toll_free}
                  </a>
                </div>
              )}

              {/* Sources Attribution */}
              {advice.sources && advice.sources.length > 0 && (
                <div className="pt-3 border-t border-gray-100 flex flex-wrap items-center gap-2 text-xs text-gray-500">
                  <span className="font-semibold text-gray-600">📚 {isHindi ? 'सत्यापित स्रोत:' : 'Sources:'}</span>
                  {advice.sources.map((s, idx) => (
                    <span key={idx} className="bg-gray-100 text-gray-700 px-2.5 py-0.5 rounded font-mono">
                      {s}
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}
        </>
      )}

      {/* TAB 2: CERTIFIED SEED VARIETIES */}
      {activeTab === 'seeds' && (
        <div className="space-y-4">
          <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
            <h2 className="font-bold text-gray-800 mb-1 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-yellow-500" />
              {isHindi ? 'विश्वविद्यालय अनुशंसित बीज किस्में' : 'Recommended Seed Varieties'}
            </h2>
            <p className="text-xs text-gray-500 mb-4">
              {isHindi
                ? 'कृषि विश्वविद्यालयों (HAU, PAU, IARI) द्वारा अनुशंसित प्रमुख प्रमाणित किस्में।'
                : 'Key certified varieties recommended by agricultural universities.'}
            </p>

            {seedLoading ? (
              <div className="py-8 flex justify-center"><Loader className="w-6 h-6 animate-spin text-green-600" /></div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {seedList.map((seed, idx) => (
                  <div key={idx} className="border border-gray-200 rounded-xl p-3.5 hover:border-green-300 transition-colors bg-gray-50">
                    <div className="flex items-start justify-between">
                      <span className="font-bold text-gray-800 text-sm">{seed.variety}</span>
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded font-medium">
                        {seed.crop_id?.toUpperCase()}
                      </span>
                    </div>
                    {seed.sowing_condition && (
                      <p className="text-xs text-gray-600 mt-1.5">
                        <span className="font-semibold">{isHindi ? 'स्थिति:' : 'Condition:'}</span> {seed.sowing_condition}
                      </p>
                    )}
                    {seed.state && (
                      <p className="text-xs text-gray-500 mt-0.5">
                        <span className="font-semibold">{isHindi ? 'राज्य:' : 'State:'}</span> {seed.state}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: AGRICULTURAL GLOSSARY */}
      {activeTab === 'glossary' && (
        <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="font-bold text-gray-800 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-600" />
                {isHindi ? 'कृषि शब्दावली व परिभाषाएं' : 'Agricultural Terms & Glossary'}
              </h2>
              <p className="text-xs text-gray-500">
                {isHindi ? 'खेती-बाड़ी से जुड़े जरूरी शब्दों के सरल अर्थ' : 'Simple explanations of farming terms'}
              </p>
            </div>
            <input
              type="text"
              value={glossarySearch}
              onChange={e => setGlossarySearch(e.target.value)}
              placeholder={isHindi ? 'शब्द खोजें…' : 'Search term…'}
              className="border border-gray-300 rounded-xl px-3 py-1.5 text-xs focus:ring-2 focus:ring-green-500 outline-none w-full sm:w-48"
            />
          </div>

          <div className="divide-y divide-gray-100">
            {filteredGlossary.map((item, idx) => (
              <div key={idx} className="py-3">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-green-800 text-sm">
                    {item.term?.hi}
                  </span>
                  {item.term?.en && (
                    <span className="text-xs text-gray-500 font-mono">
                      ({item.term?.en})
                    </span>
                  )}
                  {item.kind && (
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded ml-auto">
                      {item.kind}
                    </span>
                  )}
                </div>
                {item.notes && (
                  <p className="text-xs text-gray-600 mt-1 leading-relaxed">
                    {item.notes}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
