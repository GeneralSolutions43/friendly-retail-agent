import { render, screen, fireEvent } from '@testing-library/react'
import ChatInput from './ChatInput'
import '@testing-library/jest-dom'

describe('ChatInput', () => {
  it('calls onSendMessage when message is sent', () => {
    const onSendMessage = jest.fn()
    render(<ChatInput onSendMessage={onSendMessage} />)
    
    const input = screen.getByPlaceholderText(/Type your message.../i)
    const button = screen.getByRole('button')
    
    fireEvent.change(input, { target: { value: 'Hello' } })
    fireEvent.click(button)
    
    expect(onSendMessage).toHaveBeenCalledWith('Hello')
    expect(input).toHaveValue('')
  })

  it('has the correct styling for text and placeholder', () => {
    render(<ChatInput onSendMessage={jest.fn()} />)
    const input = screen.getByPlaceholderText(/Type your message.../i)
    
    expect(input).toHaveClass('text-zinc-900')
    expect(input).toHaveClass('placeholder:text-zinc-500')
  })
})
