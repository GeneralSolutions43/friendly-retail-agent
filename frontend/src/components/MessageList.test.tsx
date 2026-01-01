import { render, screen } from '@testing-library/react'
import MessageList from './MessageList'
import '@testing-library/jest-dom'

describe('MessageList', () => {
  it('renders messages correctly', () => {
    const messages = [
      { id: '1', text: 'Hello', sender: 'user' as const },
      { id: '2', text: 'Hi! How can I help?', sender: 'agent' as const }
    ]
    render(<MessageList messages={messages} />)
    
    expect(screen.getByText('Hello')).toBeInTheDocument()
    expect(screen.getByText('Hi! How can I help?')).toBeInTheDocument()
  })
})
