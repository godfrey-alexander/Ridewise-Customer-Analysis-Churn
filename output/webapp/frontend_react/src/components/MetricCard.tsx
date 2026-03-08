import { Card, CardContent } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

interface MetricCardProps {
  title: string
  value: string | number
  delta?: number
  prefix?: string
  suffix?: string
  className?: string
}

export function MetricCard({ title, value, prefix = '', suffix = '', delta, className }: MetricCardProps) {
  const displayValue = typeof value === 'number' ? `${prefix}${value.toLocaleString()}${suffix}` : `${prefix}${value}${suffix}`
  return (
    <Card className={cn('card-hover', className)}>
      <CardContent className="p-4 sm:p-5 text-center min-w-0">
        <p className="text-xs sm:text-sm font-medium text-white/60 truncate">{title}</p>
        <p className="mt-1 text-lg sm:text-2xl font-semibold text-white truncate" title={displayValue}>{displayValue}</p>
        {delta !== undefined && (
          <p className={cn('mt-1 text-xs font-medium', delta >= 0 ? 'text-risk-low' : 'text-risk-critical')}>
            {delta >= 0 ? '▲' : '▼'} {Math.abs(delta)}%
          </p>
        )}
      </CardContent>
    </Card>
  )
}
