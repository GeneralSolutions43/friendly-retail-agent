'use client'

import React from 'react'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-zinc-50/50 p-4 text-center">
      <div className="max-w-md w-full">
        <h1 className="text-4xl font-bold text-zinc-900 mb-4 tracking-tight">
          Friendly Retail Agent
        </h1>
        <p className="text-lg text-zinc-600 mb-8">
          Your helpful shopping assistant. Use the chat icon in the bottom corner to get started.
        </p>
      </div>
    </div>
  )
}
