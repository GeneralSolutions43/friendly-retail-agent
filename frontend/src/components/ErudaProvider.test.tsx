import { render, waitFor } from '@testing-library/react'
import ErudaProvider from './ErudaProvider'
import '@testing-library/jest-dom'
import React from 'react'

// Mock eruda
const mockInit = jest.fn()
jest.mock('eruda', () => ({
  __esModule: true,
  default: {
    init: mockInit,
  },
}))

describe('ErudaProvider', () => {
  const originalEnv = process.env.NODE_ENV

  beforeEach(() => {
    jest.clearAllMocks()
  })

  afterAll(() => {
    process.env.NODE_ENV = originalEnv
  })

  it('should call eruda.init in development', async () => {
    // Note: process.env.NODE_ENV might be tricky to change at runtime for some bundlers/loaders
    // but in Jest it usually works if not cached.
    // However, the component checks it at mount.
    
    // We mock the environment by defining it
    Object.defineProperty(process.env, 'NODE_ENV', {
      value: 'development',
      configurable: true
    })

    render(<ErudaProvider><div>Test</div></ErudaProvider>)
    
    await waitFor(() => {
      expect(mockInit).toHaveBeenCalled()
    })
  })

  it('should NOT call eruda.init in production', async () => {
    Object.defineProperty(process.env, 'NODE_ENV', {
      value: 'production',
      configurable: true
    })

    render(<ErudaProvider><div>Test</div></ErudaProvider>)
    
    // Wait a bit to ensure async import would have happened
    await new Promise((r) => setTimeout(r, 100))
    expect(mockInit).not.toHaveBeenCalled()
  })
})