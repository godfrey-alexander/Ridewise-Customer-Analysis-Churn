# RideWise Dashboard

A simple, interactive dashboard for a ride-sharing business. Explore trips and revenue, see where money is at risk, and predict which riders might leave—so you can act before they do.

**Developed by Godfrey Alexander Abban**

---

## What is this?

RideWise Dashboard is a **web app** that turns ride-sharing data into clear charts and numbers. You can:

- **See the big picture** — How many users and trips you have, how much revenue you make, and how customers are spread across cities and loyalty tiers.
- **See when rides and revenue happen** — By hour and by day, so you can plan drivers and spot busy periods.
- **See revenue at risk** — How much money is tied to customers who haven’t ridden in a while, and which groups they belong to.
- **Predict churn** — For a single rider or a whole list, get a “how likely are they to leave?” score plus a suggested action (e.g. send an offer, give a perk).

No coding or data skills are required to use the app. You click through the pages and use filters and buttons to explore.

---

## How to open the app

1. Make sure you have **Python** installed on your computer.
2. Open a terminal (or command prompt) in the project folder.
3. Install what the app needs (the project’s `requirements.txt` lists everything).
4. Start the **backend** (the part that runs the churn prediction):  
   From the `backend` folder, run:  
   `uvicorn main:app --reload`  
   (or the command your project uses to start the backend server.)
5. Start the **frontend** (the part you see in the browser):  
   From the `frontend` folder, run:  
   `streamlit run Home.py`
6. Your browser will open the dashboard. Use the **navigation bar at the top** to switch between pages.

---

## What’s in the app?

At the **top of the screen** you’ll see a bar with:

- **Home** — Short intro and a list of what each page does. Use the bar to go to any other page.
- **Overview** — Summary numbers (users, trips, revenue) and charts by city and loyalty tier.
- **Demand & Revenue** — One page with two tabs: when rides happen (demand) and when money comes in (revenue).
- **Exposure Analysis** — How much revenue could be lost if “inactive” customers don’t come back, and who they are.
- **Churn Predictor** — Enter one rider’s details (or upload a file of many) and get a churn risk score and a recommendation.

The **sidebar** (left side) shows the RideWise logo and, on some pages, **filters** (e.g. city, year, month). Changing a filter updates the numbers and charts on that page. Many filters start on **“All”** so you see everything until you narrow it down.

---

## Page-by-page (in plain language)

### Home

Your starting point. It explains what the app does and lists the other pages. Use the **navigation bar above** (not the sidebar) to open Overview, Demand & Revenue, Exposure Analysis, or Churn Predictor.

---

### Overview

**What it answers:** *“What does our business look like right now?”*

- **Summary cards:** Total users, total trips, total revenue.
- **Filters:** City and Loyalty Tier. Choose “All” or pick one (e.g. one city, one tier). The numbers and charts update.
- **Charts:**  
  - Share of users in each loyalty tier (e.g. Bronze, Silver, Gold).  
  - Number of users per city.

**Use it when:** You want a quick snapshot or to compare one city or tier to the rest.

---

### Demand & Revenue

**What it answers:** *“When do rides happen?”* and *“When does revenue come in?”*

This is **one page with two tabs** at the top:

- **Demand Analysis** — Trips per hour of the day and trips per day. Helps you see peak times and plan driver supply.
- **Revenue Analysis** — Revenue per hour and revenue per day. Helps you see when you earn the most.

**Filters (same for both tabs):** Year, Month, City. Each can be set to “All” or a single option. Four summary cards (users, trips, revenue, average fare) sit above the tabs and also react to the filters.

**Use it when:** You want to see patterns over time (e.g. busy hours, busy days) or compare demand and revenue side by side.

---

### Exposure Analysis

**What it answers:** *“How much revenue could we lose if we don’t win back customers who haven’t ridden in a while?”*

- **Filter:** A slider for “days since last activity” (e.g. 7, 14, 30, 90 days). You decide what counts as “inactive.”
- **Summary:** Revenue at risk, number of customers in that group, and a breakdown by customer segment.
- **Charts and list:** A visual breakdown of which segments hold the most at-risk revenue, and a list of those customers so you know who to re-engage.

**Use it when:** You want to decide how much to invest in win-back campaigns and who to target first.

---

### Churn Predictor

**What it answers:** *“Is this rider (or these riders) likely to leave? What should we do about it?”*

Two ways to use it:

1. **Single Predict**  
   - Fill in one rider’s details: how long since last trip, number of trips, spend, tips, rating, loyalty tier, city, segment, etc.  
   - Click **“Predict Churn Risk.”**  
   - A **pop-up** appears with: churn probability, risk level (Low / Medium / High), and a **recommendation** (e.g. “Send a limited-time offer,” “Give recognition or perks”).  
   - Close the pop-up when you’re done; the main form stays as is.

2. **Batch Predict**  
   - Upload a file (e.g. CSV) with many riders and the same kinds of columns.  
   - The app runs the prediction for each row and lets you download the results (probability, risk level, etc.).

The **About** tab on this page describes the inputs and outputs in a bit more detail, still in plain language.

**Use it when:** You want to prioritize retention actions or decide what offer or message to send to a rider or a list of riders.

---

## Summary

| Page              | What you get |
|-------------------|--------------|
| **Home**          | Intro and links to all other pages. |
| **Overview**      | Big-picture numbers and charts by city and loyalty. |
| **Demand & Revenue** | When rides and revenue happen (two tabs), with filters. |
| **Exposure Analysis** | Revenue at risk from inactive customers and who they are. |
| **Churn Predictor**   | Churn risk and recommendations for one rider or many. |

---

## For people who want a bit more detail

- The app is built with **Streamlit** (the part you see) and a small **FastAPI** service (the part that runs the churn model).
- Data is loaded from files or sources set up in the project (e.g. trip data, segment data). The exact path is in the project setup.
- The churn model uses things like “days since last trip,” “number of trips,” “spend,” “loyalty tier,” “city,” and “customer segment” to score how likely a rider is to churn and to suggest an action. All of that is done behind the scenes; you only fill in the form or upload a file.

---

*This README is kept free of heavy jargon so anyone can understand what the project does and how to use it. For full technical details, see the code and the rest of the repository.*
