import { render, screen } from '@testing-library/react'
import Page from './page'
import '@testing-library/jest-dom'

describe('Page', () => {
  it('renders a minimalist landing page without the original chat interface', () => {
    render(<Page />)
    
    // Original chat elements should NOT be present
    expect(screen.queryByPlaceholderText(/Type your message.../i)).not.toBeInTheDocument()
    expect(screen.queryByLabelText(/Tone:/i)).not.toBeInTheDocument()
    
    // Minimalist landing page elements
    expect(screen.getByText(/Friendly Retail Agent/i)).toBeInTheDocument()
    expect(screen.getByText(/Your helpful shopping assistant/i)).toBeInTheDocument()
  })
})