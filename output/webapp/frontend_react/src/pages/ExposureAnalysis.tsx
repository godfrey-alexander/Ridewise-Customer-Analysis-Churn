import { useMemo, useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { loadRfm } from '@/lib/data'
import type { RfmRow } from '@/types'
import { MetricCard } from '@/components/MetricCard'
import { DateCard } from '@/components/DateCard'
import { ChartCard } from '@/components/ChartCard'
import { DataTable } from '@/components/DataTable'
import { formatCurrency } from '@/lib/utils'

const GRAY_SCALE = ['#6b7280', '#4b5563', '#374151', '#9ca3af', '#d1d5db']

export function ExposureAnalysis() {
  const [rfm, setRfm] = useState<RfmRow[]>([])
  const [inactivityDays, setInactivityDays] = useState(7)

  useEffect(() => {
    loadRfm().then(setRfm)
  }, [])

  const atRisk = useMemo(() => rfm.filter((r) => r.recency <= inactivityDays), [rfm, inactivityDays])

  const exposureBySegment = useMemo(() => {
    const bySeg = new Map<string, number>()
    atRisk.forEach((r) => bySeg.set(r.segments, (bySeg.get(r.segments) ?? 0) + r.monetary))
    const total = atRisk.reduce((s, r) => s + r.monetary, 0)
    return Array.from(bySeg.entries())
      .map(([Segments, revenue]) => ({
        Segments,
        revenue: Math.round(revenue),
        proportion: total ? (revenue / total) * 100 : 0,
      }))
      .sort((a, b) => b.revenue - a.revenue)
  }, [atRisk])

  const totalRevenueExposed = useMemo(() => atRisk.reduce((s, r) => s + r.monetary, 0), [atRisk])
  const totalCustomersExposed = useMemo(() => new Set(atRisk.map((r) => r.user_id)).size, [atRisk])

  const dateMin = useMemo(() => {
    if (atRisk.length === 0) return '—'
    const d = atRisk.map((r) => new Date(r.last_trip_time).getTime())
    return new Date(Math.min(...d)).toISOString().slice(0, 10)
  }, [atRisk])
  const dateMax = useMemo(() => {
    if (atRisk.length === 0) return '—'
    const d = atRisk.map((r) => new Date(r.last_trip_time).getTime())
    return new Date(Math.max(...d)).toISOString().slice(0, 10)
  }, [atRisk])

  const tableColumns = [
    { key: 'user_id' as const, header: 'User ID', sortable: true },
    { key: 'recency' as const, header: 'Recency', sortable: true },
    { key: 'frequency' as const, header: 'Frequency', sortable: true },
    { key: 'monetary' as const, header: 'Monetary', sortable: true, render: (r: RfmRow) => formatCurrency(r.monetary) },
    { key: 'segments' as const, header: 'Segment', sortable: true },
  ]

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-white sm:text-2xl">Insights</h1>
          <p className="text-sm text-white/60 mt-0.5">
            Revenue at risk if customers inactive for the selected days are not re-engaged
          </p>
        </div>
        <div className="w-full min-w-0 sm:w-56">
          <label className="mb-1 block text-xs text-white/50">Days since last activity</label>
          <input
            type="range"
            min={7}
            max={90}
            step={7}
            value={inactivityDays}
            onChange={(e) => setInactivityDays(Number(e.target.value))}
            className="w-full h-2 rounded-lg appearance-none bg-white/10 accent-dashboard-cyan"
          />
          <p className="text-xs text-white/60 mt-1">{inactivityDays} days</p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <MetricCard title="Revenue at Risk" value={formatCurrency(totalRevenueExposed, '£')} />
        <MetricCard title="Customers Exposed" value={totalCustomersExposed.toLocaleString()} />
        <div className="sm:col-span-2 lg:col-span-1">
          <DateCard dateMin={dateMin} dateMax={dateMax} />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard title="Revenue by Segment" description="Proportion of revenue at risk by segment">
          <div className="h-64 min-h-[220px] sm:h-72 md:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={exposureBySegment} layout="vertical" margin={{ left: 60 }}>
                <XAxis type="number" stroke="rgba(255,255,255,0.4)" fontSize={12} tickFormatter={(v) => `£${(v / 1000).toFixed(0)}k`} />
                <YAxis type="category" dataKey="Segments" stroke="rgba(255,255,255,0.4)" fontSize={11} width={80} />
                <Tooltip
                  contentStyle={{ background: '#12141c', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                  formatter={(v: number, _name: string, props: { payload?: { proportion?: number } }) => [
                    `£${v.toLocaleString()} (${props.payload?.proportion?.toFixed(1) ?? 0}%)`,
                    'Revenue',
                  ]}
                />
                <Bar dataKey="revenue" radius={[0, 4, 4, 0]} name="Revenue">
                  {exposureBySegment.map((_, i) => (
                    <Cell key={i} fill={GRAY_SCALE[i % GRAY_SCALE.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
        <DataTable
          title="Customers Driving Exposure"
          data={atRisk}
          columns={tableColumns}
          keyField="user_id"
          pageSize={8}
        />
      </div>
    </div>
  )
}
