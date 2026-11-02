import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Mic, Wheat, FileText, TrendingUp, Cloud, History,
  CheckCircle, AlertCircle, Loader, Leaf, ArrowRight,
} from 'lucide-react'
import { useApp } from '../context/AppContext'

const FEATURE_CARDS = [
  {
    to: '/assistant',
    icon: Mic,
    color: 'green',
    titleHi: 'AI वॉइस सहायक',
    titleEn: 'AI Voice Assistant',
    descHi: 'हिंदी में बोलकर खेती से जुड़े सवाल पूछें और सुनने योग्य जवाब पाएं।',
    descEn: 'Ask farming questions in Hindi by voice and get answers you can listen to.',
    badge: '⭐ मुख्य फीचर',
  },
  {
    to: '/crop-advisory',
    icon: Wheat,
    color: 'yellow',
    titleHi: 'फसल सलाह',
    titleEn: 'Crop Advisory',
    descHi: 'बुवाई, सिंचाई, कीट-रोग प्रबंधन और फसल चयन की विश्वसनीय जानकारी।',
    descEn: 'Reliable guidance on sowing, irrigation, pest management and crop selection.',
  },
  {
    to: '/schemes',
    icon: FileText,
    color: 'blue',
    titleHi: 'सरकारी योजनाएं',
    titleEn: 'Government Schemes',
    descHi: 'PM-KISAN, PMFBY और अन्य सरकारी कृषि योजनाओं की पूरी जानकारी।',
    descEn: 'Complete information on PM-KISAN, PMFBY and other agricultural schemes.',
  },
  {
    to: '/mandi',
    icon: TrendingUp,
    color: 'orange',
    titleHi: 'मंडी भाव',
    titleEn: 'Mandi Prices',
    descHi: 'फसलों के बाज़ार भाव जानें। डेटा स्रोत और अंतिम अपडेट समय सहित।',
    descEn: 'Know crop market prices with data source and last update time.',
  },
  {
    to: '/weather',
    icon: Cloud,
    color: 'sky',
    titleHi: 'मौसम जानकारी',
    titleEn: 'Weather Information',
    descHi: 'अपने क्षेत्र का मौसम और खेती से जुड़ी मौसम सलाह पाएं।',
    descEn: 'Get local weather and farming-related weather advisories.',
  },
  {
    to: '/history',
    icon: History,
    color: 'purple',
    titleHi: 'बातचीत इतिहास',
    titleEn: 'Conversation History',
    descHi: 'पिछली बातचीत देखें, सवाल और जवाब दोबारा पढ़ें।',
    descEn: 'View previous conversations and re-read questions and answers.',
  },
]

const colorMap = {
  green:  { bg: 'bg-green-50',  icon: 'text-green-600',  border: 'border-green-200',  btn: 'bg-green-600 hover:bg-green-700' },
  yellow: { bg: 'bg-yellow-50', icon: 'text-yellow-600', border: 'border-yellow-200', btn: 'bg-yellow-600 hover:bg-yellow-700' },
  blue:   { bg: 'bg-blue-50',   icon: 'text-blue-600',   border: 'border-blue-200',   btn: 'bg-blue-600 hover:bg-blue-700' },
  orange: { bg: 'bg-orange-50', icon: 'text-orange-600', border: 'border-orange-200', btn: 'bg-orange-600 hover:bg-orange-700' },
  sky:    { bg: 'bg-sky-50',    icon: 'text-sky-600',    border: 'border-sky-200',    btn: 'bg-sky-600 hover:bg-sky-700' },
  purple: { bg: 'bg-purple-50', icon: 'text-purple-600', border: 'border-purple-200', btn: 'bg-purple-600 hover:bg-purple-700' },
}

function HealthBadge({ health, healthLoading, healthError }) {
  if (healthLoading) {
    return (
      <span className="inline-flex items-center gap-1.5 bg-yellow-100 text-yellow-700 text-xs px-3 py-1 rounded-full">
        <Loader className="w-3 h-3 animate-spin" /> जांच हो रही है…
      </span>
    )
  }
  if (healthError || !health) {
    return (
      <span className="inline-flex items-center gap-1.5 bg-red-100 text-red-700 text-xs px-3 py-1 rounded-full">
        <AlertCircle className="w-3 h-3" /> बैकएंड ऑफलाइन
      </span>
    )
  }
  return (
    <span className="inline-flex items-center gap-1.5 bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full">
      <CheckCircle className="w-3 h-3" />
      सर्वर ऑनलाइन · {health.records_count || 0} रिकॉर्ड
    </span>
  )
}

export default function HomePage() {
  const { language, health, healthLoading, healthError } = useApp()
  const isHindi = language === 'hi'

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Hero */}
      <div className="text-center mb-10">
        <div className="flex justify-center mb-4">
          <div className="bg-green-100 rounded-full p-4">
            <Leaf className="w-12 h-12 text-green-600" />
          </div>
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-800 mb-2">
          {isHindi ? 'किसानवाणी AI में आपका स्वागत है' : 'Welcome to KisanVaani AI'}
        </h1>
        <p className="text-lg text-green-700 font-medium mb-4">
          अपनी भाषा, अपनी खेती, Smart Faisle.
        </p>
        <p className="text-gray-500 max-w-xl mx-auto text-sm">
          {isHindi
            ? 'भारतीय किसानों के लिए एक वॉइस-फर्स्ट AI कृषि सहायक। हिंदी में बोलें और सटीक जानकारी पाएं।'
            : 'A voice-first AI agricultural assistant for Indian farmers. Speak in Hindi and get accurate information.'}
        </p>
        <div className="mt-4 flex justify-center gap-3 flex-wrap">
          <HealthBadge health={health} healthLoading={healthLoading} healthError={healthError} />
          {health?.knowledge_base_loaded && (
            <span className="inline-flex items-center gap-1.5 bg-blue-100 text-blue-700 text-xs px-3 py-1 rounded-full">
              <CheckCircle className="w-3 h-3" />
              {isHindi ? 'ज्ञान आधार लोड' : 'Knowledge Base Loaded'}
            </span>
          )}
        </div>
      </div>

      {/* Quick start CTA */}
      <div className="bg-green-700 rounded-xl p-6 mb-8 text-white text-center">
        <Mic className="w-10 h-10 mx-auto mb-3 text-yellow-300" />
        <h2 className="text-xl font-bold mb-2">
          {isHindi ? 'अभी शुरू करें' : 'Get Started Now'}
        </h2>
        <p className="text-green-200 text-sm mb-4">
          {isHindi
            ? 'माइक्रोफोन बटन दबाएं और अपना सवाल हिंदी में पूछें।'
            : 'Press the microphone button and ask your question in Hindi.'}
        </p>
        <Link
          to="/assistant"
          className="inline-flex items-center gap-2 bg-white text-green-700 font-semibold px-6 py-2.5 rounded-lg hover:bg-green-50 transition-colors"
        >
          <Mic className="w-5 h-5" />
          {isHindi ? 'AI सहायक खोलें' : 'Open AI Assistant'}
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Feature grid */}
      <h2 className="text-xl font-bold text-gray-700 mb-4">
        {isHindi ? 'सभी सुविधाएं' : 'All Features'}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {FEATURE_CARDS.map(({ to, icon: Icon, color, titleHi, titleEn, descHi, descEn, badge }) => {
          const c = colorMap[color]
          return (
            <Link
              key={to}
              to={to}
              className={`block rounded-xl border ${c.border} ${c.bg} p-5 hover:shadow-md transition-shadow group`}
            >
              <div className="flex items-start gap-3 mb-3">
                <div className={`p-2 rounded-lg bg-white border ${c.border}`}>
                  <Icon className={`w-5 h-5 ${c.icon}`} />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-800 text-sm">
                    {isHindi ? titleHi : titleEn}
                  </h3>
                  {badge && (
                    <span className="text-xs text-green-600 font-medium">{badge}</span>
                  )}
                </div>
                <ArrowRight className={`w-4 h-4 ${c.icon} opacity-0 group-hover:opacity-100 transition-opacity mt-1`} />
              </div>
              <p className="text-xs text-gray-500 leading-relaxed">
                {isHindi ? descHi : descEn}
              </p>
            </Link>
          )
        })}
      </div>

      {/* Target regions */}
      <div className="mt-8 bg-white border border-gray-200 rounded-xl p-5">
        <h3 className="font-semibold text-gray-700 mb-3">
          {isHindi ? 'सेवा क्षेत्र' : 'Service Regions'}
        </h3>
        <div className="flex flex-wrap gap-2">
          {['हरियाणा', 'पंजाब', 'उत्तर प्रदेश', 'राजस्थान', 'हिमाचल प्रदेश', 'उत्तराखंड', 'दिल्ली NCR'].map(r => (
            <span key={r} className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full font-medium">
              {r}
            </span>
          ))}
        </div>
        <p className="text-xs text-gray-400 mt-3">
          {isHindi
            ? '⚠️ किसानवाणी AI कृषि जानकारी का एक सहायक स्रोत है। महत्वपूर्ण निर्णयों के लिए कृपया स्थानीय कृषि विशेषज्ञ या KVK से संपर्क करें।'
            : '⚠️ KisanVaani AI is a supplementary source of agricultural information. For critical decisions, please contact your local agricultural expert or KVK.'}
        </p>
      </div>
    </div>
  )
}

