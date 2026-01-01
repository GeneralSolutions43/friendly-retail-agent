'use client'

import React from 'react'

export interface Message {
  id: string
  text: string
  sender: 'user' | 'agent'
}

interface MessageListProps {
  messages: Message[]
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[80%] px-4 py-2 rounded-2xl ${
              msg.sender === 'user'
                ? 'bg-black text-white rounded-br-none'
                : 'bg-zinc-100 text-black rounded-bl-none'
            }`}
          >
            <p className="text-sm leading-relaxed">{msg.text}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

export default MessageList
