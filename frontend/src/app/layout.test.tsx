import { render } from '@testing-library/react'
import RootLayout from './layout'
import '@testing-library/jest-dom'
import React from 'react'

// Mock ErudaProvider
jest.mock('@/components/ErudaProvider', () => {
  const MockErudaProvider = ({ children }: { children: React.ReactNode }) => <div data-testid="eruda-provider">{children}</div>
  MockErudaProvider.displayName = 'MockErudaProvider'
  return MockErudaProvider
})

// Mock MinimalAgentOverlay
jest.mock('@/components/MinimalAgentOverlay', () => {
  const MockMinimalAgentOverlay = () => <div data-testid="minimal-agent-overlay" />
  MockMinimalAgentOverlay.displayName = 'MockMinimalAgentOverlay'
  return MockMinimalAgentOverlay
})

describe('RootLayout', () => {
  it('renders children wrapped in ErudaProvider and includes MinimalAgentOverlay', () => {
    const { getByTestId } = render(
      <RootLayout>
        <div data-testid="child">Test Child</div>
      </RootLayout>
    )
    
    expect(getByTestId('eruda-provider')).toBeInTheDocument()
    expect(getByTestId('child')).toBeInTheDocument()
    expect(getByTestId('minimal-agent-overlay')).toBeInTheDocument()
  })
})
