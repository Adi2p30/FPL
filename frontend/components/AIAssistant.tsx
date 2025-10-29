'use client'

import { useState, useEffect, useRef } from 'react'
import api from '@/lib/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface AIAssistantProps {
  context?: {
    team?: any[]
    budget_remaining?: number
    selected_players?: string[]
    current_gameweek?: number
  }
}

export default function AIAssistant({ context }: AIAssistantProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{
        role: 'assistant',
        content: `Hi! 👋 I'm your FPL AI Assistant powered by Gemini.

I know everything about this dashboard and can help you with:
• Player recommendations and comparisons
• Transfer suggestions
• Captain picks
• Team analysis and strategy
• Explaining all 30+ metrics
• Navigation and features

What would you like help with?`,
        timestamp: new Date()
      }])
    }
  }, [])

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/api/ai/chat', {
        message: input,
        context: context
      })

      const aiMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('AI Error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure your GEMINI_API_KEY is set in the backend environment.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const quickActions = [
    { label: '👑 Best Captains', query: 'Who should I captain this week?' },
    { label: '💎 Find Differentials', query: 'Show me some good differential players' },
    { label: '📊 Analyze My Team', query: 'Analyze my current team' },
    { label: '💰 Value Picks', query: 'Who are the best value players right now?' },
  ]

  const handleQuickAction = (query: string) => {
    setInput(query)
  }

  const clearChat = () => {
    setMessages([{
      role: 'assistant',
      content: 'Chat cleared! How can I help you?',
      timestamp: new Date()
    }])
  }

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed right-4 bottom-4 z-50 btn btn-primary flex items-center gap-2 shadow-glow-lg animate-glow"
        title="Open AI Assistant"
      >
        <span className="text-xl">🤖</span>
        <span className="hidden sm:inline">AI Assistant</span>
      </button>
    )
  }

  return (
    <div className={`fixed right-4 bottom-4 z-50 card border-2 border-accent-pink shadow-glow-lg transition-all duration-300 ${
      isMinimized ? 'w-80 h-16' : 'w-80 sm:w-96 h-[600px]'
    }`}>
      {/* Header */}
      <div className="bg-gradient-primary p-4 rounded-t flex items-center justify-between cursor-pointer"
           onClick={() => !isMinimized && setIsMinimized(!isMinimized)}>
        <div className="flex items-center gap-2">
          <span className="text-2xl">🤖</span>
          <div>
            <h3 className="font-bold text-white">FPL AI Assistant</h3>
            <p className="text-xs text-gray-200">Powered by Gemini</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation()
              setIsMinimized(!isMinimized)
            }}
            className="text-white hover:text-accent-cyan text-xl"
            title={isMinimized ? 'Expand' : 'Minimize'}
          >
            {isMinimized ? '▲' : '▼'}
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation()
              setIsOpen(false)
            }}
            className="text-white hover:text-red-400 text-xl"
            title="Close"
          >
            ✕
          </button>
        </div>
      </div>

      {/* Content (hidden when minimized) */}
      {!isMinimized && (
        <>
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar bg-background-card h-[420px]">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-lg p-3 ${
                    msg.role === 'user'
                      ? 'bg-gradient-primary text-white'
                      : 'bg-background-hover text-white border border-border'
                  }`}
                >
                  <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                  <div className="text-xs opacity-60 mt-1">
                    {msg.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-background-hover rounded-lg p-3 border border-border">
                  <div className="flex items-center gap-2">
                    <div className="spinner"></div>
                    <span className="text-sm text-gray-400">Thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Actions */}
          {messages.length <= 2 && (
            <div className="p-2 border-t border-border bg-background-hover">
              <div className="text-xs text-gray-400 mb-2">Quick actions:</div>
              <div className="grid grid-cols-2 gap-1">
                {quickActions.map((action, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleQuickAction(action.query)}
                    className="btn btn-ghost btn-sm text-xs justify-start"
                    disabled={loading}
                  >
                    {action.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="p-4 border-t border-border bg-background">
            <div className="flex gap-2">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything about FPL..."
                className="input flex-1 resize-none h-12"
                disabled={loading}
                rows={2}
              />
              <div className="flex flex-col gap-1">
                <button
                  onClick={sendMessage}
                  disabled={!input.trim() || loading}
                  className="btn btn-primary btn-sm h-full"
                  title="Send (Enter)"
                >
                  📤
                </button>
                <button
                  onClick={clearChat}
                  className="btn btn-ghost btn-sm text-xs"
                  title="Clear chat"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
