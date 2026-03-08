import { useState } from 'react'
import { Search, Bell, ChevronDown, Calendar, Menu } from 'lucide-react'
import { cn } from '@/lib/utils'

const dateRanges = [
  { label: 'Last 7 days', value: '7d' },
  { label: 'Last 30 days', value: '30d' },
  { label: 'Last 90 days', value: '90d' },
  { label: 'This year', value: 'ytd' },
]

interface TopNavbarProps {
  onMenuClick?: () => void
}

export function TopNavbar({ onMenuClick }: TopNavbarProps) {
  const [searchFocused, setSearchFocused] = useState(false)
  const [dateRange, setDateRange] = useState('30d')
  const [dateOpen, setDateOpen] = useState(false)

  return (
    <header className="sticky top-0 z-20 flex h-14 shrink-0 items-center gap-2 border-b border-dashboard-border bg-dashboard-dark/80 backdrop-blur-xl px-3 sm:px-4 md:px-6">
      <button
        type="button"
        onClick={onMenuClick}
        className="lg:hidden flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-white/70 hover:bg-white/10 hover:text-white transition-colors"
        aria-label="Open menu"
      >
        <Menu className="h-5 w-5" />
      </button>
      <div className="flex flex-1 items-center gap-2 min-w-0">
        <div
          className={cn(
            'flex h-9 flex-1 min-w-0 max-w-md items-center gap-2 rounded-lg border bg-white/5 px-2 sm:px-3 transition-all duration-200',
            searchFocused ? 'border-dashboard-cyan/40 ring-1 ring-dashboard-cyan/20' : 'border-white/10'
          )}
        >
          <Search className="h-4 w-4 text-white/40 shrink-0" />
          <input
            type="search"
            placeholder="Search..."
            className="h-8 flex-1 min-w-0 bg-transparent text-sm text-white placeholder:text-white/40 focus:outline-none"
            onFocus={() => setSearchFocused(true)}
            onBlur={() => setSearchFocused(false)}
          />
        </div>
        <div className="relative shrink-0">
          <button
            type="button"
            onClick={() => setDateOpen((o) => !o)}
            className="flex h-9 items-center gap-1.5 rounded-lg border border-white/10 bg-white/5 px-2 sm:px-3 text-sm text-white/90 hover:bg-white/10 transition-colors"
          >
            <Calendar className="h-4 w-4 text-white/60 shrink-0" />
            <span className="hidden sm:inline truncate max-w-[100px] md:max-w-none">
              {dateRanges.find((d) => d.value === dateRange)?.label ?? dateRange}
            </span>
            <ChevronDown className="h-4 w-4 text-white/50 shrink-0" />
          </button>
          {dateOpen && (
            <>
              <div className="fixed inset-0 z-10" onClick={() => setDateOpen(false)} aria-hidden />
              <div className="absolute right-0 top-full z-20 mt-1 w-48 rounded-lg border border-white/10 bg-dashboard-panel py-1 shadow-lg">
                {dateRanges.map((d) => (
                  <button
                    key={d.value}
                    type="button"
                    onClick={() => {
                      setDateRange(d.value)
                      setDateOpen(false)
                    }}
                    className="w-full px-3 py-2 text-left text-sm text-white/90 hover:bg-white/5"
                  >
                    {d.label}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
      <div className="flex items-center gap-1 shrink-0">
        <button
          type="button"
          className="relative flex h-9 w-9 items-center justify-center rounded-lg text-white/70 hover:bg-white/5 hover:text-white transition-colors"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-dashboard-cyan" />
        </button>
        <button
          type="button"
          className="flex h-9 items-center gap-2 rounded-lg border border-white/10 bg-white/5 pl-1.5 pr-2 sm:pl-2 sm:pr-3 py-1.5 text-sm text-white/90 hover:bg-white/10 transition-colors min-w-0"
        >
          <div className="h-6 w-6 shrink-0 rounded-full bg-gradient-to-br from-dashboard-cyan to-dashboard-purple" />
          <span className="hidden sm:inline truncate">Account</span>
          <ChevronDown className="h-4 w-4 text-white/50 shrink-0 hidden sm:block" />
        </button>
      </div>
    </header>
  )
}
