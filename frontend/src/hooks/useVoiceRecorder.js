import { useState, useRef, useCallback, useEffect } from 'react'

/**
 * Encodes Float32Array audio samples into 16-bit PCM WAV Blob at target sample rate.
 */
function encodeWAV(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2)
  const view = new DataView(buffer)

  /* RIFF identifier */
  writeString(view, 0, 'RIFF')
  /* file length */
  view.setUint32(4, 36 + samples.length * 2, true)
  /* RIFF type */
  writeString(view, 8, 'WAVE')
  /* format chunk identifier */
  writeString(view, 12, 'fmt ')
  /* format chunk length */
  view.setUint32(16, 16, true)
  /* sample format (raw PCM) */
  view.setUint16(20, 1, true)
  /* channel count (mono) */
  view.setUint16(22, 1, true)
  /* sample rate */
  view.setUint32(24, sampleRate, true)
  /* byte rate (sample rate * block align) */
  view.setUint32(28, sampleRate * 2, true)
  /* block align (channel count * bytes per sample) */
  view.setUint16(32, 2, true)
  /* bits per sample */
  view.setUint16(34, 16, true)
  /* data chunk identifier */
  writeString(view, 36, 'data')
  /* data chunk length */
  view.setUint32(40, samples.length * 2, true)

  // Float to 16-bit PCM conversion
  let offset = 44
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true)
  }

  return new Blob([view], { type: 'audio/wav' })
}

function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i))
  }
}

/**
 * Resamples Float32 audio samples from source sample rate to target sample rate.
 */
function downsampleBuffer(buffer, sourceRate, targetRate) {
  if (sourceRate === targetRate) return buffer
  if (sourceRate < targetRate) return buffer
  const ratio = sourceRate / targetRate
  const newLength = Math.round(buffer.length / ratio)
  const result = new Float32Array(newLength)
  let offsetResult = 0
  let offsetBuffer = 0
  while (offsetResult < result.length) {
    const nextOffsetBuffer = Math.round((offsetResult + 1) * ratio)
    let accum = 0
    let count = 0
    for (let i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
      accum += buffer[i]
      count++
    }
    result[offsetResult] = count > 0 ? accum / count : 0
    offsetResult++
    offsetBuffer = nextOffsetBuffer
  }
  return result
}

export function useVoiceRecorder() {
  const [isRecording, setIsRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState(null)
  const [duration, setDuration] = useState(0)
  const [error, setError] = useState(null)

  const audioContextRef = useRef(null)
  const streamRef = useRef(null)
  const scriptProcessorRef = useRef(null)
  const recordedSamplesRef = useRef([])
  const timerRef = useRef(null)

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearInterval(timerRef.current)
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop())
      }
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        audioContextRef.current.close().catch(() => {})
      }
    }
  }, [])

  const startRecording = useCallback(async () => {
    setError(null)
    setAudioBlob(null)
    setDuration(0)
    recordedSamplesRef.current = []

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
        },
      })
      streamRef.current = stream

      const AudioContextClass = window.AudioContext || window.webkitAudioContext
      const audioContext = new AudioContextClass()
      audioContextRef.current = audioContext

      const source = audioContext.createMediaStreamSource(stream)
      // Buffer size: 4096 samples, 1 input channel, 1 output channel
      const processor = audioContext.createScriptProcessor(4096, 1, 1)
      scriptProcessorRef.current = processor

      processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0)
        // Clone samples
        recordedSamplesRef.current.push(new Float32Array(inputData))
      }

      source.connect(processor)
      processor.connect(audioContext.destination)

      setIsRecording(true)

      // Start duration timer
      timerRef.current = setInterval(() => {
        setDuration(prev => prev + 1)
      }, 1000)
    } catch (err) {
      if (err.name === 'NotAllowedError') {
        setError('माइक्रोफोन की अनुमति नहीं दी गई। कृपया ब्राउज़र में अनुमति दें।')
      } else if (err.name === 'NotFoundError') {
        setError('माइक्रोफोन नहीं मिला।')
      } else {
        setError(`माइक्रोफोन एरर: ${err.message}`)
      }
      setIsRecording(false)
    }
  }, [])

  const stopRecording = useCallback(() => {
    clearInterval(timerRef.current)
    setIsRecording(false)

    if (scriptProcessorRef.current) {
      scriptProcessorRef.current.disconnect()
      scriptProcessorRef.current = null
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop())
      streamRef.current = null
    }

    const audioContext = audioContextRef.current
    if (audioContext && recordedSamplesRef.current.length > 0) {
      const sourceRate = audioContext.sampleRate
      // Flatten chunks into single buffer
      const totalSamples = recordedSamplesRef.current.reduce((acc, c) => acc + c.length, 0)
      const mergedSamples = new Float32Array(totalSamples)
      let offset = 0
      for (const chunk of recordedSamplesRef.current) {
        mergedSamples.set(chunk, offset)
        offset += chunk.length
      }

      // Gnani prefers 16,000 Hz 16-bit PCM mono
      const TARGET_RATE = 16000
      const downsampled = downsampleBuffer(mergedSamples, sourceRate, TARGET_RATE)
      const wavBlob = encodeWAV(downsampled, TARGET_RATE)
      setAudioBlob(wavBlob)

      audioContext.close().catch(() => {})
      audioContextRef.current = null
    }
  }, [])

  const clearRecording = useCallback(() => {
    setAudioBlob(null)
    setDuration(0)
    setError(null)
    recordedSamplesRef.current = []
  }, [])

  return {
    isRecording,
    audioBlob,
    duration,
    mimeType: 'audio/wav',
    error,
    startRecording,
    stopRecording,
    clearRecording,
  }
}
