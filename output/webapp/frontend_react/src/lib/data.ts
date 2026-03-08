import Papa from 'papaparse'
import type { TripRow, RfmRow } from '@/types'

const TRIPS_URL = '/data/riders_trips.csv'
const RFM_URL = '/data/rfm_data.csv'

let tripsCache: TripRow[] | null = null
let rfmCache: RfmRow[] | null = null

function parseTrip(row: Record<string, string>): TripRow {
  const pickup = row.pickup_time ? new Date(row.pickup_time) : new Date()
  return {
    ...row,
    pickup_time: row.pickup_time,
    pickup_hour: parseInt(row.pickup_hour ?? '0', 10),
    pickup_year: pickup.getUTCFullYear(),
    pickup_month_num: pickup.getUTCMonth() + 1,
    total_fare: parseFloat(row.total_fare ?? '0'),
    total_fare_with_tip: parseFloat(row.total_fare_with_tip ?? row.total_fare ?? '0'),
  } as TripRow
}

function parseRfm(row: Record<string, string>): RfmRow {
  return {
    ...row,
    recency: parseFloat(row.recency ?? '0'),
    frequency: parseFloat(row.frequency ?? '0'),
    monetary: parseFloat(row.monetary ?? '0'),
  } as RfmRow
}

export async function loadTrips(): Promise<TripRow[]> {
  if (tripsCache) return tripsCache
  const res = await fetch(TRIPS_URL)
  const text = await res.text()
  const parsed = Papa.parse<Record<string, string>>(text, { header: true })
  const data = (parsed.data ?? []).filter((r: Record<string, string>) => r.pickup_time).map(parseTrip)
  tripsCache = data
  return data
}

export async function loadRfm(): Promise<RfmRow[]> {
  if (rfmCache) return rfmCache
  const res = await fetch(RFM_URL)
  const text = await res.text()
  const parsed = Papa.parse<Record<string, string>>(text, { header: true })
  const data = (parsed.data ?? []).filter((r: Record<string, string>) => r.user_id).map(parseRfm)
  rfmCache = data
  return data
}

export function getUniqueCities(trips: TripRow[]): string[] {
  const set = new Set(trips.map((t) => t.city).filter(Boolean))
  return Array.from(set).sort()
}

export function getUniqueLoyalty(trips: TripRow[]): string[] {
  const set = new Set(trips.map((t) => t.loyalty_status).filter(Boolean))
  return Array.from(set).sort()
}

export function getUniqueYears(trips: TripRow[]): number[] {
  const set = new Set(trips.map((t) => t.pickup_year).filter((y): y is number => typeof y === 'number'))
  return Array.from(set).sort((a, b) => a - b)
}
