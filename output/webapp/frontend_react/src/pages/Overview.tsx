import { useMemo, useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'
import { loadTrips, getUniqueCities, getUniqueLoyalty } from '@/lib/data'
import type { TripRow } from '@/types'
import { MetricCard } from '@/components/MetricCard'
import { ChartCard } from '@/components/ChartCard'
import { Select } from '@/components/ui/Select'
import { formatCurrency } from '@/lib/utils'

const CHART_COLORS = ['#9ca3af', '#6b7280', '#4b5563', '#374151', '#d1d5db']

export function Overview() {
  const [trips, setTrips] = useState<TripRow[]>([])
  const [city, setCity] = useState('All')
  const [loyalty, setLoyalty] = useState('All')

  useEffect(() => {
    loadTrips().then(setTrips)
  }, [])

  const cities = useMemo(() => ['All', ...getUniqueCities(trips)], [trips])
  const loyalties = useMemo(() => ['All', ...getUniqueLoyalty(trips)], [trips])

  const filtered = useMemo(() => {
    let f = trips
    if (city !== 'All') f = f.filter((t) => t.city === city)
    if (loyalty !== 'All') f = f.filter((t) => t.loyalty_status === loyalty)
    return f
  }, [trips, city, loyalty])

  const totalUsers = useMemo(() => new Set(filtered.map((t) => t.user_id)).size, [filtered])
  const totalTrips = useMemo(() => filtered.length, [filtered])
  const revenue = useMemo(() => filtered.reduce((s, t) => s + t.total_fare_with_tip, 0), [filtered])

  const loyaltyData = useMemo(() => {
    const byLoyalty = new Map<string, number>()
    filtered.forEach((t) => byLoyalty.set(t.loyalty_status, (byLoyalty.get(t.loyalty_status) ?? 0) + 1))
    const total = filtered.length
    return Array.from(byLoyalty.entries()).map(([name, count]) => ({
      name,
      value: total ? (count / total) * 100 : 0,
      count,
    }))
  }, [filtered])

  const cityData = useMemo(() => {
    const byCity = new Map<string, number>()
    filtered.forEach((t) => byCity.set(t.city, (byCity.get(t.city) ?? 0) + 1))
    return Array.from(byCity.entries())
      .map(([city, count]) => ({ city, count }))
      .sort((a, b) => b.count - a.count)
  }, [filtered])

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-white sm:text-2xl">Executive Summary</h1>
          <p className="text-sm text-white/60 mt-0.5">Trip activity, city distribution, and customer dynamics</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <div className="w-full min-w-0 sm:w-40">
            <label className="mb-1 block text-xs text-white/50">City</label>
            <Select
              options={cities.map((c) => ({ value: c, label: c }))}
              value={city}
              onChange={(e) => setCity(e.target.value)}
            />
          </div>
          <div className="w-full min-w-0 sm:w-40">
            <label className="mb-1 block text-xs text-white/50">Loyalty Tier</label>
            <Select
              options={loyalties.map((l) => ({ value: l, label: l }))}
              value={loyalty}
              onChange={(e) => setLoyalty(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="grid gap-3 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
        <MetricCard title="Total Users" value={totalUsers} />
        <MetricCard title="Total Trips" value={totalTrips} />
        <MetricCard title="Revenue" value={formatCurrency(revenue)} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard title="Customer Segmentation" description="Share by loyalty tier">
          <div className="h-64 min-h-[200px] sm:h-72 md:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={loyaltyData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={({ name, value }) => `${name} ${value.toFixed(1)}%`}
                >
                  {loyaltyData.map((_, i) => (
                    <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: number) => `${v.toFixed(1)}%`} contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
        <ChartCard title="City Distribution" description="Users per city">
          <div className="h-64 min-h-[200px] sm:h-72 md:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cityData} layout="vertical" margin={{ left: 50 }}>
                <XAxis type="number" stroke="rgba(255,255,255,0.4)" fontSize={11} tick={{ fontSize: 10 }} />
                <YAxis type="category" dataKey="city" stroke="rgba(255,255,255,0.4)" fontSize={11} width={60} tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                <Bar dataKey="count" fill="#6c757d" radius={[0, 4, 4, 0]} name="Users" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
