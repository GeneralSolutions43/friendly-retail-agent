import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import MinimalAgentOverlay from './MinimalAgentOverlay'
import '@testing-library/jest-dom'
import React from 'react'
import { TextDecoder, TextEncoder } from 'util'

// Polyfill TextDecoder for Node environment used by Jest
if (typeof global.TextDecoder === 'undefined') {
  (global as any).TextDecoder = TextDecoder
}
if (typeof global.TextEncoder === 'undefined') {
  (global as any).TextEncoder = TextEncoder
}

describe('MinimalAgentOverlay', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders in open state by default', () => {
    render(<MinimalAgentOverlay />)
    expect(screen.getByText(/AI Assistant/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/Ask me anything.../i)).toBeInTheDocument()
  })

  it('toggles minimized state', () => {
    render(<MinimalAgentOverlay />)
    const minimizeBtn = screen.getByLabelText(/minimize/i)
    
    // Minimize
    fireEvent.click(minimizeBtn)
    expect(screen.queryByPlaceholderText(/Ask me anything.../i)).not.toBeInTheDocument()
    expect(screen.getByText(/AI Assistant/i)).toBeInTheDocument()
    
    // Open again
    fireEvent.click(minimizeBtn)
    expect(screen.getByPlaceholderText(/Ask me anything.../i)).toBeInTheDocument()
  })

  it('dismisses the overlay and shows trigger icon', () => {
    render(<MinimalAgentOverlay />)
    const closeBtn = screen.getByLabelText(/close/i)
    
    fireEvent.click(closeBtn)
    expect(screen.queryByText(/AI Assistant/i)).not.toBeInTheDocument()
    
    const trigger = screen.getByLabelText(/open agent/i)
    expect(trigger).toBeInTheDocument()
    
    // Reopen
    fireEvent.click(trigger)
    expect(screen.getByText(/AI Assistant/i)).toBeInTheDocument()
  })

  it('sends a message and displays streaming response', async () => {
    const mockChunks = [
      'data: {"response": "Hello", "tone": "Helpful Professional"}\n\n',
      'data: {"response": " user", "tone": "Helpful Professional"}\n\n',
    ]

    const mockReader = {
      read: jest.fn()
        .mockResolvedValueOnce({ done: false, value: new TextEncoder().encode(mockChunks[0]) })
        .mockResolvedValueOnce({ done: false, value: new TextEncoder().encode(mockChunks[1]) })
        .mockResolvedValue({ done: true }),
    }

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      body: {
        getReader: () => mockReader,
      },
    })

    render(<MinimalAgentOverlay />)
    const input = screen.getByPlaceholderText(/Ask me anything.../i)
    const sendBtn = screen.getByLabelText(/send message/i)
    
    fireEvent.change(input, { target: { value: 'User message' } })
    fireEvent.click(sendBtn)
    
    expect(screen.getByText('User message')).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByText('Hello user')).toBeInTheDocument()
    })
  })
})