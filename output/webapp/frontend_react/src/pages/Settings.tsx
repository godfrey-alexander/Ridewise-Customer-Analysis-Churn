import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Input } from '@/components/ui/Input'

export function Settings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-2xl">
      <div>
        <h1 className="text-xl font-bold text-white sm:text-2xl">Settings</h1>
        <p className="text-sm text-white/60 mt-0.5">App and API configuration</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">API</CardTitle>
          <p className="text-sm text-white/60">Churn prediction backend URL (e.g. http://localhost:8000)</p>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="mb-1 block text-xs text-white/50">API URL</label>
            <Input
              placeholder="http://localhost:8000"
              defaultValue={import.meta.env?.VITE_API_URL ?? ''}
              readOnly
              className="bg-white/5"
            />
            <p className="text-xs text-white/40 mt-1">Set VITE_API_URL at build time to change.</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Data</CardTitle>
          <p className="text-sm text-white/60">CSV data is loaded from /data/riders_trips.csv and /data/rfm_data.csv</p>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-white/70">
            Place riders_trips.csv and rfm_data.csv in the <code className="rounded bg-white/10 px-1">public/data</code> folder.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">About</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-white/70">
          <p>RideWise Dashboard — Applied data science for ride-sharing analytics.</p>
          <p className="mt-2">Developed by Godfrey Alexander Abban.</p>
        </CardContent>
      </Card>
    </div>
  )
}
