'use client'

import React, { useState, useEffect, useRef } from 'react'
import '@/styles/minimal-agent.css'

type Tone = 'Helpful Professional' | 'Friendly Assistant' | 'Expert Consultant'

interface Message {
  id: string
  text: string
  sender: 'user' | 'agent'
  time: string
}

type OverlayState = 'open' | 'minimized' | 'dismissed'

const MinimalAgentOverlay: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello, how can I assist you today?',
      sender: 'agent',
      time: 'Just now',
    },
  ])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [state, setState] = useState<OverlayState>('open')
  const [tone, setTone] = useState<Tone>('Helpful Professional')
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const conversationRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Initialize Session ID
    let id = localStorage.getItem('retail_agent_session_id')
    if (!id) {
      id = crypto.randomUUID?.() || Math.random().toString(36).substring(2, 15)
      localStorage.setItem('retail_agent_session_id', id)
    }
    setSessionId(id)

    // Load persisted messages
    const savedMessages = localStorage.getItem('retail_agent_messages')
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages))
      } catch (e) {
        console.error('Error loading messages from localStorage:', e)
      }
    }
  }, [])

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('retail_agent_messages', JSON.stringify(messages))
    }
  }, [messages])

  useEffect(() => {
    if (conversationRef.current) {
      conversationRef.current.scrollTop = conversationRef.current.scrollHeight
    }
  }, [messages, state])

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }

    setMessages((prev) => [...prev, userMessage])
    const currentInput = inputValue
    setInputValue('')
    setIsLoading(true)
    setIsTyping(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'
      const response = await fetch(`${apiUrl}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentInput,
          tone: tone,
          session_id: sessionId,
        }),
      })

      if (!response.ok) {
        setIsTyping(false)
        throw new Error('Failed to get response from agent')
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let accumulatedResponse = ''
      const agentMessageId = (Date.now() + 1).toString()

      // Create an initial empty agent message
      setMessages((prev) => [
        ...prev,
        {
          id: agentMessageId,
          text: '',
          sender: 'agent',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ])

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          // First chunk received, stop showing typing indicator
          setIsTyping(false)

          const chunk = decoder.decode(value, { stream: true })
          const lines = chunk.split('\n')

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                accumulatedResponse += data.response
                
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === agentMessageId ? { ...msg, text: accumulatedResponse } : msg
                  )
                )
              } catch (e) {
                console.error('Error parsing SSE data:', e)
              }
            }
          }
        }
      }

      if (!accumulatedResponse) {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === agentMessageId
              ? { ...msg, text: "I'm sorry, I encountered an issue processing that. Could you try rephrasing?" }
              : msg
          )
        )
      }
    } catch (error) {
      console.error('Error:', error)
      setIsTyping(false)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'agent',
        time: 'Now',
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      setIsTyping(false)
    }
  }

  const handleReset = () => {
    if (confirm('Are you sure you want to reset the conversation?')) {
      localStorage.removeItem('retail_agent_session_id')
      localStorage.removeItem('retail_agent_messages')
      window.location.reload()
    }
  }

  if (state === 'dismissed') {
    return (
      <div className="ai-overlay-container">
        <button 
          className="ai-trigger" 
          onClick={() => setState('open')}
          aria-label="open agent"
        >
          <div className="ai-logo" style={{ marginBottom: 0 }}>
            <div className="ai-logo-inner"></div>
          </div>
        </button>
      </div>
    )
  }

  return (
    <div className="ai-overlay-container">
      <div className={`ai-container ${state === 'minimized' ? 'minimized' : ''}`}>
        <div className="ai-header">
          <div className="ai-controls">
            <button 
              className="ai-control-btn" 
              onClick={handleReset}
              aria-label="reset conversation"
              title="Reset Conversation"
            >
              ⟳
            </button>
            <button 
              className="ai-control-btn" 
              onClick={() => setState(state === 'open' ? 'minimized' : 'open')}
              aria-label="minimize"
            >
              {state === 'open' ? '−' : '+'}
            </button>
            <button 
              className="ai-control-btn" 
              onClick={() => setState('dismissed')}
              aria-label="close"
            >
              ×
            </button>
          </div>
          <div className="ai-logo">
            <div className="ai-logo-inner"></div>
          </div>
          <h1 className="ai-title">AI Assistant</h1>
          <p className="ai-subtitle">Ready to help</p>
          
          {state === 'open' && (
            <div style={{ marginTop: '8px' }}>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value as Tone)}
                style={{
                  fontSize: '10px',
                  background: 'transparent',
                  color: 'rgba(245, 245, 247, 0.6)',
                  border: '1px solid rgba(245, 245, 247, 0.1)',
                  borderRadius: '4px',
                  padding: '2px 4px'
                }}
              >
                <option value="Helpful Professional">Helpful Professional</option>
                <option value="Friendly Assistant">Friendly Assistant</option>
                <option value="Expert Consultant">Expert Consultant</option>
              </select>
            </div>
          )}
        </div>

        {state === 'open' && (
          <>
            <div className="ai-conversation" ref={conversationRef}>
              {messages.map((msg) => (
                <div key={msg.id} className={`ai-message ${msg.sender === 'agent' ? 'ai-response' : 'user-message'}`}>
                  <div className="message-content">{msg.text}</div>
                  <div className="message-time">{msg.time}</div>
                </div>
              ))}
              {isTyping && (
                <div className="ai-message ai-response">
                  <div className="message-content typing-indicator">
                    <span>.</span><span>.</span><span>.</span>
                  </div>
                </div>
              )}
            </div>

            <div className="ai-input-container">
              <form className="ai-input-border" onSubmit={handleSendMessage}>
                <input
                  type="text"
                  className="ai-input"
                  placeholder="Ask me anything..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  disabled={isLoading}
                />
                <button type="submit" className="ai-send-button" disabled={isLoading} aria-label="send message">
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M22 2L11 13"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                    <path
                      d="M22 2L15 22L11 13L2 9L22 2Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
              </form>
            </div>

            <div className="ai-status">
              <div className="ai-status-light" style={{ animationPlayState: isLoading ? 'running' : 'paused' }}></div>
              <span>{isLoading ? 'Processing' : 'Online'}</span>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default MinimalAgentOverlay
