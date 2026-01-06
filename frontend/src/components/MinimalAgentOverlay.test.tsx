import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import MinimalAgentOverlay from './MinimalAgentOverlay'
import '@testing-library/jest-dom'
import React from 'react'

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

  it('sends a message and displays response', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ response: 'Hello user', tone: 'Helpful Professional' }),
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