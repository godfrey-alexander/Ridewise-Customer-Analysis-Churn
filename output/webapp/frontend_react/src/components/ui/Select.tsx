import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  options: { value: string; label: string }[]
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, options, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        'flex h-10 w-full rounded-lg border border-white/15 bg-white/5 px-3 py-2 text-sm text-white',
        'focus:outline-none focus:ring-2 focus:ring-dashboard-cyan/40 focus:border-dashboard-cyan/30',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value} className="bg-dashboard-panel text-white">
          {opt.label}
        </option>
      ))}
    </select>
  )
)
Select.displayName = 'Select'
export { Select }
