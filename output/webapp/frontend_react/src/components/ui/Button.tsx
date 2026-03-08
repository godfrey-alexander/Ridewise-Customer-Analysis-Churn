import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'gradient'
  size?: 'sm' | 'md' | 'lg'
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', ...props }, ref) => {
    const base =
      'inline-flex items-center justify-center rounded-lg font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-dashboard-cyan/50 disabled:pointer-events-none disabled:opacity-50'
    const variants = {
      default: 'bg-white/10 text-white hover:bg-white/20 border border-white/20',
      outline: 'border border-dashboard-border bg-transparent hover:bg-white/5',
      ghost: 'hover:bg-white/5',
      gradient:
        'bg-gradient-to-r from-dashboard-cyan to-dashboard-purple text-white border-0 font-mono hover:shadow-glow hover:-translate-y-0.5 active:translate-y-0',
    }
    const sizes = {
      sm: 'h-8 px-3 text-sm',
      md: 'h-10 px-5 text-sm',
      lg: 'h-12 px-6 text-base',
    }
    return (
      <button
        ref={ref}
        className={cn(base, variants[variant], sizes[size], className)}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'
export { Button }
