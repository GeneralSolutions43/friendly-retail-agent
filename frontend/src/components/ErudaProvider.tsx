'use client'

import React, { useEffect } from 'react'

interface ErudaProviderProps {
  children: React.ReactNode
}

const ErudaProvider: React.FC<ErudaProviderProps> = ({ children }) => {
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      import('eruda').then((eruda) => {
        eruda.default.init()
      }).catch((err) => {
        console.error('Failed to load eruda', err)
      })
    }
  }, [])

  return <>{children}</>
}

export default ErudaProvider
