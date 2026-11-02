import { useState, useCallback, useRef } from 'react'
import { chat, transcribeAudio, synthesizeSpeech } from '../services/api'

/**
 * KisanVaani AI chat/voice hook.
 *
 * Implements:
 *   - Voice transcription with Gnani Prisma v2.5 / honest status reporting
 *   - Grounded agricultural Q&A with SQLite conversation tracking
 *   - Speech synthesis with Gnani Timbre v2.5 + Browser Web Speech API fallback
 *   - Audio playback controls (play, pause, stop)
 */
export function useKisanVaaniApi() {
  const [conversationId, setConversationId] = useState(null)
  const [messages, setMessages] = useState([])

  const [chatLoading, setChatLoading] = useState(false)
  const [chatError, setChatError] = useState(null)

  const [transcribeLoading, setTranscribeLoading] = useState(false)
  const [transcribeError, setTranscribeError] = useState(null)
  const [lastTranscriptionInfo, setLastTranscriptionInfo] = useState(null)

  const [ttsLoading, setTtsLoading] = useState(false)
  const [ttsError, setTtsError] = useState(null)
  const [ttsAudioUrl, setTtsAudioUrl] = useState(null)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [ttsProviderInfo, setTtsProviderInfo] = useState(null)

  const currentAudioRef = useRef(null)

  /** Send a text message. Appends user + assistant messages to state. */
  const sendMessage = useCallback(async (text, language = 'hi') => {
    setChatError(null)
    setChatLoading(true)

    const userMsg = { role: 'user', content: text, timestamp: new Date().toISOString() }
    setMessages(prev => [...prev, userMsg])

    try {
      const payload = { message: text, language }
      if (conversationId) payload.conversation_id = conversationId

      const data = await chat(payload)

      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id)
      }

      const assistantMsg = {
        role: 'assistant',
        content: data.answer || data.answer_text || data.answer_hi || '',
        sources: data.sources || [],
        confidence: data.confidence,
        verification_status: data.verification_status,
        data_type: data.data_type,
        follow_up_questions: data.follow_up_questions || [],
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, assistantMsg])
      return assistantMsg
    } catch (err) {
      setChatError(err.message)
      return null
    } finally {
      setChatLoading(false)
    }
  }, [conversationId])

  /** Transcribe an audio Blob via the backend (Gnani Prisma). */
  const transcribe = useCallback(async (audioBlob, mimeType, language = 'hi') => {
    setTranscribeError(null)
    setTranscribeLoading(true)
    setLastTranscriptionInfo(null)

    try {
      const formData = new FormData()
      const ext = mimeType.includes('ogg') ? 'ogg' : mimeType.includes('wav') ? 'wav' : 'webm'
      formData.append('audio', audioBlob, `recording.${ext}`)
      formData.append('language', language)

      const data = await transcribeAudio(formData)
      setLastTranscriptionInfo(data)

      if (data.status === 'pending_configuration') {
        setTranscribeError(data.message || 'Gnani Prisma API Key pending in backend .env.')
        return null
      }

      if (data.status === 'error') {
        setTranscribeError(data.message || 'Speech recognition failed.')
        return null
      }

      return data.transcript || ''
    } catch (err) {
      setTranscribeError(err.message)
      return null
    } finally {
      setTranscribeLoading(false)
    }
  }, [])

  /** Stop any currently playing audio (HTML5 or browser speech synthesis) */
  const stopSpeaking = useCallback(() => {
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.cancel()
    }
    if (currentAudioRef.current) {
      currentAudioRef.current.pause()
      currentAudioRef.current.currentTime = 0
    }
    setIsSpeaking(false)
  }, [])

  /** Convert text to speech via Gnani Timbre or Browser Web Speech fallback */
  const speak = useCallback(async (text, language = 'hi') => {
    stopSpeaking()
    setTtsError(null)
    setTtsLoading(true)

    // Revoke previous blob URL
    if (ttsAudioUrl) {
      URL.revokeObjectURL(ttsAudioUrl)
      setTtsAudioUrl(null)
    }

    try {
      const data = await synthesizeSpeech({ text, language })
      setTtsProviderInfo(data.service_provider)

      // 1. If backend returned binary audio via Gnani Timbre
      if (data.audio_base64) {
        const byteChars = atob(data.audio_base64)
        const byteArr = new Uint8Array(byteChars.length)
        for (let i = 0; i < byteChars.length; i++) byteArr[i] = byteChars.charCodeAt(i)
        const blob = new Blob([byteArr], { type: data.format || 'audio/wav' })
        const url = URL.createObjectURL(blob)
        setTtsAudioUrl(url)
        setIsSpeaking(true)

        const audio = new Audio(url)
        currentAudioRef.current = audio
        audio.onended = () => setIsSpeaking(false)
        audio.onerror = () => setIsSpeaking(false)
        await audio.play()
        return { type: 'gnani', url }
      }

      if (data.audio_url) {
        setTtsAudioUrl(data.audio_url)
        setIsSpeaking(true)
        const audio = new Audio(data.audio_url)
        currentAudioRef.current = audio
        audio.onended = () => setIsSpeaking(false)
        audio.onerror = () => setIsSpeaking(false)
        await audio.play()
        return { type: 'gnani', url: data.audio_url }
      }

      // 2. Browser SpeechSynthesis Fallback
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text)
        utterance.lang = language === 'en' ? 'en-IN' : 'hi-IN'
        utterance.rate = 0.95 // slightly slower for rural clarity

        // Try to pick a Hindi voice if available
        const voices = window.speechSynthesis.getVoices()
        const hiVoice = voices.find(v => v.lang.startsWith('hi'))
        if (hiVoice) utterance.voice = hiVoice

        utterance.onstart = () => setIsSpeaking(true)
        utterance.onend = () => setIsSpeaking(false)
        utterance.onerror = () => setIsSpeaking(false)

        window.speechSynthesis.speak(utterance)
        return { type: 'browser_fallback', url: null }
      }

      setTtsError('आवाज़ आउटपुट इस ब्राउज़र में उपलब्ध नहीं है।')
      return null
    } catch (err) {
      setTtsError(err.message)
      return null
    } finally {
      setTtsLoading(false)
    }
  }, [ttsAudioUrl, stopSpeaking])

  const clearConversation = useCallback(() => {
    stopSpeaking()
    setMessages([])
    setConversationId(null)
    setChatError(null)
    setTranscribeError(null)
    setTtsError(null)
    setTtsAudioUrl(null)
    setLastTranscriptionInfo(null)
  }, [stopSpeaking])

  return {
    conversationId,
    messages,
    chatLoading,
    chatError,
    transcribeLoading,
    transcribeError,
    lastTranscriptionInfo,
    ttsLoading,
    ttsError,
    ttsAudioUrl,
    isSpeaking,
    ttsProviderInfo,
    sendMessage,
    transcribe,
    speak,
    stopSpeaking,
    clearConversation,
  }
}
