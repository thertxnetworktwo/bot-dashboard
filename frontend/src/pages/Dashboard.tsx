import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { api } from '@/lib/api'
import { DashboardStats } from '@/types'
import { Activity, Package, AlertCircle, CheckCircle } from 'lucide-react'

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats'],
    queryFn: api.products.stats,
  })

  if (isLoading) {
    return <div>Loading...</div>
  }

  const statCards = [
    {
      title: 'Total Products',
      value: stats?.total_products || 0,
      icon: Package,
      description: 'All registered products',
    },
    {
      title: 'Active Products',
      value: stats?.active_products || 0,
      icon: CheckCircle,
      description: 'Currently active',
      color: 'text-green-600',
    },
    {
      title: 'Expired Products',
      value: stats?.expired_products || 0,
      icon: AlertCircle,
      description: 'Need renewal',
      color: 'text-red-600',
    },
    {
      title: 'Expiring Soon (30d)',
      value: stats?.expiring_soon_30_days || 0,
      icon: Activity,
      description: 'Expiring in 30 days',
      color: 'text-yellow-600',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Overview of your bot products</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color || 'text-gray-500'}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Quick Stats</CardTitle>
          <CardDescription>
            Products expiring in the next 7 days: {stats?.expiring_soon_7_days || 0}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-600">
            Monitor your product expirations and ensure timely renewals.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
