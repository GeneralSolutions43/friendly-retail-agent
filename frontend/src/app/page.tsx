'use client'

import React, { useEffect, useState } from 'react'
import ProductCard, { Product } from '@/components/ProductCard'

export default function Home() {
  const [products, setProducts] = useState<Product[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'
        const response = await fetch(`${apiUrl}/products`)
        if (!response.ok) {
          throw new Error('Failed to fetch products')
        }
        const data = await response.json()
        setProducts(data)
      } catch (err) {
        console.error('Error fetching products:', err)
        setError('Could not load products. Please ensure the backend is running.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchProducts()
  }, [])

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-zinc-900 text-white py-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl font-extrabold mb-6 tracking-tight">
            Friendly Retail Store
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Discover our curated collection of premium products. 
            Experience personalized shopping with our AI assistant.
          </p>
        </div>
      </section>

      {/* Product Grid Section */}
      <main className="max-w-6xl mx-auto py-16 px-4">
        <h2 className="text-2xl font-bold text-zinc-900 mb-8 border-b pb-4">
          Featured Products
        </h2>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 animate-pulse">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-80 bg-zinc-100 rounded-xl"></div>
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12 bg-zinc-50 rounded-xl border border-dashed border-zinc-300">
            <p className="text-zinc-600 mb-2">{error}</p>
            <button 
              onClick={() => window.location.reload()}
              className="text-sm font-semibold text-black underline"
            >
              Try again
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </main>

      {/* Footer info for demo */}
      <footer className="bg-zinc-50 border-t py-12 px-4 mt-auto">
        <div className="max-w-6xl mx-auto text-center text-zinc-500 text-sm">
          <p>&copy; 2026 Friendly Retail Agent Demo. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}