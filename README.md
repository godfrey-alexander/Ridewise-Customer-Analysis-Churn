# Ridewise-Customer-Analysis-Churn

This guide explains **what the project is**, **what each page does**, and **how it helps the business** — in plain language. No technical background needed.

---

## Table of Contents

1. [What Is RideWise?](#1-what-is-ridewise)
2. [How the Project Is Organized](#2-how-the-project-is-organized)
3. [Where the Data Comes From](#3-where-the-data-comes-from)
4. [The Dashboard Pages (In Detail)](#4-the-dashboard-pages-in-detail)
5. [The Notebooks (What They’re For)](#5-the-notebooks-what-theyre-for)
6. [How the Pages Work Together](#6-how-the-pages-work-together)
7. [Quick Reference: What Each Page Answers](#7-quick-reference-what-each-page-answers)

---

## 1. What Is RideWise?

**RideWise** is a ride-hailing analytics project. It has two main parts:

- **A web dashboard** — Several pages where you can explore trips, demand, revenue, at-risk customers, and where rides start and end on a map.
- **Notebooks** — Step-by-step analyses that check the data and explore business questions before the dashboard was built.

**In one sentence:** The dashboard helps you see how the business is doing (who’s riding, when, where, and how much money is at risk if customers stop riding).

---


## 2. The Notebooks (What They’re For)

The project includes two Jupyter notebooks. They don’t run inside the dashboard — they’re separate step-by-step analyses.

### Notebook 01: Dataset Exploration & Feature Selection

**What it’s for**  
To **check the raw data** before any modeling. It loads the original tables (riders, trips, sessions, promotions, drivers), looks at their structure, checks for duplicates and missing values, and figures out how the tables should be linked. The main idea: in the end, we care about **one row per customer (rider)**; trip-level and session-level data are combined and summarized before being attached to each customer.

**Why it matters**  
It makes sure the data is understood and linked correctly so that later work (e.g. building the trip file and customer segments that feed the dashboard) is built on a solid base.

### Notebook 02: EDA for Business Context

**What it’s for**  
To **explore the data** and answer business questions, for example:

- What does the customer base look like (e.g. age, city)?
- When is demand highest?
- Which users are most profitable?
- Which cities should marketing focus on?
- Does surge pricing affect churn?
- How do trip distance and time relate to price?
- What drives tipping?
- How stable is the customer base in terms of churn?

**Why it matters**  
It decides which metrics and segments matter for the business. The dashboard’s Overview, Demand, and Revenue pages turn some of these into interactive charts; the Exposure page uses customer segments in the same spirit (who’s valuable, who’s at risk).

---


## 3. Where the Data Comes From

### What the dashboard uses

- **Trip data** — One row per ride. It includes things like: when the ride was, which city, how much was paid, and whether the rider is Bronze/Silver/Gold. This powers the **Overview**, **Demand**, and **Revenue** pages.
- **Customer-segment data** — One row per customer, with how recently they rode, how often, how much they spent, and a label like “Regular Commuter” or “At Risk.” This powers the **Exposure** page.

The app reads these from CSV files that were already prepared (with dates and segments calculated). The dashboard does **not** change the files — it only filters and sums for the charts and tables you see.

### One important detail

- **Map Hotspots** uses its own data file and its own path. It doesn’t use the same date or city filters as the other pages, so the map is a fixed view of where pickups and dropoffs concentrate.

### Do filters carry over between pages?

**No.** If you choose “Nairobi” on the Overview page, then open Demand Analysis, Demand will still show all cities until you change the filters on that page. Each page has its own filters.

---

## 4. The Dashboard Pages (In Detail)

---

### Home Page

**What it’s for**  
Your starting point. It briefly explains the app and tells you to use the **sidebar** to open other pages. It also loads the main trip data in the background so the next pages open quickly.

**What you see**  
A short title, a list of what the app can do, and a note: “Use the sidebar to navigate between pages.” No charts or filters.

**What you do**  
Read the intro and click any page name in the sidebar to go there.

**Why it matters**  
It makes the app feel faster when you open other pages and sets the expectation that navigation happens through the sidebar.

---

### Overview Page

**What it’s for**  
Answers: **“What does our rideshare business look like at a glance?”** You see total users, trips, revenue, how customers are split by loyalty tier (e.g. Bronze, Silver, Gold), and how they’re spread across cities.

**What you see**

- **Filters (sidebar):** City and Loyalty Tier. You can pick one or more of each; default is “all.”
- **Top numbers:** Total Users (note: this value is currently fixed at 10,000 and does not change with filters), Total Trips, and Revenue.
- **Two charts:**  
  - A **pie chart** — Share of users in each loyalty tier.  
  - A **bar chart** — How many users are in each city.

**What you do**  
Change City and/or Loyalty Tier. The totals (except Total Users) and both charts update to only the cities and tiers you selected. You can compare, for example, “just Nairobi” vs “all cities” or “only Gold” vs “everyone.”

**What data it uses**  
The same trip data as Demand and Revenue. The page keeps only the rows that match your chosen cities and loyalty tiers, then counts users and trips and sums revenue.

**Why it matters**  
You get a quick sense of scale (how many trips, how much revenue) and mix (loyalty and geography). Good for questions like “Which city has the most users?” or “What share of users are in each loyalty tier?”

---

### Demand Analysis Page

**What it’s for**  
Answers: **“When do rides happen?”** You see how many trips occur **each hour of the day** and **each day** in the period you pick. That helps with driver scheduling and spotting busy times.

**What you see**

- **Filters (sidebar):** Year, Month, and Cities. Defaults are set (e.g. one year, one month, all cities).
- **Top numbers:** Total Users, Total Trips, Revenue, and Average Fare.
- **Two charts:**  
  - **Bar chart** — Trips per hour (0–23). Shows which hours are busiest.  
  - **Line chart** — Trips per day over the chosen month. Shows how demand changes day by day.

**What you do**  
Change Year, Month, and/or Cities. All four numbers and both charts update. You can compare, for example, “May in Nairobi” vs “September in all cities.”

**What data it uses**  
The same trip data. The page keeps only trips in your selected year, month, and cities, then counts trips by hour and by day. No extra business rules — just counts.

**Why it matters**  
You see peak hours and days so you can plan driver supply and pricing. Useful for spotting patterns (e.g. weekday vs weekend, morning vs evening).

---

### Revenue Analysis Page

**What it’s for**  
Answers: **“How does revenue change over time?”** You see **revenue by hour** and **revenue by day** for the period you choose. Same idea as Demand, but focused on **money** instead of trip counts.

**What you see**

- **Filters (sidebar):** Same as Demand — Year, Month, Cities.
- **Top numbers:** Same four — Total Users, Total Trips, Revenue, Average Fare.
- **Two charts:**  
  - **Bar chart** — Revenue per hour. Which hours make the most money.  
  - **Line chart** — Revenue per day over the month. How revenue changes day by day.

**What you do**  
Same as Demand: change the filters and everything updates. You can compare this page with Demand to see if “busy” times are also “high-revenue” times.

**What data it uses**  
Same trip data and same filters as Demand. The page sums fare (and tip where relevant) by hour and by day instead of counting trips.

**Why it matters**  
You see which hours and days bring in the most revenue. Used together with Demand, you can tell if high demand also means high revenue (e.g. because of pricing or surge).

---

### Exposure Analysis Page

**What it’s for**  
Answers: **“How much revenue could we lose if we don’t win back customers who might be drifting away?”** You choose a **number of days** (e.g. “customers who haven’t ridden in 7 days”). The page then shows how much revenue those customers represent and breaks it down by **customer segment**. You also get a list of those customers for re-engagement (e.g. emails or offers).

**What you see**

- **Filter (sidebar):** A **slider** — “Days since last activity.” You can pick from 7 up to 90 days (in steps of 7). Default is 7.
- **Top row:**  
  - **Revenue at Risk** — Total revenue linked to the “at risk” customers (in £).  
  - **Customers Exposed** — How many customers that is.  
  - **Date Range** — The range of “last trip” dates for those customers.
- **Treemap** — Each block is a customer segment (e.g. “Regular Commuters”, “At Risk Users”). The size of the block shows how much of the “revenue at risk” comes from that segment. Hover to see the amount.
- **Table** — The list of at-risk customers so you can see who they are (e.g. for targeting campaigns).

**What you do**  
Move the slider to different values (e.g. 7, 14, 30, 90 days). The numbers, treemap, and table all update. A higher number of days usually means more customers and more “revenue at risk.”

**What data it uses**  
A separate file with one row per customer: how many days since their last trip (recency), how often they ride (frequency), how much they’ve spent (monetary), and a segment label. The page uses your chosen “days since last activity” to decide who counts as “at risk,” then sums their past revenue and groups by segment.

**One note**  
The page caption describes revenue lost if customers *inactive* for that many days are not re-engaged. The way “at risk” is calculated in the app (which customers are included when you move the slider) should match that idea. If you ever feel the numbers don’t match the caption (e.g. you expect “inactive 30+ days” but see different customers), it’s worth checking with whoever maintains the app so the logic and the wording stay aligned.

**Why it matters**  
You can decide how much to invest in re-engagement by seeing how much revenue is tied to potentially inactive customers. The treemap shows which segments matter most; the table tells you who to contact.

---

### Map Hotspots Page

**What it’s for**  
Answers: **“Where do pickups and dropoffs concentrate?”** Two maps show **pickup** and **dropoff** hotspots (denser areas appear as darker or larger hexagons). Useful for deciding where to position drivers or run local campaigns.

**What you see**

- A title: “Pickup & Dropoff Hotspots Map.”
- **First map** — Pickup hotspots. Darker/bigger hexagons = more pickups in that area.
- **Second map** — Dropoff hotspots. Same idea for dropoffs.
- No filters in the sidebar on this page.

**What you do**  
Pan and zoom on each map to explore. The maps don’t change when you change filters on other pages; this page uses its own data and a fixed snapshot.

**What data it uses**  
A separate data file that contains pickup and dropoff locations. The app doesn’t use the same date or city filters as the other pages here, so what you see is one fixed view. (Technically, the file path is set inside the app and may point to a specific folder on one machine; if the map doesn’t load elsewhere, the path may need to be updated.)

**Why it matters**  
You see where rides start and end so you can plan driver placement and local promotions.

---


## 5. How the Pages Work Together

- **Home** — Entry point; loads data so other pages are fast; directs you to the sidebar.
- **Overview** — Big picture: users, trips, revenue, loyalty, cities. Same underlying trip data as Demand and Revenue.
- **Demand Analysis** and **Revenue Analysis** — Same filters (year, month, cities). One shows **when rides happen** (counts); the other shows **when money comes in** (revenue). Use them together to see if busy times are also profitable times.
- **Exposure Analysis** — Uses customer-segment data. Shows **how much revenue is at risk** if you don’t re-engage certain customers and **who those customers are** (by segment and in a table).
- **Map Hotspots** — Standalone. Shows **where** pickups and dropoffs concentrate; uses its own data and no shared filters.

**Remember:** Filters are **not** shared. Each page only uses its own sidebar choices.

---

## 6. Quick Reference: What Each Page Answers

| Page | Main question | What you can do |
|------|----------------|-----------------|
| **Home** | Where do I go? | Use the sidebar to open any page |
| **Overview** | What does the business look like at a glance? | Filter by city and loyalty → see totals and pie/bar charts |
| **Demand Analysis** | When do rides happen? | Filter by year, month, cities → see trips by hour and by day |
| **Revenue Analysis** | When does revenue come in? | Same filters → see revenue by hour and by day |
| **Exposure Analysis** | How much revenue is at risk if we don’t re-engage customers? | Move the “days since last activity” slider → see revenue at risk, treemap by segment, and customer list |
| **Map Hotspots** | Where do pickups and dropoffs concentrate? | Pan and zoom on the two maps |

---

For step-by-step **how to use** the app (without technical detail), see **Read Me.md** in the dashboard folder.
