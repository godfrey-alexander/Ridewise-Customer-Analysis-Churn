import { useState, useEffect, useMemo } from 'react'
import { loadTrips, loadRfm } from '@/lib/data'
import type { TripRow, RfmRow } from '@/types'
import { DataTable } from '@/components/DataTable'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Select } from '@/components/ui/Select'
import { formatCurrency } from '@/lib/utils'

export function DataExplorer() {
  const [trips, setTrips] = useState<TripRow[]>([])
  const [rfm, setRfm] = useState<RfmRow[]>([])
  const [cityFilter, setCityFilter] = useState('All')
  const [loyaltyFilter, setLoyaltyFilter] = useState('All')

  useEffect(() => {
    loadTrips().then(setTrips)
    loadRfm().then(setRfm)
  }, [])

  const cities = useMemo(() => ['All', ...new Set(trips.map((t) => t.city).filter(Boolean))].sort(), [trips])
  const loyalties = useMemo(() => ['All', ...new Set(trips.map((t) => t.loyalty_status).filter(Boolean))].sort(), [trips])

  const filteredTrips = useMemo(() => {
    let f = trips
    if (cityFilter !== 'All') f = f.filter((t) => t.city === cityFilter)
    if (loyaltyFilter !== 'All') f = f.filter((t) => t.loyalty_status === loyaltyFilter)
    return f
  }, [trips, cityFilter, loyaltyFilter])

  const tripColumns = [
    { key: 'user_id' as const, header: 'User ID', sortable: true },
    { key: 'trip_id' as const, header: 'Trip ID', sortable: true },
    { key: 'city' as const, header: 'City', sortable: true },
    { key: 'loyalty_status' as const, header: 'Loyalty', sortable: true },
    { key: 'pickup_time' as const, header: 'Pickup', sortable: true, render: (r: TripRow) => r.pickup_time?.slice(0, 16) ?? '—' },
    { key: 'total_fare_with_tip' as const, header: 'Total', sortable: true, render: (r: TripRow) => formatCurrency(r.total_fare_with_tip) },
  ]

  const rfmColumns = [
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
          <h1 className="text-xl font-bold text-white sm:text-2xl">Data Explorer</h1>
          <p className="text-sm text-white/60 mt-0.5">Browse trips and segment data</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <div className="w-full min-w-0 sm:w-36">
            <label className="mb-1 block text-xs text-white/50">City</label>
            <Select options={cities.map((c) => ({ value: c, label: c }))} value={cityFilter} onChange={(e) => setCityFilter(e.target.value)} />
          </div>
          <div className="w-full min-w-0 sm:w-36">
            <label className="mb-1 block text-xs text-white/50">Loyalty</label>
            <Select options={loyalties.map((l) => ({ value: l, label: l }))} value={loyaltyFilter} onChange={(e) => setLoyaltyFilter(e.target.value)} />
          </div>
        </div>
      </div>

      <Tabs defaultValue="trips">
        <TabsList>
          <TabsTrigger value="trips">Trips</TabsTrigger>
          <TabsTrigger value="rfm">RFM Segments</TabsTrigger>
        </TabsList>
        <TabsContent value="trips">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Trip records</CardTitle>
              <p className="text-sm text-white/60">{filteredTrips.length} rows</p>
            </CardHeader>
            <CardContent className="p-0">
              <DataTable data={filteredTrips} columns={tripColumns} keyField="trip_id" pageSize={15} />
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="rfm">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">RFM segment data</CardTitle>
              <p className="text-sm text-white/60">{rfm.length} rows</p>
            </CardHeader>
            <CardContent className="p-0">
              <DataTable data={rfm} columns={rfmColumns} keyField="user_id" pageSize={15} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
