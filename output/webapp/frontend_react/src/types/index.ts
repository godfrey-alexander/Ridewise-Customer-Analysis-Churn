// Trip/riders data (from riders_trips.csv)
export interface TripRow {
  user_id: string
  trip_id: string
  city: string
  loyalty_status: string
  pickup_time: string
  pickup_hour: number
  pickup_year?: number
  pickup_month_num?: number
  total_fare: number
  total_fare_with_tip: number
  [key: string]: unknown
}

// RFM / segment data (from rfm_data.csv)
export interface RfmRow {
  user_id: string
  recency: number
  frequency: number
  monetary: number
  last_trip_time: string
  segments: string
  [key: string]: unknown
}

// Churn API
export interface ChurnFeatures {
  recency: number
  total_trips: number
  avg_spend: number
  total_tip: number
  avg_tip: number
  avg_rating_given: number
  loyalty_status: string
  city: string
  avg_distance: number
  avg_duration: number
  RFMS_segment: string
}

export interface ChurnPrediction {
  churn_probability: number
  churn_label: number
  threshold: number
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical'
  recommendation?: string
}

export interface HealthResponse {
  status: string
  model_loaded: boolean
}

export type RiskLevel = 'Low' | 'Medium' | 'High' | 'Critical'
