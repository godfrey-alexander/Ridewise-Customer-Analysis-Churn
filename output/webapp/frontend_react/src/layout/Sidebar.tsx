import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  BarChart3,
  PieChart,
  AlertTriangle,
  Brain,
  Database,
  Settings,
  Car,
  X,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Home' },
  { to: '/overview', icon: PieChart, label: 'Overview' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/insights', icon: AlertTriangle, label: 'Insights' },
  { to: '/predictions', icon: Brain, label: 'Predictions' },
  // { to: '/data-explorer', icon: Database, label: 'Data Explorer' },
  { to: '/settings', icon: Settings, label: 'Settings' },
]

interface SidebarProps {
  open?: boolean
  onClose?: () => void
  children?: React.ReactNode
}

export function Sidebar({ open = true, onClose, children }: SidebarProps) {
  return (
    <>
      {/* Mobile overlay when sidebar is open */}
      {onClose && (
        <div
          aria-hidden
          className={cn(
            'fixed inset-0 z-30 bg-black/60 backdrop-blur-sm transition-opacity lg:hidden',
            open ? 'opacity-100' : 'pointer-events-none opacity-0'
          )}
          onClick={onClose}
        />
      )}
      <aside
        className={cn(
          'fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-dashboard-border bg-dashboard-panel/95 backdrop-blur-xl transition-transform duration-300 ease-out',
          'lg:translate-x-0',
          open ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex h-14 shrink-0 items-center justify-between gap-2 border-b border-dashboard-border px-4">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-dashboard-cyan/20 to-dashboard-purple/20 border border-dashboard-border">
              <Car className="h-5 w-5 text-dashboard-cyan" />
            </div>
            <span className="font-semibold text-white truncate">RideWise</span>
          </div>
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="lg:hidden flex h-9 w-9 items-center justify-center rounded-lg text-white/70 hover:bg-white/10 hover:text-white transition-colors"
              aria-label="Close menu"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
        <nav className="flex-1 space-y-0.5 overflow-y-auto p-3">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              onClick={onClose}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                  isActive
                    ? 'bg-dashboard-cyan/10 text-dashboard-cyan border border-dashboard-cyan/20'
                    : 'text-white/70 hover:bg-white/5 hover:text-white border border-transparent'
                )
              }
            >
              <item.icon className="h-4 w-4 shrink-0" />
              <span className="truncate">{item.label}</span>
            </NavLink>
          ))}
        </nav>
        {children && (
          <div className="shrink-0 border-t border-dashboard-border p-3">
            {children}
          </div>
        )}
      </aside>
    </>
  )
}
