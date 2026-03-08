import { Routes, Route, Navigate } from 'react-router-dom'
import { DashboardLayout } from '@/layout/DashboardLayout'
import { Dashboard } from '@/pages/Dashboard'
import { Overview } from '@/pages/Overview'
import { DemandRevenue } from '@/pages/DemandRevenue'
import { ExposureAnalysis } from '@/pages/ExposureAnalysis'
import { ChurnPredictor } from '@/pages/ChurnPredictor'
// import { DataExplorer } from '@/pages/DataExplorer'
import { Settings } from '@/pages/Settings'

function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="overview" element={<Overview />} />
        <Route path="analytics" element={<DemandRevenue />} />
        <Route path="insights" element={<ExposureAnalysis />} />
        <Route path="predictions" element={<ChurnPredictor />} />
        {/* <Route path="data-explorer" element={<DataExplorer />} /> */}
        <Route path="settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
