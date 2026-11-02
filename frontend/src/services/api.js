/**
 * KisanVaani AI — API service layer
 * All requests go through Vite proxy: /api/v1 → http://127.0.0.1:8000/api/v1
 * No credentials are ever sent to the browser; Gnani keys live in backend .env only.
 */

const BASE_URL = '/api/v1'

/**
 * Generic fetch wrapper. Throws an Error with a user-friendly message on failure.
 */
async function apiFetch(path, options = {}) {
  const url = `${BASE_URL}${path}`
  const defaultHeaders = {}

  // Do not set Content-Type for FormData; browser sets it with boundary automatically
  if (!(options.body instanceof FormData)) {
    defaultHeaders['Content-Type'] = 'application/json'
  }

  const res = await fetch(url, {
    ...options,
    headers: { ...defaultHeaders, ...(options.headers || {}) },
  })

  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    try {
      const err = await res.json()
      detail = err.detail || err.message || detail
    } catch (_) {
      // response body not JSON — keep status string
    }
    throw new Error(detail)
  }

  return res.json()
}

// ── Health ────────────────────────────────────────────────────────────────────

/** GET /health — backend + DB + knowledge base status */
export async function getHealth() {
  return apiFetch('/health')
}

// ── Knowledge base ────────────────────────────────────────────────────────────

/** GET /knowledge/status */
export async function getKnowledgeStatus() {
  return apiFetch('/knowledge/status')
}

/** GET /knowledge/search?q=… */
export async function searchKnowledge(query) {
  const params = new URLSearchParams({ q: query })
  return apiFetch(`/knowledge/search?${params}`)
}

/** GET /knowledge/crops */
export async function getCrops() {
  return apiFetch('/knowledge/crops')
}

/** GET /knowledge/crops/{name} */
export async function getCrop(name) {
  return apiFetch(`/knowledge/crops/${encodeURIComponent(name)}`)
}

/** GET /knowledge/seeds */
export async function getSeedVarieties(params = {}) {
  const qs = new URLSearchParams(params)
  return apiFetch(`/knowledge/seeds?${qs}`)
}

/** GET /knowledge/glossary */
export async function getGlossary(query = '') {
  const qs = query ? `?q=${encodeURIComponent(query)}` : ''
  return apiFetch(`/knowledge/glossary${qs}`)
}

/** GET /knowledge/zones */
export async function getAgroZones(state = '') {
  const qs = state ? `?state=${encodeURIComponent(state)}` : ''
  return apiFetch(`/knowledge/zones${qs}`)
}

// ── Smart Crop Advisory ───────────────────────────────────────────────────────

/** GET /crop-advisory/districts?state=… */
export async function getDistricts(state) {
  const params = new URLSearchParams({ state })
  return apiFetch(`/crop-advisory/districts?${params}`)
}

/** GET /crop-advisory/topics */
export async function getCropTopics() {
  return apiFetch('/crop-advisory/topics')
}

/** POST /crop-advisory/recommendation */
export async function getCropRecommendation(payload) {
  return apiFetch('/crop-advisory/recommendation', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

// ── AI Assistant ──────────────────────────────────────────────────────────────

/**
 * POST /assistant/chat
 * @param {Object} payload — { message, language, conversation_id? }
 */
export async function chat(payload) {
  return apiFetch('/assistant/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// ── Government Schemes ────────────────────────────────────────────────────────

/**
 * GET /schemes
 * @param {Object} params — { category?, q? }
 */
export async function getSchemes(params = {}) {
  const qs = new URLSearchParams(params)
  const queryStr = qs.toString() ? `?${qs.toString()}` : ''
  return apiFetch(`/schemes${queryStr}`)
}

/** GET /schemes/{id} */
export async function getScheme(id) {
  return apiFetch(`/schemes/${encodeURIComponent(id)}`)
}

// ── Mandi prices ──────────────────────────────────────────────────────────────

/**
 * GET /mandi-prices
 * @param {Object} params — { crop?, state?, district?, mandi? }
 */
export async function getMandiPrices(params = {}) {
  const qs = new URLSearchParams(params)
  return apiFetch(`/mandi-prices?${qs}`)
}

/** GET /mandi-prices/markets */
export async function getMandiMarkets() {
  return apiFetch('/mandi-prices/markets')
}

/** GET /mandi-prices/commodities */
export async function getMandiCommodities() {
  return apiFetch('/mandi-prices/commodities')
}

/** GET /mandi-prices/status */
export async function getMandiStatus() {
  return apiFetch('/mandi-prices/status')
}

// ── Weather ───────────────────────────────────────────────────────────────────

/** GET /weather?location=… */
export async function getWeather(location) {
  const qs = location ? `?${new URLSearchParams({ location })}` : ''
  return apiFetch(`/weather${qs}`)
}

/** GET /weather/locations */
export async function getWeatherLocations() {
  return apiFetch('/weather/locations')
}

/** GET /weather/status */
export async function getWeatherStatus() {
  return apiFetch('/weather/status')
}

/** GET /weather/parameters */
export async function getWeatherParameters() {
  return apiFetch('/weather/parameters')
}

/** GET /weather/advisory?location=… */
export async function getWeatherAdvisory(location) {
  const qs = location ? `?${new URLSearchParams({ location })}` : ''
  return apiFetch(`/weather/advisory${qs}`)
}

// ── Conversation history ──────────────────────────────────────────────────────

/** GET /history */
export async function getHistory() {
  return apiFetch('/history')
}

/** GET /history/{id} */
export async function getConversation(id) {
  return apiFetch(`/history/${id}`)
}

/** DELETE /history/{id} */
export async function deleteConversation(id) {
  return apiFetch(`/history/${id}`, { method: 'DELETE' })
}

/** DELETE /history — clear all */
export async function clearHistory() {
  return apiFetch('/history', { method: 'DELETE' })
}

// ── Voice (STT / TTS) ─────────────────────────────────────────────────────────

/** GET /voice/status — Gnani Prisma & Timbre readiness */
export async function getVoiceStatus() {
  return apiFetch('/voice/status')
}

/**
 * POST /voice/transcribe
 * @param {FormData} formData — must contain field "audio" (Blob)
 */
export async function transcribeAudio(formData) {
  return apiFetch('/voice/transcribe', {
    method: 'POST',
    body: formData, // FormData — no Content-Type header set manually
  })
}

/**
 * POST /voice/speak
 * @param {Object} payload — { text, language }
 */
export async function synthesizeSpeech(payload) {
  return apiFetch('/voice/speak', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

