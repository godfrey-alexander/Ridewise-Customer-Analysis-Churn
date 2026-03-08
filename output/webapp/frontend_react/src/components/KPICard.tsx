import { Area, AreaChart, ResponsiveContainer } from 'recharts'
import { Card, CardContent } from '@/components/ui/Card'
import { cn, formatNumber } from '@/lib/utils'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface KPICardProps {
  title: string
  value: string | number
  delta?: number
  sparklineData?: { value: number }[]
  icon?: React.ReactNode
  className?: string
}

export function KPICard({ title, value, delta, sparklineData, icon, className }: KPICardProps) {
  return (
    <Card className={cn('card-hover overflow-hidden', className)}>
      <CardContent className="p-4 sm:p-5 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <p className="text-xs sm:text-sm font-medium text-white/60 truncate">{title}</p>
            <p className="mt-1 text-lg sm:text-2xl font-semibold tracking-tight text-white truncate">
              {typeof value === 'number' ? formatNumber(value) : value}
            </p>
            {delta !== undefined && (
              <div
                className={cn(
                  'mt-1.5 flex items-center gap-1 text-xs font-medium',
                  delta >= 0 ? 'text-risk-low' : 'text-risk-critical'
                )}
              >
                {delta >= 0 ? <TrendingUp className="h-3.5 w-3" /> : <TrendingDown className="h-3.5 w-3" />}
                {delta >= 0 ? '+' : ''}{delta}% vs last period
              </div>
            )}
          </div>
          {icon && (
            <div className="rounded-lg bg-dashboard-cyan/10 p-2 text-dashboard-cyan">
              {icon}
            </div>
          )}
        </div>
        {sparklineData && sparklineData.length > 0 && (
          <div className="mt-4 h-12 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={sparklineData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="sparkline" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="rgba(0, 217, 255, 0.4)" />
                    <stop offset="100%" stopColor="rgba(0, 217, 255, 0)" />
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke="rgba(0, 217, 255, 0.6)"
                  strokeWidth={1.5}
                  fill="url(#sparkline)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
