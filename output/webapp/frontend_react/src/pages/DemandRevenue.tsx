import { useMemo, useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid } from 'recharts'
import { loadTrips, getUniqueCities, getUniqueYears } from '@/lib/data'
import type { TripRow } from '@/types'
import { MetricCard } from '@/components/MetricCard'
import { ChartCard } from '@/components/ChartCard'
import { Select } from '@/components/ui/Select'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs'
import { formatCurrency, formatCurrencyCompact } from '@/lib/utils'

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

export function DemandRevenue() {
  const [trips, setTrips] = useState<TripRow[]>([])
  const [year, setYear] = useState('All')
  const [month, setMonth] = useState('All')
  const [city, setCity] = useState('All')

  useEffect(() => {
    loadTrips().then(setTrips)
  }, [])

  const years = useMemo(() => ['All', ...getUniqueYears(trips).map(String)], [trips])
  const cities = useMemo(() => ['All', ...getUniqueCities(trips)], [trips])
  const monthOptions = useMemo(() => [{ value: 'All', label: 'All' }, ...MONTHS.map((m, i) => ({ value: String(i + 1), label: m }))], [])

  const filtered = useMemo(() => {
    let f = trips
    if (year !== 'All') f = f.filter((t) => t.pickup_year === parseInt(year, 10))
    if (month !== 'All') f = f.filter((t) => t.pickup_month_num === parseInt(month, 10))
    if (city !== 'All') f = f.filter((t) => t.city === city)
    return f
  }, [trips, year, month, city])

  const users = useMemo(() => new Set(filtered.map((t) => t.user_id)).size, [filtered])
  const totalTrips = filtered.length
  const revenue = useMemo(() => filtered.reduce((s, t) => s + t.total_fare_with_tip, 0), [filtered])
  const avgFare = totalTrips ? revenue / totalTrips : 0

  const hourlyTrips = useMemo(() => {
    const byHour = Array.from({ length: 24 }, (_, h) => ({ hour: h, trips: 0 }))
    filtered.forEach((t) => {
      const h = t.pickup_hour ?? new Date(t.pickup_time).getUTCHours()
      if (h >= 0 && h < 24) byHour[h].trips++
    })
    return byHour
  }, [filtered])

  const dailyTrips = useMemo(() => {
    const byDate = new Map<string, number>()
    filtered.forEach((t) => {
      const d = new Date(t.pickup_time).toISOString().slice(0, 10)
      byDate.set(d, (byDate.get(d) ?? 0) + 1)
    })
    return Array.from(byDate.entries())
      .map(([date, trips]) => ({ date, trips }))
      .sort((a, b) => a.date.localeCompare(b.date))
  }, [filtered])

  const hourlyRevenue = useMemo(() => {
    const byHour = Array.from({ length: 24 }, (_, h) => ({ hour: h, revenue: 0 }))
    filtered.forEach((t) => {
      const h = t.pickup_hour ?? new Date(t.pickup_time).getUTCHours()
      if (h >= 0 && h < 24) byHour[h].revenue += t.total_fare ?? 0
    })
    return byHour
  }, [filtered])

  const dailyRevenue = useMemo(() => {
    const byDate = new Map<string, number>()
    filtered.forEach((t) => {
      const d = new Date(t.pickup_time).toISOString().slice(0, 10)
      byDate.set(d, (byDate.get(d) ?? 0) + (t.total_fare ?? 0))
    })
    return Array.from(byDate.entries())
      .map(([date, revenue]) => ({ date, revenue }))
      .sort((a, b) => a.date.localeCompare(b.date))
  }, [filtered])

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-white sm:text-2xl">Analytics</h1>
          <p className="text-sm text-white/60 mt-0.5">Demand and revenue by hour and day</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <div className="w-full min-w-0 sm:w-32">
            <label className="mb-1 block text-xs text-white/50">Year</label>
            <Select options={years.map((y) => ({ value: y, label: y }))} value={year} onChange={(e) => setYear(e.target.value)} />
          </div>
          <div className="w-full min-w-0 sm:w-32">
            <label className="mb-1 block text-xs text-white/50">Month</label>
            <Select options={monthOptions} value={month} onChange={(e) => setMonth(e.target.value)} />
          </div>
          <div className="w-full min-w-0 sm:w-32">
            <label className="mb-1 block text-xs text-white/50">City</label>
            <Select options={cities.map((c) => ({ value: c, label: c }))} value={city} onChange={(e) => setCity(e.target.value)} />
          </div>
        </div>
      </div>

      <div className="grid gap-3 gap-y-4 grid-cols-2 lg:grid-cols-4">
        <MetricCard title="Total Users" value={users} />
        <MetricCard title="Total Trips" value={totalTrips} />
        <MetricCard title="Revenue" value={formatCurrency(revenue)} />
        <MetricCard title="Avg Fare" value={formatCurrencyCompact(avgFare)} />
      </div>

      <Tabs defaultValue="demand">
        <TabsList className="flex flex-wrap w-full">
          <TabsTrigger value="demand" className="flex-1 min-w-0 sm:flex-initial">Demand</TabsTrigger>
          <TabsTrigger value="revenue" className="flex-1 min-w-0 sm:flex-initial">Revenue</TabsTrigger>
        </TabsList>
        <TabsContent value="demand">
          <div className="space-y-6">
            <ChartCard title="Hourly Trips (24h)" description="Trips per hour of day">
              <div className="h-56 min-h-[200px] sm:h-64 md:h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={hourlyTrips}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="hour" stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <Tooltip contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                    <Bar dataKey="trips" fill="#6c757d" radius={[4, 4, 0, 0]} name="Trips" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>
            <ChartCard title="Daily Demand" description="Trips per day">
              <div className="h-56 min-h-[200px] sm:h-64 md:h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={dailyTrips}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="date" stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <Tooltip contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                    <Line type="monotone" dataKey="trips" stroke="#6c757d" strokeWidth={2} dot={{ fill: '#6c757d' }} name="Trips" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>
          </div>
        </TabsContent>
        <TabsContent value="revenue">
          <div className="space-y-6">
            <ChartCard title="Revenue by Hour" description="Revenue per hour of day">
              <div className="h-56 min-h-[200px] sm:h-64 md:h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={hourlyRevenue}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="hour" stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <Tooltip contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} formatter={(v: number) => formatCurrency(v)} />
                    <Bar dataKey="revenue" fill="#6c757d" radius={[4, 4, 0, 0]} name="Revenue" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>
            <ChartCard title="Daily Revenue" description="Revenue per day">
              <div className="h-56 min-h-[200px] sm:h-64 md:h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={dailyRevenue}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="date" stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} />
                    <Tooltip contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} formatter={(v: number) => formatCurrency(v)} />
                    <Line type="monotone" dataKey="revenue" stroke="#6c757d" strokeWidth={2} dot={{ fill: '#6c757d' }} name="Revenue" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
