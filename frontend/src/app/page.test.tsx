import { render, screen, waitFor } from '@testing-library/react'
import Page from './page'
import '@testing-library/jest-dom'
import React from 'react'

// Mock fetch
global.fetch = jest.fn()

describe('Home Page Storefront', () => {
  const mockProducts = [
    { id: 1, name: 'Prod 1', category: 'Cat 1', price: 10, description: 'Desc 1', inventory_count: 5 },
    { id: 2, name: 'Prod 2', category: 'Cat 2', price: 20, description: 'Desc 2', inventory_count: 10 },
  ]

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders hero and product grid with data from backend', async () => {
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockProducts,
    })

    // Note: Since we are using Server Components pattern in plan, but testing with RTL which usually handles Client Components,
    // we need to be careful. However, for the demo we'll likely use a Client Component or a hybrid.
    // If it's a true async Server Component, we need a different testing approach (or make it a Client component for now).
    // Given 'use client' is currently in page.tsx, we'll stick with that for simplicity in the demo.
    
    render(<Page />)
    
    expect(screen.getByText(/Friendly Retail Store/i)).toBeInTheDocument()
    
    await waitFor(() => {
      expect(screen.getByText('Prod 1')).toBeInTheDocument()
      expect(screen.getByText('Prod 2')).toBeInTheDocument()
    })
  })
})
