const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface HealthResponse {
  status: string
  model_loaded: boolean
}

export async function checkHealth(): Promise<{ ok: boolean; message: string }> {
  try {
    const r = await fetch(`${API_URL}/health`, { method: 'GET' })
    const data: HealthResponse = await r.json()
    if (!r.ok) return { ok: false, message: 'API error' }
    if (!data.model_loaded) return { ok: false, message: 'Model not loaded' }
    return { ok: true, message: 'Connected' }
  } catch (e) {
    return { ok: false, message: e instanceof Error ? e.message : 'Cannot reach API' }
  }
}

export async function predictChurn(features: Record<string, unknown>): Promise<Record<string, unknown> | null> {
  try {
    const r = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(features),
    })
    if (!r.ok) {
      const text = await r.text()
      throw new Error(text)
    }
    return await r.json()
  } catch (e) {
    throw e
  }
}

export async function predictBatch(featuresList: Record<string, unknown>[]): Promise<{ predictions: Record<string, unknown>[]; count: number }> {
  const r = await fetch(`${API_URL}/predict/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(featuresList),
  })
  if (!r.ok) throw new Error(await r.text())
  return await r.json()
}
