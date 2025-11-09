import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { toast } from 'sonner'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { api } from '@/lib/api'
import { Product, ProductStatus } from '@/types'
import { formatDate, getDaysUntilExpiry } from '@/lib/utils'
import { ExternalLink, Trash2, RefreshCw } from 'lucide-react'

export default function Products() {
  const queryClient = useQueryClient()
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ['products', page],
    queryFn: () => api.products.list({ page, per_page: 50 }),
  })

  const deleteMutation = useMutation({
    mutationFn: api.products.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] })
      toast.success('Product deleted successfully')
    },
  })

  const renewMutation = useMutation({
    mutationFn: ({ id, months }: { id: string; months: number }) => api.products.renew(id, months),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] })
      toast.success('Product renewed successfully')
    },
  })

  const getStatusBadge = (product: Product) => {
    const daysLeft = getDaysUntilExpiry(product.contract_end_date)
    
    if (product.status === ProductStatus.ACTIVE) {
      return <Badge variant="success">Active ({daysLeft}d left)</Badge>
    } else if (product.status === ProductStatus.EXPIRED) {
      return <Badge variant="destructive">Expired</Badge>
    } else {
      return <Badge variant="warning">Expiring Soon ({daysLeft}d)</Badge>
    }
  }

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Products</h1>
          <p className="text-gray-500 mt-1">Manage your bot products</p>
        </div>
      </div>

      <div className="grid gap-4">
        {data?.products?.map((product: Product) => (
          <Card key={product.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="space-y-1">
                  <CardTitle>{product.name}</CardTitle>
                  <p className="text-sm text-gray-500">{product.description || 'No description'}</p>
                </div>
                {getStatusBadge(product)}
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div>
                  <p className="text-sm font-medium text-gray-500">Bot/Website</p>
                  {product.bot_username ? (
                    <a
                      href={`https://t.me/${product.bot_username}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline flex items-center gap-1"
                    >
                      @{product.bot_username} <ExternalLink className="h-3 w-3" />
                    </a>
                  ) : product.website_link ? (
                    <a
                      href={product.website_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline flex items-center gap-1"
                    >
                      Website <ExternalLink className="h-3 w-3" />
                    </a>
                  ) : (
                    <p className="text-sm">N/A</p>
                  )}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500">Contract</p>
                  <p className="text-sm">{product.contract_months} months</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500">End Date</p>
                  <p className="text-sm">{formatDate(product.contract_end_date)}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500">Customer</p>
                  <p className="text-sm">{product.customer_telegram || 'N/A'}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => renewMutation.mutate({ id: product.id, months: 3 })}
                >
                  <RefreshCw className="h-4 w-4 mr-1" />
                  Renew 3m
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => {
                    if (confirm('Are you sure you want to delete this product?')) {
                      deleteMutation.mutate(product.id)
                    }
                  }}
                >
                  <Trash2 className="h-4 w-4 mr-1" />
                  Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {data?.total === 0 && (
        <Card>
          <CardContent className="py-10 text-center">
            <p className="text-gray-500">No products found. Create your first product to get started.</p>
          </CardContent>
        </Card>
      )}

      {data && data.total > 0 && (
        <div className="flex justify-between items-center">
          <p className="text-sm text-gray-500">
            Showing {data.products.length} of {data.total} products
          </p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={page === 1}
              onClick={() => setPage(p => p - 1)}
            >
              Previous
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={page * data.per_page >= data.total}
              onClick={() => setPage(p => p + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
