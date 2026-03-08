import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { cn } from '@/lib/utils'

interface ChartCardProps {
  title: string
  description?: string
  children: React.ReactNode
  className?: string
}

export function ChartCard({ title, description, children, className }: ChartCardProps) {
  return (
    <Card className={cn('card-hover', className)}>
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-medium text-white">{title}</CardTitle>
        {description && (
          <p className="text-xs text-white/50 mt-0.5">{description}</p>
        )}
      </CardHeader>
      <CardContent className="pt-0">{children}</CardContent>
    </Card>
  )
}
