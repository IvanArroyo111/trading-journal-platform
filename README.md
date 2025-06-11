# Trading Journal Platform (TraderCore)

A Django-based day trading journal and analytics platform built to help traders log trades, track progress, and gain insight into their performance over time.

**Live Demo:** [https://trading-journal-platform.onrender.com](https://trading-journal-platform.onrender.com)  
**Demo Account:**  
Username: `demo`  
Password: `DemoPass123`

---

## Features

- Dashboard Overview  
  View monthly trading performance including total PnL, win rate, number of trades, average risk/reward, and average holding time.

- Trade Journal  
  Add, edit, and delete trades with detailed fields including entry/exit, position size, notes, tags, and trade screenshots.

- Reports & Analytics  
  Filter trades by preset ranges (Last 30/60/90 days, This Month vs Last Month, All Time) and view charts that display performance trends and summaries.

- Calendar View  
  Visualize trading activity by date, color-coded based on profit or loss.

- Trade Details Page  
  Inspect each trade with full details and attached screenshots.

- Responsive User Interface  
  Clean layout with sidebar navigation, chart integrations (Chart.js), and mobile-friendly design.

---

## Tech Stack

- Backend: Python, Django  
- Frontend: HTML, CSS, JavaScript, Chart.js  
- Database: SQLite (development), PostgreSQL-ready  
- Deployment: Render  
- Other: Django Auth System, Static Files Management, Custom Templates

---

## Project Structure

TRADINGJOURNALPLATFORM/

├── trading_journal/

│ ├── accounts/ # Authentication and user-related views

│ ├── dashboard/ # Dashboard UI and logic

│ ├── journal/ # Trade journal models, views, and forms

│ ├── media/ # Uploaded screenshots and media files

│ ├── staticfiles/ # Custom CSS, JS, images

│ └── trading_journal/ # Core Django project settings and URLs

├── venv/ # Python virtual environment

├── db.sqlite3 # SQLite database (dev only)

├── manage.py # Django project manager script
├── requirements.txt # Python dependencies
