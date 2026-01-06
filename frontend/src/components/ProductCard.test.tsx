import { render, screen } from '@testing-library/react'
import ProductCard from './ProductCard'
import '@testing-library/jest-dom'

describe('ProductCard', () => {
  const mockProduct = {
    id: 1,
    name: 'Running Shoes',
    category: 'Footwear',
    price: 99.99,
    description: 'Great for running',
    inventory_count: 10
  }

  it('renders product details correctly', () => {
    render(<ProductCard product={mockProduct} />)
    
    expect(screen.getByText('Running Shoes')).toBeInTheDocument()
    expect(screen.getByText('Footwear')).toBeInTheDocument()
    expect(screen.getByText('$99.99')).toBeInTheDocument()
    expect(screen.getByText(/Great for running/i)).toBeInTheDocument()
  })
})
