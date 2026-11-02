import React from 'react'
import { Leaf, Mic, Shield, Database, Globe, AlertTriangle, CheckCircle } from 'lucide-react'
import { useApp } from '../context/AppContext'

const DATA_SOURCES = [
  { name: 'ICAR (भारतीय कृषि अनुसंधान परिषद)', type: 'official_static' },
  { name: 'कृषि एवं किसान कल्याण मंत्रालय', type: 'official_static' },
  { name: 'PM-KISAN आधिकारिक पोर्टल', type: 'official_static' },
  { name: 'PMFBY आधिकारिक पोर्टल', type: 'official_static' },
  { name: 'कृषि विस्तार प्रकाशन', type: 'official_static' },
  { name: 'KVK (कृषि विज्ञान केंद्र) दिशानिर्देश', type: 'official_static' },
]

const LIMITATIONS = [
  { hi: 'लाइव मंडी भाव: AGMARKNET API उपलब्ध नहीं — नमूना डेटा दिखाया गया', en: 'Live mandi prices: AGMARKNET API unavailable — sample data shown' },
  { hi: 'लाइव मौसम: IMD API के लिए लिखित अनुमति आवश्यक — नमूना डेटा दिखाया गया', en: 'Live weather: Written IMD permission required — sample data shown' },
  { hi: 'वॉइस API: Gnani Prisma/Timbre के लिए API कुंजी आवश्यक', en: 'Voice API: API key required for Gnani Prisma/Timbre' },
  { hi: 'हरियाणवी भाषा: केवल उच्चारण परीक्षण — समर्पित भाषा समर्थन का दावा नहीं', en: 'Haryanvi language: Accent testing only — no dedicated language support claimed' },
  { hi: 'यह एक शोध प्रोटोटाइप है, प्रमाणित उत्पाद नहीं', en: 'This is a research prototype, not a certified product' },
]

const PRINCIPLES = [
  { hi: 'अनुमानित उर्वरक या कीटनाशक मात्रा कभी न दें', en: 'Never provide guessed fertilizer or pesticide doses' },
  { hi: 'असत्यापित जानकारी को सत्यापित के रूप में न दिखाएं', en: 'Never present unverified information as verified' },
  { hi: 'डेटा स्रोत और अंतिम अपडेट हमेशा दिखाएं', en: 'Always show data source and last update' },
  { hi: 'नकली API सफलता कभी न दिखाएं', en: 'Never fake API success' },
  { hi: 'महत्वपूर्ण निर्णयों के लिए स्थानीय विशेषज्ञ को संदर्भित करें', en: 'Refer to local expert for critical decisions' },
]

export default function AboutPage() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Hero */}
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="bg-green-100 rounded-full p-4">
            <Leaf className="w-12 h-12 text-green-600" />
          </div>
        </div>
        <h1 className="text-2xl font-bold text-gray-800">
          {isHindi ? 'किसानवाणी AI के बारे में' : 'About KisanVaani AI'}
        </h1>
        <p className="text-green-700 font-medium mt-1">अपनी भाषा, अपनी खेती, Smart Faisle.</p>
      </div>

      {/* Mission */}
      <section className="bg-green-50 border border-green-200 rounded-xl p-5 mb-6">
        <h2 className="font-semibold text-green-800 flex items-center gap-2 mb-3">
          <Globe className="w-5 h-5" />
          {isHindi ? 'हमारा मिशन' : 'Our Mission'}
        </h2>
        <p className="text-sm text-green-700 leading-relaxed">
          {isHindi
            ? 'किसानवाणी AI का उद्देश्य भारतीय किसानों को उनकी अपनी भाषा में सटीक और उपयोगी कृषि जानकारी प्रदान करना है। विशेषकर उन किसानों के लिए जो जटिल डिजिटल अनुप्रयोगों से परिचित नहीं हैं, यह प्लेटफ़ॉर्म वॉइस-फर्स्ट तकनीक से कृषि सलाह को सुलभ बनाता है।'
            : 'KisanVaani AI aims to provide Indian farmers with accurate and useful agricultural information in their own language. Especially for farmers not comfortable with complex digital applications, this platform makes agricultural advice accessible through voice-first technology.'}
        </p>
      </section>

      {/* Voice technology */}
      <section className="bg-white border border-gray-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-gray-800 flex items-center gap-2 mb-3">
          <Mic className="w-5 h-5 text-green-600" />
          {isHindi ? 'AI वॉइस तकनीक' : 'AI Voice Technology'}
        </h2>
        <div className="space-y-3">
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-xs font-semibold text-gray-700">Gnani Prisma v2.5 — Speech-to-Text</p>
            <p className="text-xs text-gray-500 mt-1">
              {isHindi
                ? 'हिंदी वॉइस इनपुट को टेक्स्ट में बदलने के लिए। हरियाणवी उच्चारण परीक्षण शामिल।'
                : 'Converts Hindi voice input to text. Includes Haryanvi accent testing.'}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-xs font-semibold text-gray-700">Gnani Timbre v2.5 — Text-to-Speech</p>
            <p className="text-xs text-gray-500 mt-1">
              {isHindi
                ? 'AI उत्तरों को हिंदी में बोले जाने वाले ऑडियो में बदलने के लिए।'
                : 'Converts AI answers to spoken Hindi audio.'}
            </p>
          </div>
          <p className="text-xs text-amber-700 bg-amber-50 border border-amber-100 rounded-lg p-2">
            ⚠️ {isHindi
              ? 'वॉइस फीचर के लिए Gnani API कुंजी आवश्यक है। API कुंजी के बिना, सिस्टम स्पष्ट रूप से बताएगा कि वॉइस उपलब्ध नहीं है।'
              : 'Voice feature requires Gnani API key. Without an API key, the system will clearly report that voice is unavailable.'}
          </p>
        </div>
      </section>

      {/* Data sources */}
      <section className="bg-white border border-gray-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-gray-800 flex items-center gap-2 mb-3">
          <Database className="w-5 h-5 text-blue-600" />
          {isHindi ? 'कृषि जानकारी स्रोत' : 'Agricultural Information Sources'}
        </h2>
        <div className="space-y-2">
          {DATA_SOURCES.map((src, i) => (
            <div key={i} className="flex items-center gap-2 text-xs">
              <CheckCircle className="w-3.5 h-3.5 text-green-500 flex-shrink-0" />
              <span className="text-gray-700">{src.name}</span>
              <span className="ml-auto bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full text-xs">
                {src.type}
              </span>
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-400 mt-3">
          {isHindi
            ? 'ज्ञान आधार में 37 स्रोत, 114 डोमेन रिकॉर्ड और 82 समीक्षाधीन रिकॉर्ड हैं।'
            : 'Knowledge base contains 37 sources, 114 domain records and 82 records pending review.'}
        </p>
      </section>

      {/* Farmer safety principles */}
      <section className="bg-white border border-gray-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-gray-800 flex items-center gap-2 mb-3">
          <Shield className="w-5 h-5 text-green-600" />
          {isHindi ? 'किसान सुरक्षा सिद्धांत' : 'Farmer Safety Principles'}
        </h2>
        <ul className="space-y-2">
          {PRINCIPLES.map((p, i) => (
            <li key={i} className="flex items-start gap-2 text-xs text-gray-700">
              <CheckCircle className="w-3.5 h-3.5 text-green-500 flex-shrink-0 mt-0.5" />
              <span>{isHindi ? p.hi : p.en}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Known limitations */}
      <section className="bg-amber-50 border border-amber-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-amber-800 flex items-center gap-2 mb-3">
          <AlertTriangle className="w-5 h-5" />
          {isHindi ? 'ज्ञात सीमाएं' : 'Known Limitations'}
        </h2>
        <ul className="space-y-2">
          {LIMITATIONS.map((l, i) => (
            <li key={i} className="flex items-start gap-2 text-xs text-amber-700">
              <span className="flex-shrink-0 mt-0.5">⚠️</span>
              <span>{isHindi ? l.hi : l.en}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Target regions */}
      <section className="bg-white border border-gray-200 rounded-xl p-5 mb-4">
        <h2 className="font-semibold text-gray-800 mb-3">
          {isHindi ? 'लक्षित क्षेत्र' : 'Target Regions'}
        </h2>
        <div className="flex flex-wrap gap-2">
          {['हरियाणा', 'पंजाब', 'उत्तर प्रदेश', 'राजस्थान', 'हिमाचल प्रदेश', 'उत्तराखंड', 'दिल्ली NCR'].map(r => (
            <span key={r} className="bg-green-100 text-green-700 text-xs px-3 py-1 rounded-full font-medium">{r}</span>
          ))}
        </div>
      </section>

      {/* Disclaimer */}
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-xs text-red-700">
        <p className="font-semibold mb-1">
          {isHindi ? '⚠️ महत्वपूर्ण अस्वीकरण' : '⚠️ Important Disclaimer'}
        </p>
        <p className="leading-relaxed">
          {isHindi
            ? 'किसानवाणी AI एक शोध प्रोटोटाइप है। यह प्रमाणित कृषि सलाह सेवा नहीं है। कीटनाशक, उर्वरक, बीज या सिंचाई से संबंधित महत्वपूर्ण निर्णयों के लिए हमेशा अपने स्थानीय कृषि अधिकारी, KVK या प्रमाणित कृषि विशेषज्ञ से संपर्क करें। किसानवाणी AI किसी भी कृषि निर्णय के परिणामों के लिए जिम्मेदार नहीं है।'
            : 'KisanVaani AI is a research prototype and not a certified agricultural advisory service. For important decisions regarding pesticides, fertilizers, seeds or irrigation, always consult your local agriculture officer, KVK or certified agricultural expert. KisanVaani AI is not responsible for the outcomes of any farming decision.'}
        </p>
      </div>
    </div>
  )
}

