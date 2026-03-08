import { useState, useEffect } from 'react'
import { predictChurn, predictBatch, checkHealth } from '@/lib/api'
import { Dialog } from '@/components/ui/Dialog'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { DataTable } from '@/components/DataTable'
import { formatPercent } from '@/lib/utils'
import type { ChurnPrediction, RiskLevel } from '@/types'
import Papa from 'papaparse'

const LOYALTY_OPTIONS = ['Bronze', 'Silver', 'Gold', 'Platinum']
const RFMS_OPTIONS = ['At Risk', 'Occasional Riders', 'Core Loyal Riders', 'High-Value Surge-Tolerant']
const CITY_OPTIONS = ['Cairo', 'Lagos', 'Nairobi']
const REQUIRED_COLUMNS = [
  'recency', 'total_trips', 'avg_spend', 'total_tip', 'avg_tip', 'avg_rating_given',
  'loyalty_status', 'city', 'avg_distance', 'avg_duration', 'RFMS_segment',
]

const defaultForm = {
  recency: 30,
  total_trips: 20,
  avg_spend: 15,
  total_tip: 3,
  avg_tip: 0.15,
  avg_rating_given: 4,
  loyalty_status: 'Bronze',
  city: 'Cairo',
  avg_distance: 5,
  avg_duration: 18,
  RFMS_segment: 'Occasional Riders',
}

function riskVariant(risk: RiskLevel): 'low' | 'medium' | 'high' | 'critical' {
  const m: Record<RiskLevel, 'low' | 'medium' | 'high' | 'critical'> = {
    Low: 'low',
    Medium: 'medium',
    High: 'high',
    Critical: 'critical',
  }
  return m[risk] ?? 'default'
}

export function ChurnPredictor() {
  const [apiStatus, setApiStatus] = useState<{ ok: boolean; message: string }>({ ok: false, message: 'Checking...' })
  const [form, setForm] = useState(defaultForm)
  const [result, setResult] = useState<ChurnPrediction | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [batchFile, setBatchFile] = useState<File | null>(null)
  const [batchResult, setBatchResult] = useState<Record<string, unknown>[] | null>(null)
  const [batchError, setBatchError] = useState<string | null>(null)

  useEffect(() => {
    checkHealth().then(setApiStatus)
  }, [])

  const handlePredict = async () => {
    try {
      const res = await predictChurn(form) as unknown as ChurnPrediction
      setResult(res)
      setDialogOpen(true)
    } catch (e) {
      setApiStatus({ ok: false, message: e instanceof Error ? e.message : 'Prediction failed' })
    }
  }

  const handleBatchUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    setBatchFile(file ?? null)
    setBatchResult(null)
    setBatchError(null)
  }

  const handleBatchPredict = async () => {
    if (!batchFile) return
    setBatchError(null)
    const text = await batchFile.text()
    const parsed = Papa.parse<Record<string, unknown>>(text, { header: true })
    const rows = parsed.data ?? []
    const missing = REQUIRED_COLUMNS.filter((c) => !parsed.meta.fields?.includes(c))
    if (missing.length) {
      setBatchError(`Missing columns: ${missing.join(', ')}`)
      return
    }
    try {
      const payload = rows.map((r: Record<string, unknown>) => {
        const out: Record<string, unknown> = {}
        REQUIRED_COLUMNS.forEach((col) => {
          const v = r[col]
          if (typeof v === 'string' && (col === 'recency' || col === 'total_trips' || col === 'avg_spend' || col === 'total_tip' || col === 'avg_tip' || col === 'avg_rating_given' || col === 'avg_distance' || col === 'avg_duration')) {
            out[col] = parseFloat(v) ?? 0
          } else {
            out[col] = v
          }
        })
        return out
      })
      const res = await predictBatch(payload)
      setBatchResult(res.predictions.map((p, i) => ({ ...p, _row: i })))
    } catch (e) {
      setBatchError(e instanceof Error ? e.message : 'Batch prediction failed')
    }
  }

  const downloadCsv = () => {
    if (!batchResult?.length) return
    const headers = Object.keys(batchResult[0])
    const line = (row: Record<string, unknown>) => headers.map((h) => JSON.stringify(row[h] ?? '')).join(',')
    const csv = [headers.join(','), ...batchResult.map(line)].join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = 'predictions.csv'
    a.click()
    URL.revokeObjectURL(a.href)
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-white sm:text-2xl">Churn Predictor</h1>
          <p className="text-sm text-white/60 mt-0.5">Estimate churn risk from rider engagement and RFMS metrics</p>
        </div>
        <div className="flex shrink-0 items-center gap-2 rounded-lg border border-white/10 px-3 py-2">
          {apiStatus.ok ? (
            <span className="text-risk-low text-sm font-medium">✓ API ready</span>
          ) : (
            <span className="text-risk-high text-sm font-medium">⚠ {apiStatus.message}</span>
          )}
        </div>
      </div>

      <Tabs defaultValue="single">
        <TabsList className="flex flex-wrap w-full">
          <TabsTrigger value="single" className="flex-1 min-w-0 sm:flex-initial">Single</TabsTrigger>
          <TabsTrigger value="batch" className="flex-1 min-w-0 sm:flex-initial">Batch</TabsTrigger>
          <TabsTrigger value="about" className="flex-1 min-w-0 sm:flex-initial">About</TabsTrigger>
        </TabsList>

        <TabsContent value="single">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Rider features</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                <div className="space-y-4">
                  <p className="text-sm font-medium text-white/80">Usage & Spend</p>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Recency (days)</label>
                    <Input type="number" min={0} step={1} value={form.recency} onChange={(e) => setForm({ ...form, recency: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Total Trips</label>
                    <Input type="number" min={0} step={1} value={form.total_trips} onChange={(e) => setForm({ ...form, total_trips: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Avg Spend ($)</label>
                    <Input type="number" min={0} step={0.5} value={form.avg_spend} onChange={(e) => setForm({ ...form, avg_spend: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Total Tip ($)</label>
                    <Input type="number" min={0} step={0.5} value={form.total_tip} onChange={(e) => setForm({ ...form, total_tip: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Avg Tip ($)</label>
                    <Input type="number" min={0} step={0.02} value={form.avg_tip} onChange={(e) => setForm({ ...form, avg_tip: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Avg Rating (0–5)</label>
                    <input
                      type="range"
                      min={0}
                      max={5}
                      step={0.1}
                      value={form.avg_rating_given}
                      onChange={(e) => setForm({ ...form, avg_rating_given: Number(e.target.value) })}
                      className="w-full accent-dashboard-cyan"
                    />
                    <span className="text-xs text-white/60">{form.avg_rating_given}</span>
                  </div>
                </div>
                <div className="space-y-4">
                  <p className="text-sm font-medium text-white/80">Trip, Segment & City</p>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Loyalty Status</label>
                    <Select options={LOYALTY_OPTIONS.map((l) => ({ value: l, label: l }))} value={form.loyalty_status} onChange={(e) => setForm({ ...form, loyalty_status: e.target.value })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Avg Distance</label>
                    <Input type="number" min={0} step={0.5} value={form.avg_distance} onChange={(e) => setForm({ ...form, avg_distance: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">Avg Duration (min)</label>
                    <Input type="number" min={0} step={1} value={form.avg_duration} onChange={(e) => setForm({ ...form, avg_duration: Number(e.target.value) })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">RFMS Segment</label>
                    <Select options={RFMS_OPTIONS.map((r) => ({ value: r, label: r }))} value={form.RFMS_segment} onChange={(e) => setForm({ ...form, RFMS_segment: e.target.value })} />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs text-white/50">City</label>
                    <Select options={CITY_OPTIONS.map((c) => ({ value: c, label: c }))} value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
                  </div>
                </div>
                <div className="flex flex-col justify-center">
                  <p className="text-sm text-white/60 mb-4">Click Predict Churn Risk to see the result in a pop-up.</p>
                  <Button variant="gradient" onClick={handlePredict} className="font-mono">
                    Predict Churn Risk
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="batch">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Batch upload</CardTitle>
              <p className="text-sm text-white/60">Upload a CSV with columns: {REQUIRED_COLUMNS.join(', ')}</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <input type="file" accept=".csv" onChange={handleBatchUpload} className="text-sm text-white/80" />
              {batchFile && (
                <Button variant="gradient" onClick={handleBatchPredict}>
                  Predict batch
                </Button>
              )}
              {batchError && <p className="text-sm text-risk-high">{batchError}</p>}
              {batchResult && (
                <>
                  <p className="text-sm text-risk-low">Processed {batchResult.length} rows</p>
                  <DataTable
                    data={batchResult}
                    columns={Object.keys(batchResult[0] ?? {}).filter((k) => k !== '_row').map((k) => ({ key: k, header: k, sortable: true }))}
                    keyField="_row"
                  />
                  <Button variant="outline" onClick={downloadCsv}>Download results (CSV)</Button>
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="about">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">About</CardTitle>
            </CardHeader>
            <CardContent className="prose prose-invert prose-sm max-w-none text-white/80">
              <p>
                RideWise Churn Predictor estimates how likely a rider is to churn and suggests retention actions.
              </p>
              <p><strong>Single Predict</strong> — Enter one rider’s metrics; get churn probability, risk level, and a recommendation.</p>
              <p><strong>Batch Predict</strong> — Upload a CSV with the same 11 columns; get predictions for all rows and download results.</p>
              <p><strong>Inputs (11)</strong> — recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given, avg_distance, avg_duration, loyalty_status, RFMS_segment, city.</p>
              <p><strong>Outputs</strong> — churn_probability, risk_level, churn_label, recommendation.</p>
              <p className="text-xs text-white/50 mt-4">RideWise Churn Predictor v1.0 • FastAPI + React</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen} title="Churn Prediction Result">
        {result && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/60">Churn Probability</span>
              <span className="text-xl font-semibold text-white">{formatPercent(result.churn_probability)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/60">Risk Level</span>
              <Badge variant={riskVariant(result.risk_level)}>{result.risk_level}</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/60">Label</span>
              <span className="text-white">{result.churn_label === 1 ? 'Churn' : 'Retained'}</span>
            </div>
            <div className="h-2 w-full rounded-full bg-white/10 overflow-hidden">
              <div
                className="h-full rounded-full bg-dashboard-cyan transition-all"
                style={{ width: `${Math.min(result.churn_probability * 100, 100)}%` }}
              />
            </div>
            <p className="text-xs text-white/50">Threshold: {formatPercent(result.threshold)}</p>
            {result.recommendation && (
              <div className="rounded-lg border border-dashboard-cyan/30 bg-dashboard-cyan/10 p-3">
                <p className="text-sm font-medium text-white">Recommendation</p>
                <p className="text-sm text-white/80 mt-1">{result.recommendation}</p>
              </div>
            )}
          </div>
        )}
      </Dialog>
    </div>
  )
}
