# RideWise Dashboard — User Guide

This guide explains what the dashboard is for and what you can do on each page. No technical background needed.

---

## 1. What Is This App?

The **RideWise Dashboard** is a multi-page app that helps you understand your rideshare business using your trip data. You can:

- **See the big picture** — total users, trips, revenue, and where your customers are (Overview).
- **See when rides happen** — by hour and by day (Demand Analysis).
- **See when money comes in** — revenue by hour and by day (Revenue Analysis).
- **See revenue at risk** — if customers stop riding, how much could you lose, and who those customers are (Exposure Analysis).
- **See where rides start and end** — pickup and dropoff hotspots on a map (Map Hotspots).

You don’t need to know how the data is loaded or stored; you just use the sidebar to open a page and the filters on that page to explore.

---

## 2. How to Get Around

- **Sidebar (left):** Use it to switch between pages. Click **Home**, **Overview**, **Demand Analysis**, **Revenue Analysis**, **Exposure Analysis**, or **Map Hotspots**.
- **Filters:** Many pages have filters in the sidebar (e.g. city, year, month). When you change a filter, the numbers and charts on that page update automatically.
- **No shared filters:** What you choose on one page (e.g. Overview) does not change another page (e.g. Demand Analysis). Each page has its own filters.

---

## 3. How the Pages Work Together

- **Home** is the starting point and explains navigation.
- **Overview** gives you the big picture (users, trips, revenue, loyalty, cities). Use it when you want a quick summary or to compare cities/loyalty tiers.
- **Demand Analysis** and **Revenue Analysis** both use the same type of filters (year, month, cities) but show different things: Demand = *when* rides happen (counts), Revenue = *when* money comes in. Use them together to see if busy times are also high-revenue times.
- **Exposure Analysis** focuses on “at risk” customers and how much revenue they represent. Use it to prioritize re-engagement and see which segments to focus on.
- **Map Hotspots** is separate: it shows *where* rides happen on a map and doesn’t use the same filters as the other pages. Use it when you care about geography and hotspots.

Filters on one page do **not** affect another. For example, if you select “Nairobi” on Overview, then open Demand Analysis, Demand will still show all cities until you change its own filters. Each page is independent.

## 4. Home Page

### What it’s for

The Home page is your starting point. It briefly explains what the app does and tells you to use the **sidebar** to open other pages. It also loads the main data in the background so other pages open quickly when you click them.

### What you’ll see

- A short title and description of the app.
- A note: **“Use the sidebar to navigate between pages.”**
- No charts, tables, or filters — just text and the sidebar.

### What you can do

- Read the intro.
- Click any page name in the sidebar to go to that page.

---

## 5. Overview Page

### What it’s for

Overview answers: **“What does our rideshare business look like at a glance?”** It shows how many users and trips you have, how much revenue you make, how customers are split by loyalty tier, and how they’re spread across cities. Good for a quick summary or for comparing different cities or loyalty groups.

### What you’ll see

- **At the top:** Three summary numbers in cards:
  - **Total Users**
  - **Total Trips**
  - **Revenue**
- **In the sidebar:** Two filters:
  - **City** — choose one or more cities (default: all).
  - **Loyalty Tier** — choose one or more tiers (default: all).
- **Charts:**
  - A **pie chart** showing the share of users in each loyalty tier (e.g. Bronze, Silver, Gold).
  - A **horizontal bar chart** showing how many users are in each city.

### What you can do

- Change **City** and/or **Loyalty Tier** in the sidebar. The totals (except Total Users) and both charts update to show only the selected cities and tiers.
- Use this to compare, for example, “just Nairobi” vs “all cities” or “only Gold members” vs “everyone.”

### Why it’s useful

- Get a quick sense of scale (trips, revenue) and mix (loyalty, geography).
- Answer questions like: “Which city has the most users?” or “What share of our users are in each loyalty tier?”

---

## 6. Demand Analysis Page

### What it’s for

Demand Analysis answers: **“When do rides happen?”** It shows how many trips you get **each hour of the day** and **each day** in the period you pick. That helps you plan driver supply, peak hours, and busy days.

### What you’ll see

- **At the top:** Four summary cards:
  - **Total Users**
  - **Total Trips**
  - **Revenue**
  - **Avg Fare**
- **In the sidebar:** Three filters:
  - **Year** (default: first year in the data).
  - **Month** (default: often May, depending on data).
  - **Cities** (default: all).
- **Charts:**
  - A **bar chart** of trips per hour (0–23). Shows which hours are busiest.
  - A **line chart** of trips per day over the chosen month. Shows how demand changes day by day.

### What you can do

- Change **Year**, **Month**, and/or **Cities**. All four numbers and both charts update to match your selection.
- Use this to compare different months or cities (e.g. “May in Nairobi” vs “September in all cities”).

### Why it’s useful

- Find peak hours and days so you can schedule more drivers or adjust pricing.
- Spot patterns (e.g. weekday vs weekend, morning vs evening).

---

## 7. Revenue Analysis Page

### What it’s for

Revenue Analysis answers: **“How does revenue change over time?”** It shows **revenue by hour of day** and **revenue by day** for the period you choose. It’s the money view of your business; Demand Analysis is the trip-count view. Same filters (year, month, cities) so you can compare the two pages easily.

### What you’ll see

- **At the top:** Same four cards as Demand Analysis — Total Users, Total Trips, Revenue, Avg Fare.
- **In the sidebar:** Same three filters — Year, Month, Cities (same defaults as Demand).
- **Charts:**
  - A **bar chart** of revenue per hour. Shows which hours make the most money.
  - A **line chart** of revenue per day over the chosen month. Shows how revenue changes day by day.

### What you can do

- Change Year, Month, and/or Cities. All numbers and charts update.
- Compare with the Demand Analysis page: e.g. “Lots of trips at 8am but revenue is also high then” helps you understand when demand and revenue line up.

### Why it’s useful

- See which hours and days bring in the most revenue.
- Use it together with Demand to understand if high demand also means high revenue (e.g. pricing or surge effects).

---

## 8. Exposure Analysis Page

### What it’s for

Exposure Analysis answers: **“How much revenue could we lose if we don’t win back customers who might be drifting away?”** You choose a **number of days** (e.g. “customers who haven’t ridden in 7 days”). The page then shows how much revenue those customers represent and breaks it down by **customer segment** (e.g. “Regular Commuters,” “At Risk Users”). You also get a list of those customers so you can target re-engagement (e.g. emails or offers).

### What you’ll see

- **In the sidebar:** A **slider** — “Days since last activity.” You can pick from 7 up to 90 days (in steps of 7). Default is 7.
- **At the top:** Three pieces of info:
  - **Revenue at Risk** — total revenue linked to the “at risk” customers (shown in pounds £).
  - **Customers Exposed** — how many customers that is.
  - **Date Range** — the range of “last trip” dates for those customers.
- **Charts and table:**
  - A **treemap** — each block is a customer segment; the size of the block shows how much of the “revenue at risk” comes from that segment. You can hover to see the amount.
  - A **table** — the list of at-risk customers (without the “last trip” date column) so you can see who they are.

### What you can do

- Move the **slider** to different values (e.g. 7, 14, 30, 90 days). The numbers, treemap, and table all update. A higher number of days usually means more customers and more “revenue at risk.”

### Why it’s useful

- Decide how much to invest in re-engagement (emails, discounts, etc.) by seeing how much revenue is tied to potentially inactive customers.
- See which segments matter most (big blocks in the treemap) and who to contact (the table).

---

## 9. Map Hotspots Page

### What it’s for

Map Hotspots answers: **“Where do pickups and dropoffs concentrate?”** It shows two maps: one where **pickups** are most common (hexagon hotspots) and one where **dropoffs** are most common. Useful for deciding where to position drivers or run local campaigns. This page uses its own dataset and does not use the same date or city filters as the other pages — it’s a fixed snapshot.

### What you’ll see

- A title: **“Pickup & Dropoff Hotspots Map.”**
- **First map:** Pickup hotspots — darker/bigger hexagons = more pickups in that area.
- **Second map:** Dropoff hotspots — same idea for dropoffs.
- No filters in the sidebar on this page.

### What you can do

- **Pan and zoom** on each map to explore. You can move around and zoom in to see specific areas.
- The maps don’t change when you go to other pages or change filters elsewhere; what you see is based on a single dataset loaded for this page.

### Why it’s useful

- Find busy areas for pickups and dropoffs to plan where to have more drivers or where to promote the service.

---

*End of User Guide. For technical details (data sources, code structure), see the development team or the codebase.*
