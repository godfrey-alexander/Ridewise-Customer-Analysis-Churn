import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { AlertTriangle, TrendingUp, Zap } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface InsightItem {
  id: string
  type: 'anomaly' | 'trend' | 'opportunity'
  title: string
  description: string
  value?: string
  severity?: 'low' | 'medium' | 'high'
}

interface InsightsPanelProps {
  insights: InsightItem[]
  className?: string
}

const typeConfig = {
  anomaly: { icon: AlertTriangle, color: 'text-risk-high', bg: 'bg-risk-high/10' },
  trend: { icon: TrendingUp, color: 'text-risk-low', bg: 'bg-risk-low/10' },
  opportunity: { icon: Zap, color: 'text-dashboard-cyan', bg: 'bg-dashboard-cyan/10' },
}

export function InsightsPanel({ insights, className }: InsightsPanelProps) {
  return (
    <Card className={cn('', className)}>
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-medium text-white flex items-center gap-2">
          <Zap className="h-4 w-4 text-dashboard-cyan" />
          Insights
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {insights.length === 0 ? (
          <p className="text-sm text-white/50">No insights for the current filters.</p>
        ) : (
          insights.slice(0, 5).map((item) => {
            const config = typeConfig[item.type]
            const Icon = config.icon
            return (
              <div
                key={item.id}
                className={cn(
                  'rounded-lg border border-white/10 p-3 transition-colors hover:border-white/20',
                  config.bg
                )}
              >
                <div className="flex items-start gap-2">
                  <Icon className={cn('h-4 w-4 shrink-0 mt-0.5', config.color)} />
                  <div>
                    <p className="text-sm font-medium text-white">{item.title}</p>
                    <p className="text-xs text-white/60 mt-0.5">{item.description}</p>
                    {item.value && (
                      <p className="text-xs font-mono text-dashboard-cyan mt-1">{item.value}</p>
                    )}
                  </div>
                </div>
              </div>
            )
          })
        )}
      </CardContent>
    </Card>
  )
}
