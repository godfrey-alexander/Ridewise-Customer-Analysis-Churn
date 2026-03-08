import { Card, CardContent } from '@/components/ui/Card'
import { Calendar } from 'lucide-react'
import { cn } from '@/lib/utils'

interface DateCardProps {
  dateMin: string
  dateMax: string
  className?: string
}

export function DateCard({ dateMin, dateMax, className }: DateCardProps) {
  return (
    <Card className={cn('card-hover', className)}>
      <CardContent className="p-5 flex items-center gap-3">
        <div className="rounded-lg bg-white/10 p-2">
          <Calendar className="h-5 w-5 text-dashboard-cyan" />
        </div>
        <div>
          <p className="text-sm font-medium text-white/60">Date Range</p>
          <p className="text-lg font-semibold text-white">
            {dateMax} — {dateMin}
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
