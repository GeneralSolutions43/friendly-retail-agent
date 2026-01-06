'use client'

import React from 'react'

export interface Product {
  id: number
  name: string
  category: string
  price: number
  description: string
  inventory_count: number
}

interface ProductCardProps {
  product: Product
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  return (
    <div className="bg-white border border-zinc-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <div className="aspect-square bg-zinc-100 flex items-center justify-center text-zinc-400">
        <svg
          width="48"
          height="48"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
          <circle cx="9" cy="9" r="2" />
          <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
        </svg>
      </div>
      <div className="p-4">
        <div className="flex justify-between items-start mb-1">
          <span className="text-[10px] uppercase tracking-wider font-semibold text-zinc-500">
            {product.category}
          </span>
          <span className="text-sm font-bold text-zinc-900">
            ${product.price.toFixed(2)}
          </span>
        </div>
        <h3 className="text-base font-semibold text-zinc-900 mb-2 truncate">
          {product.name}
        </h3>
        <p className="text-xs text-zinc-600 line-clamp-2 h-8">
          {product.description}
        </p>
      </div>
    </div>
  )
}

export default ProductCard
