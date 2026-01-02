import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Page from './page'
import '@testing-library/jest-dom'

// Mock fetch
global.fetch = jest.fn()

describe('Page Chat Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('sends a message and displays the response', async () => {
    const mockResponse = {
      response: 'Hello from agent',
      tone: 'Helpful Professional'
    }
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    })

    render(<Page />)
    
    const input = screen.getByPlaceholderText(/Type your message.../i)
    const button = screen.getByRole('button', { name: /Send/i })
    
    fireEvent.change(input, { target: { value: 'User message' } })
    fireEvent.click(button)
    
    expect(screen.getByText('User message')).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByText('Hello from agent')).toBeInTheDocument()
    })
    
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/chat'),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          message: 'User message',
          tone: 'Helpful Professional'
        })
      })
    )
  })

  it('sends the correct tone when changed', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ response: 'Expert advice', tone: 'Expert Consultant' }),
    })

    render(<Page />)
    
    const select = screen.getByLabelText(/Tone:/i)
    fireEvent.change(select, { target: { value: 'Expert Consultant' } })
    
    const input = screen.getByPlaceholderText(/Type your message.../i)
    const button = screen.getByRole('button', { name: /Send/i })
    
    fireEvent.change(input, { target: { value: 'What is your advice?' } })
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/chat'),
        expect.objectContaining({
          body: JSON.stringify({
            message: 'What is your advice?',
            tone: 'Expert Consultant'
          })
        })
      )
    })
  })

  it('has the correct styling for the tone selector', () => {
    render(<Page />)
    const select = screen.getByLabelText(/Tone:/i)
    
    expect(select).toHaveClass('text-zinc-900')
    expect(select).toHaveClass('border-zinc-300')
    expect(select).toHaveClass('bg-zinc-50')
  })
})
