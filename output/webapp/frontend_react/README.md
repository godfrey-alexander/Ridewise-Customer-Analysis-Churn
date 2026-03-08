# RideWise Dashboard — React

A futuristic analytics dashboard for RideWise ride-sharing: dark theme, glassmorphism, Recharts, and Shadcn-style components.

## Stack

- **React 18** + **TypeScript** + **Vite**
- **Tailwind CSS** — dark theme, gradients, glow
- **Recharts** — line, bar, pie charts
- **Lucide React** — icons
- **React Router** — navigation
- **PapaParse** — CSV loading

## Structure

```
frontend_react/
├── public/
│   └── data/           # riders_trips.csv, rfm_data.csv (copy from frontend/data)
├── src/
│   ├── components/     # KPICard, ChartCard, DataTable, MetricCard, DateCard, InsightsPanel
│   ├── components/ui/  # Card, Button, Input, Select, Tabs, Dialog, Badge
│   ├── layout/        # Sidebar, TopNavbar, DashboardLayout
│   ├── lib/            # utils, api, data (CSV loaders)
│   ├── pages/          # Dashboard, Overview, DemandRevenue, ExposureAnalysis, ChurnPredictor, DataExplorer, Settings
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
```

## Run

1. **Data:** Ensure `public/data/riders_trips.csv` and `public/data/rfm_data.csv` exist (copy from `frontend/data` if needed).

2. **Backend (for Churn Predictor):** Start the FastAPI backend from the project root:
   ```bash
   uvicorn backend.main:app --reload
   ```

3. **Frontend:**
   ```bash
   npm install
   npm run dev
   ```
   Open http://localhost:5174

4. **API URL:** Set `VITE_API_URL` (e.g. `http://localhost:8000`) when building if the backend is on another host.

## Pages

| Route         | Description |
|--------------|-------------|
| `/`          | Home — intro and links to all sections |
| `/overview`  | Executive summary — users, trips, revenue; city & loyalty filters; pie and bar charts |
| `/analytics` | Demand & revenue — year/month/city filters; hourly/daily demand and revenue charts |
| `/insights`  | Exposure — inactivity slider; revenue at risk; segment bar chart; at-risk customer table |
| `/predictions` | Churn — single predict (form + modal), batch CSV upload, About tab |
| `/data-explorer` | Trips and RFM tables with filters |
| `/settings`  | API URL and data info |

## Design

- **Theme:** Dark with cyan/purple gradients and soft glow.
- **Layout:** Fixed sidebar (Home, Overview, Analytics, Insights, Predictions, Data Explorer, Settings) + top bar (search, date range, notifications, profile).
- **Components:** Card-based KPIs, chart cards, sortable/filterable data tables, risk badges, gradient primary button.

Developed by Godfrey Alexander Abban.
