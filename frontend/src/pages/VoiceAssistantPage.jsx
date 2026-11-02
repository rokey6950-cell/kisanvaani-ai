import React, { useRef, useEffect, useState, useCallback } from 'react'
import {
  Mic, Square, Play, Pause, RotateCcw, Trash2,
  Loader, AlertCircle, CheckCircle, Volume2, VolumeX, Send,
  Info, Sparkles, HelpCircle, Check, ArrowRight
} from 'lucide-react'
import { useApp } from '../context/AppContext'
import { useVoiceRecorder } from '../hooks/useVoiceRecorder'
import { useKisanVaaniApi } from '../hooks/useKisanVaaniApi'
import { getVoiceStatus } from '../services/api'

// Format seconds into mm:ss
function fmtDuration(s) {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}

function MessageBubble({ msg, isHindi, onSpeak, isSpeaking, stopSpeaking, ttsLoading }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-md sm:max-w-lg lg:max-w-xl rounded-2xl px-5 py-3.5 text-sm shadow-sm transition-all ${
          isUser
            ? 'bg-green-700 text-white rounded-br-sm'
            : 'bg-white border border-gray-200 text-gray-800 rounded-bl-sm'
        }`}
      >
        {/* Role & Time Header */}
        <div className="flex items-center justify-between text-xs mb-1.5 opacity-75">
          <span className="font-semibold">
            {isUser
              ? (isHindi ? '👤 किसान भाई' : '👤 Farmer')
              : (isHindi ? '🌱 किसानवाणी AI' : '🌱 KisanVaani AI')}
          </span>
          <span>
            {new Date(msg.timestamp).toLocaleTimeString('hi-IN', { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>

        {/* Message Content */}
        <p className="leading-relaxed whitespace-pre-wrap text-sm sm:text-base">{msg.content}</p>

        {/* Sources Attribution */}
        {msg.sources && msg.sources.length > 0 && (
          <div className="mt-3 pt-2.5 border-t border-gray-100 flex flex-wrap items-center gap-1.5 text-xs text-gray-500">
            <span className="font-medium text-gray-600">📚 {isHindi ? 'स्रोत:' : 'Sources:'}</span>
            {msg.sources.map((src, idx) => (
              <span key={idx} className="bg-gray-100 text-gray-700 px-2 py-0.5 rounded text-xs font-mono">
                {src}
              </span>
            ))}
          </div>
        )}

        {/* Audio Listen / Stop Controls for Assistant Response */}
        {!isUser && (
          <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between">
            <button
              onClick={() => {
                if (isSpeaking) {
                  stopSpeaking()
                } else {
                  onSpeak(msg.content)
                }
              }}
              disabled={ttsLoading}
              className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg transition-colors ${
                isSpeaking
                  ? 'bg-red-50 text-red-600 border border-red-200 hover:bg-red-100'
                  : 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100'
              }`}
            >
              {ttsLoading ? (
                <><Loader className="w-3.5 h-3.5 animate-spin" /> {isHindi ? 'तैयार हो रहा है…' : 'Loading…'}</>
              ) : isSpeaking ? (
                <><VolumeX className="w-3.5 h-3.5" /> {isHindi ? 'आवाज़ बंद करें' : 'Stop Audio'}</>
              ) : (
                <><Volume2 className="w-3.5 h-3.5" /> {isHindi ? 'जवाब सुनें (Audio)' : 'Listen to Answer'}</>
              )}
            </button>

            {msg.verification_status && (
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                msg.verification_status === 'verified'
                  ? 'bg-green-100 text-green-700'
                  : msg.verification_status === 'pending_review'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {msg.verification_status === 'verified' ? '✓ सत्यापित' : 'समीक्षाधीन'}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function VoiceAssistantPage() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  const {
    isRecording, audioBlob, duration, mimeType, error: recError,
    startRecording, stopRecording, clearRecording,
  } = useVoiceRecorder()

  const {
    messages, chatLoading, chatError,
    transcribeLoading, transcribeError, lastTranscriptionInfo,
    ttsLoading, ttsError, isSpeaking, ttsProviderInfo,
    sendMessage, transcribe, speak, stopSpeaking, clearConversation,
  } = useKisanVaaniApi()

  const [voiceEngineStatus, setVoiceEngineStatus] = useState(null)
  const [transcript, setTranscript] = useState('')
  const [textInput, setTextInput] = useState('')
  const [showKeyNotice, setShowKeyNotice] = useState(false)

  const messagesEndRef = useRef(null)

  // Fetch Voice Engine Configuration Status on mount
  useEffect(() => {
    getVoiceStatus()
      .then(status => {
        setVoiceEngineStatus(status)
        if (!status.stt_configured) {
          setShowKeyNotice(true)
        }
      })
      .catch(() => {})
  }, [])

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, chatLoading, transcribeLoading])

  // Process audio after recording stops
  useEffect(() => {
    if (!audioBlob || isRecording) return
    ;(async () => {
      const text = await transcribe(audioBlob, mimeType, language)
      if (text && text.trim()) {
        setTranscript(text)
        const resp = await sendMessage(text, language)
        if (resp && resp.content) {
          speak(resp.content, language)
        }
      }
    })()
  }, [audioBlob]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleStopRecording = () => {
    stopRecording()
  }

  const handleTextSend = async (customText = null) => {
    const t = (customText || textInput).trim()
    if (!t) return
    setTextInput('')
    setTranscript('')
    const resp = await sendMessage(t, language)
    if (resp && resp.content) {
      speak(resp.content, language)
    }
  }

  const handleClear = () => {
    stopSpeaking()
    clearConversation()
    clearRecording()
    setTranscript('')
    setTextInput('')
  }

  const anyError = recError || transcribeError || chatError || ttsError

  // Sample quick questions
  const EXAMPLE_QUESTIONS = [
    'गेहूं की बुवाई का सही समय क्या है?',
    'धान में खैरा रोग के लक्षण और उपाय क्या हैं?',
    'PM-KISAN सम्मान निधि योजना की पात्रता क्या है?',
    'सरसों में माहू (चेपा) कीट का नियंत्रण कैसे करें?',
  ]

  // Extract follow up questions from the last assistant message
  const lastAssistantMessage = [...messages].reverse().find(m => m.role === 'assistant')
  const followUps = lastAssistantMessage?.follow_up_questions || []

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] max-w-4xl mx-auto bg-gray-50">
      {/* Top Header Bar */}
      <div className="px-4 py-3 border-b border-gray-200 bg-white flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-green-100 rounded-xl text-green-700">
            <Mic className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base sm:text-lg font-bold text-gray-800 flex items-center gap-2">
              {isHindi ? 'किसानवाणी AI वॉइस सहायक' : 'KisanVaani AI Voice Assistant'}
              <span className="text-xs bg-green-100 text-green-800 font-normal px-2 py-0.5 rounded-full">
                Prisma & Timbre v2.5
              </span>
            </h1>
            <p className="text-xs text-gray-500">
              {isHindi
                ? 'बोलकर सवाल पूछें, प्रामाणिक कृषि जानकारी सुनें'
                : 'Speak agricultural questions, listen to grounded answers'}
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={handleClear}
              className="flex items-center gap-1.5 text-xs text-red-600 hover:text-red-700 border border-red-200 hover:bg-red-50 px-3 py-1.5 rounded-lg transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>{isHindi ? 'बातचीत साफ करें' : 'Clear Chat'}</span>
            </button>
          )}
        </div>
      </div>

      {/* Gnani API Status Disclosure Banner */}
      {voiceEngineStatus?.stt_configured ? (
        <div className="bg-emerald-50 border-b border-emerald-200 px-4 py-2 flex items-center justify-between text-xs text-emerald-800">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="font-semibold">
              {isHindi ? 'Gnani Prisma v2.5 व Timbre सक्रिय:' : 'Gnani Prisma v2.5 & Timbre Active:'}
            </span>
            <span>
              {isHindi
                ? 'रियल-टाइम क्लाउड स्पीच रिकग्निशन व टेक्स्ट-टू-स्पीच सक्रिय है।'
                : 'Real-time cloud speech recognition & text-to-speech are enabled.'}
            </span>
          </div>
        </div>
      ) : showKeyNotice && (
        <div className="bg-amber-50 border-b border-amber-200 px-4 py-2.5 flex items-start justify-between text-xs text-amber-800">
          <div className="flex items-start gap-2">
            <Info className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold">
                {isHindi ? 'वॉइस API सूचना:' : 'Voice API Notice:'}
              </span>{' '}
              {isHindi
                ? 'बैकएंड .env में GNANI_API_KEY सेट होने पर Prisma STT व Timbre TTS से रियल-टाइम आवाज़ चलेगी। आवाज़ आउटपुट के लिए ऑटोमैटिक ब्राउज़र स्पीच एक्टिव है।'
                : 'When GNANI_API_KEY is configured in backend .env, real-time Prisma STT & Timbre TTS activate. Browser speech synthesis is currently active for audio playback.'}
            </div>
          </div>
          <button
            onClick={() => setShowKeyNotice(false)}
            className="text-amber-600 hover:text-amber-800 ml-2 font-bold"
          >
            ✕
          </button>
        </div>
      )}

      {/* Main Conversation Thread */}
      <div className="flex-1 overflow-y-auto px-4 py-5 space-y-2">
        {messages.length === 0 && (
          <div className="py-8 text-center max-w-lg mx-auto">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-700 shadow-inner">
              <Mic className="w-10 h-10" />
            </div>
            <h2 className="text-xl font-bold text-gray-800 mb-1">
              {isHindi ? 'अपनी भाषा में खेती का सवाल पूछें' : 'Ask your farming question by voice'}
            </h2>
            <p className="text-xs sm:text-sm text-gray-500 mb-6">
              {isHindi
                ? 'नीचे दिए गए हरे माइक बटन को दबाकर बोलें। आपका सवाल सुनकर सही उत्तर बताया जाएगा।'
                : 'Click the green microphone below and speak. Your voice will be processed for agricultural advice.'}
            </p>

            {/* Quick Sample Questions */}
            <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm text-left">
              <p className="text-xs font-semibold text-gray-700 mb-2 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-yellow-500" />
                {isHindi ? 'सुझाए गए सवाल (क्लिक करें):' : 'Suggested questions (click to test):'}
              </p>
              <div className="space-y-1.5">
                {EXAMPLE_QUESTIONS.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleTextSend(q)}
                    className="w-full text-left text-xs bg-gray-50 hover:bg-green-50 text-gray-700 hover:text-green-800 py-2 px-3 rounded-xl border border-gray-100 hover:border-green-200 transition-colors flex items-center justify-between group"
                  >
                    <span>{q}</span>
                    <ArrowRight className="w-3 h-3 text-gray-400 group-hover:text-green-600" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Message Bubbles */}
        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            msg={msg}
            isHindi={isHindi}
            onSpeak={speak}
            isSpeaking={isSpeaking}
            stopSpeaking={stopSpeaking}
            ttsLoading={ttsLoading}
          />
        ))}

        {/* Follow-up Questions from AI response */}
        {followUps.length > 0 && !chatLoading && (
          <div className="my-3 pl-4 border-l-2 border-green-400">
            <p className="text-xs font-medium text-gray-500 mb-2">
              💡 {isHindi ? 'संबंधित सवाल:' : 'Follow-up questions:'}
            </p>
            <div className="flex flex-wrap gap-2">
              {followUps.map((fu, idx) => (
                <button
                  key={idx}
                  onClick={() => handleTextSend(fu)}
                  className="text-xs bg-white hover:bg-green-50 text-green-700 border border-green-200 rounded-full px-3 py-1 transition-colors"
                >
                  {fu}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Live Status Indicators */}
        {transcribeLoading && (
          <div className="flex justify-start mb-3">
            <div className="bg-blue-50 border border-blue-200 rounded-2xl px-4 py-2.5 text-xs text-blue-700 flex items-center gap-2.5">
              <Loader className="w-4 h-4 animate-spin text-blue-600" />
              <span>{isHindi ? 'Gnani Prisma v2.5 आवाज़ की पहचान कर रहा है…' : 'Gnani Prisma v2.5 transcribing audio…'}</span>
            </div>
          </div>
        )}

        {chatLoading && (
          <div className="flex justify-start mb-3">
            <div className="bg-green-50 border border-green-200 rounded-2xl px-4 py-2.5 text-xs text-green-700 flex items-center gap-2.5">
              <Loader className="w-4 h-4 animate-spin text-green-600" />
              <span>{isHindi ? 'कृषि ज्ञान आधार से प्रामाणिक उत्तर तैयार हो रहा है…' : 'Retrieving grounded agricultural advice…'}</span>
            </div>
          </div>
        )}

        {/* Recognized Transcript Display Box */}
        {transcript && (
          <div className="my-2 bg-yellow-50 border border-yellow-200 rounded-2xl px-4 py-3 text-xs text-yellow-900 flex items-start gap-2">
            <span className="font-semibold text-yellow-700">🎤 {isHindi ? 'पहचाना गया:' : 'Recognized:'}</span>
            <span className="flex-1">{transcript}</span>
          </div>
        )}

        {/* Global Error Banner */}
        {anyError && (
          <div className="my-3 bg-red-50 border border-red-200 rounded-2xl p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-xs font-semibold text-red-700">
                {isHindi ? 'सूचना / एरर:' : 'Notice / Error:'}
              </p>
              <p className="text-xs text-red-600 mt-0.5 leading-relaxed">{anyError}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Voice Assistant Bottom Controls */}
      <div className="bg-white border-t border-gray-200 p-4">
        {/* Large Central Microphone with Pulse Ripple */}
        <div className="flex flex-col items-center justify-center mb-3">
          {/* Recording Timer & Status */}
          {isRecording && (
            <div className="mb-2 flex items-center gap-2 bg-red-50 border border-red-200 rounded-full px-3 py-1">
              <span className="w-2.5 h-2.5 bg-red-600 rounded-full animate-ping" />
              <span className="text-xs font-mono font-bold text-red-600">{fmtDuration(duration)}</span>
              <span className="text-xs text-red-600 font-medium">
                {isHindi ? 'बोल रहे हैं (सुन रहे हैं…)' : 'Recording…'}
              </span>
            </div>
          )}

          {/* Central Button */}
          <div className="relative">
            {isRecording && (
              <div className="absolute inset-0 rounded-full bg-red-400 opacity-50 animate-ping" />
            )}
            <button
              onClick={isRecording ? handleStopRecording : startRecording}
              disabled={transcribeLoading || chatLoading}
              className={`relative z-10 w-20 h-20 rounded-full flex items-center justify-center shadow-lg transition-all transform active:scale-95 text-white ${
                isRecording
                  ? 'bg-red-600 hover:bg-red-700 scale-105'
                  : 'bg-green-600 hover:bg-green-700'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
              aria-label={isRecording ? 'Stop Recording' : 'Start Recording'}
            >
              {isRecording ? (
                <Square className="w-8 h-8 fill-current" />
              ) : (
                <Mic className="w-9 h-9" />
              )}
            </button>
          </div>

          <p className="text-xs text-gray-500 font-medium mt-2">
            {isRecording
              ? (isHindi ? 'रुकने के लिए दबाएं (Stop)' : 'Click to finish speaking')
              : (isHindi ? 'बोलने के लिए माइक दबाएं' : 'Tap microphone to speak')}
          </p>
        </div>

        {/* Text Input Fallback Bar */}
        <div className="flex gap-2">
          <input
            type="text"
            value={textInput}
            onChange={e => setTextInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleTextSend()}
            placeholder={isHindi ? 'या यहाँ हिंदी में सवाल लिखें…' : 'Or type your question here…'}
            disabled={chatLoading || transcribeLoading}
            className="flex-1 border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
          />
          <button
            onClick={() => handleTextSend()}
            disabled={!textInput.trim() || chatLoading || transcribeLoading}
            className="bg-green-600 hover:bg-green-700 text-white rounded-xl px-4 py-2.5 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            aria-label="Send Message"
          >
            {chatLoading ? <Loader className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </div>

        {/* Active Audio Output Indicator */}
        {isSpeaking && (
          <div className="mt-2.5 bg-green-50 border border-green-200 rounded-xl px-3 py-1.5 flex items-center justify-between text-xs text-green-800">
            <div className="flex items-center gap-2">
              <Volume2 className="w-4 h-4 text-green-600 animate-pulse" />
              <span>{isHindi ? 'ऑडियो प्ले हो रहा है…' : 'Playing audio response…'}</span>
              {ttsProviderInfo && (
                <span className="text-xs text-gray-500">({ttsProviderInfo})</span>
              )}
            </div>
            <button
              onClick={stopSpeaking}
              className="text-red-600 hover:text-red-800 underline font-medium"
            >
              {isHindi ? 'रोकें' : 'Stop'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
