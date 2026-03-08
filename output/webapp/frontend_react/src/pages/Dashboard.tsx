import { Link } from 'react-router-dom'
import { LayoutDashboard, BarChart3, AlertTriangle, Brain, Database, ArrowRight } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'

const sections = [
  {
    to: '/overview',
    icon: LayoutDashboard,
    title: 'Overview',
    desc: 'Total users, trips, revenue, and how customers split by loyalty tier and city.',
  },
  {
    to: '/analytics',
    icon: BarChart3,
    title: 'Analytics',
    desc: 'Demand and revenue by hour and day. Plan drivers and spot peaks.',
  },
  {
    to: '/insights',
    icon: AlertTriangle,
    title: 'Insights',
    desc: 'Revenue at risk if customers go inactive; segments and who to re-engage.',
  },
  {
    to: '/predictions',
    icon: Brain,
    title: 'Predictions',
    desc: 'Churn risk for riders from RFMS and engagement features.',
  },
  // {
  //   to: '/data-explorer',
  //   icon: Database,
  //   title: 'Data Explorer',
  //   desc: 'Browse and filter trip and segment data.',
  // },
]

export function Dashboard() {
  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
          Rideshare Executive Dashboard
        </h1>
        <p className="mt-2 text-sm text-white/70 max-w-2xl sm:text-base">
          End-to-end applied data science: analytics, modeling, explainability, and production deployment.
        </p>
        <p className="mt-1 text-sm text-white/50">Developed by Godfrey Alexander Abban</p>
      </div>

      <Card className="border-dashboard-cyan/20 bg-dashboard-cyan/5">
        <CardContent className="p-4 flex items-start gap-3">
          <div className="rounded-lg bg-dashboard-cyan/20 p-2">
            <LayoutDashboard className="h-5 w-5 text-dashboard-cyan" />
          </div>
          <p className="text-sm text-white/90">
            Use the <strong>sidebar</strong> to move between Overview, Analytics, Insights, Predictions, and Data Explorer.
          </p>
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {sections.map((s) => (
          <Link key={s.to} to={s.to}>
            <Card className="card-hover h-full group cursor-pointer">
              <CardHeader className="flex flex-row items-center gap-3 pb-2">
                <div className="rounded-lg bg-white/10 p-2 group-hover:bg-dashboard-cyan/20 transition-colors">
                  <s.icon className="h-5 w-5 text-dashboard-cyan" />
                </div>
                <CardTitle className="text-base font-medium text-white group-hover:text-dashboard-cyan transition-colors">
                  {s.title}
                </CardTitle>
                <ArrowRight className="h-4 w-4 ml-auto text-white/40 group-hover:text-dashboard-cyan group-hover:translate-x-1 transition-all" />
              </CardHeader>
              <CardContent className="pt-0">
                <p className="text-sm text-white/60">{s.desc}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
