import { cn } from '@/lib/utils'

type RiskVariant = 'low' | 'medium' | 'high' | 'critical' | 'default'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: RiskVariant
}

const variantStyles: Record<RiskVariant, string> = {
  low: 'bg-risk-low/20 text-risk-low border-risk-low/40',
  medium: 'bg-risk-medium/20 text-risk-medium border-risk-medium/40',
  high: 'bg-risk-high/20 text-risk-high border-risk-high/40',
  critical: 'bg-risk-critical/20 text-risk-critical border-risk-critical/40',
  default: 'bg-white/10 text-white/90 border-white/20',
}

function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-medium',
        variantStyles[variant],
        className
      )}
      {...props}
    />
  )
}
export { Badge }
