'use client'

import React, { useState } from 'react'
import MessageList, { Message } from '@/components/MessageList'
import ChatInput from '@/components/ChatInput'

type Tone = 'Helpful Professional' | 'Friendly Assistant' | 'Expert Consultant'

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I am your friendly retail agent. How can I help you today?',
      sender: 'agent',
    },
  ])
  const [tone, setTone] = useState<Tone>('Helpful Professional')
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (text: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          tone: tone,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response from agent')
      }

      const data = await response.json()
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'agent',
      }

      setMessages((prev) => [...prev, agentMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'agent',
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white border-x shadow-sm">
      <header className="flex items-center justify-between p-4 border-b bg-zinc-50/50 backdrop-blur-sm sticky top-0 z-10">
        <div>
          <h1 className="text-lg font-semibold text-black">Retail Agent</h1>
          <p className="text-xs text-zinc-500">Always here to help</p>
        </div>
        <div className="flex items-center gap-2">
          <label htmlFor="tone-select" className="text-xs font-medium text-zinc-900">
            Tone:
          </label>
          <select
            id="tone-select"
            value={tone}
            onChange={(e) => setTone(e.target.value as Tone)}
            className="text-xs border border-zinc-300 rounded-md px-2 py-1 bg-zinc-50 text-zinc-900 focus:outline-none focus:ring-1 focus:ring-black"
          >
            <option value="Helpful Professional">Helpful Professional</option>
            <option value="Friendly Assistant">Friendly Assistant</option>
            <option value="Expert Consultant">Expert Consultant</option>
          </select>
        </div>
      </header>

      <MessageList messages={messages} />

      {isLoading && (
        <div className="px-4 py-2">
          <div className="flex gap-1">
            <div className="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-bounce" />
            <div className="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-bounce [animation-delay:0.2s]" />
            <div className="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-bounce [animation-delay:0.4s]" />
          </div>
        </div>
      )}

      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  )
}