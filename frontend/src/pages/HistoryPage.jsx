import React, { useEffect, useState } from 'react'
import { History, Loader, AlertCircle, Trash2, ChevronDown, ChevronUp, MessageSquare } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { getHistory, getConversation, deleteConversation, clearHistory } from '../services/api'

function ConversationItem({ conv, isHindi, onDelete, onOpen, isOpen }) {
  const msgCount = conv.message_count || conv.messages?.length || 0
  const preview = conv.last_message || conv.preview || ''
  const ts = conv.created_at || conv.timestamp
  const dateStr = ts
    ? new Date(ts).toLocaleString('hi-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    : ''

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="flex items-start gap-3 p-4">
        <div className="bg-purple-100 rounded-lg p-2 flex-shrink-0">
          <MessageSquare className="w-4 h-4 text-purple-600" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-sm font-medium text-gray-800 truncate">
                {conv.title || (isHindi ? 'बातचीत' : 'Conversation')} #{conv.id}
              </p>
              <p className="text-xs text-gray-500 mt-0.5">{dateStr}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {msgCount} {isHindi ? 'संदेश' : 'msg'}
              </span>
              <button
                onClick={() => onDelete(conv.id)}
                className="text-red-400 hover:text-red-600 p-1"
                title={isHindi ? 'हटाएं' : 'Delete'}
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => onOpen(conv.id)}
                className="text-gray-400 hover:text-gray-600 p-1"
              >
                {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
            </div>
          </div>
          {preview && (
            <p className="text-xs text-gray-500 mt-1 truncate">{preview}</p>
          )}
        </div>
      </div>

      {isOpen && conv._messages && (
        <div className="border-t border-gray-100 px-4 pb-4">
          <div className="max-h-80 overflow-y-auto space-y-2 mt-3">
            {conv._messages.map((msg, i) => (
              <div
                key={i}
                className={`text-xs rounded-xl px-3 py-2 ${
                  msg.role === 'user'
                    ? 'bg-green-50 border border-green-200 ml-8'
                    : 'bg-gray-50 border border-gray-200 mr-8'
                }`}
              >
                <span className="font-medium text-gray-500">
                  {msg.role === 'user'
                    ? (isHindi ? '👤 किसान:' : '👤 Farmer:')
                    : (isHindi ? '🤖 किसानवाणी:' : '🤖 KisanVaani:')}
                </span>
                <p className="text-gray-700 mt-0.5 whitespace-pre-wrap">{msg.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default function HistoryPage() {
  const { language } = useApp()
  const isHindi = language === 'hi'

  const [conversations, setConversations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [openId, setOpenId] = useState(null)
  const [clearLoading, setClearLoading] = useState(false)

  const load = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getHistory()
      setConversations(data.conversations || data || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleOpen = async (id) => {
    if (openId === id) { setOpenId(null); return }
    // Fetch full messages for this conversation
    try {
      const data = await getConversation(id)
      setConversations(prev =>
        prev.map(c => c.id === id ? { ...c, _messages: data.messages || [] } : c)
      )
      setOpenId(id)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm(isHindi ? 'क्या आप यह बातचीत हटाना चाहते हैं?' : 'Delete this conversation?')) return
    try {
      await deleteConversation(id)
      setConversations(prev => prev.filter(c => c.id !== id))
      if (openId === id) setOpenId(null)
    } catch (err) {
      setError(err.message)
    }
  }

  const handleClearAll = async () => {
    if (!window.confirm(isHindi ? 'क्या आप सभी बातचीत का इतिहास हटाना चाहते हैं?' : 'Clear all conversation history?')) return
    setClearLoading(true)
    try {
      await clearHistory()
      setConversations([])
      setOpenId(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setClearLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-100 rounded-lg">
            <History className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">
              {isHindi ? 'बातचीत इतिहास' : 'Conversation History'}
            </h1>
            <p className="text-sm text-gray-500">
              {isHindi
                ? `${conversations.length} पिछली बातचीत`
                : `${conversations.length} past conversations`}
            </p>
          </div>
        </div>
        {conversations.length > 0 && (
          <button
            onClick={handleClearAll}
            disabled={clearLoading}
            className="flex items-center gap-1.5 text-xs text-red-500 hover:text-red-700 border border-red-200 px-3 py-1.5 rounded-lg disabled:opacity-50"
          >
            {clearLoading ? <Loader className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
            {isHindi ? 'सब हटाएं' : 'Clear All'}
          </button>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-2 text-sm text-red-700 mb-4">
          <AlertCircle className="w-5 h-5 flex-shrink-0" /> {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center justify-center py-16">
          <Loader className="w-8 h-8 text-purple-600 animate-spin" />
        </div>
      )}

      {!loading && conversations.length === 0 && !error && (
        <div className="text-center text-gray-400 py-16">
          <History className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p className="text-gray-500 font-medium">
            {isHindi ? 'कोई बातचीत नहीं मिली' : 'No conversations found'}
          </p>
          <p className="text-sm mt-1">
            {isHindi
              ? 'AI सहायक से बात करें — यहाँ इतिहास दिखाई देगा।'
              : 'Chat with the AI Assistant — history will appear here.'}
          </p>
        </div>
      )}

      <div className="space-y-3">
        {conversations.map(conv => (
          <ConversationItem
            key={conv.id}
            conv={conv}
            isHindi={isHindi}
            isOpen={openId === conv.id}
            onOpen={handleOpen}
            onDelete={handleDelete}
          />
        ))}
      </div>
    </div>
  )
}

