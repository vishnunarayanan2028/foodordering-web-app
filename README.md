# Food Munch 🍔 — Madurai Food Ordering System

**Food Munch** is a full-stack, single and multi-restaurant food delivery web application built with Python (Flask), MySQL, and modern Vanilla HTML5/CSS3/JavaScript. It includes authentic Madurai iconic hotels (*Murugan Idli Shop, Simmakkal Konar Mess, Famous Special Jigarthanda, Amma Mess, Sree Sabarees, Kumar Mess*), a full shopping cart, checkout, demo instant payment / cash-on-delivery, live order tracking, and role-based management dashboards.

---

## ✨ Features

- **Iconic Madurai Hotels Showcase:** Discover famous Madurai restaurants, view hotel menus, ratings, and locations.
- **Dynamic Restaurant Filter:** Filter authentic dishes by specific Madurai hotels or categories (Kari Dosa, Bun Parotta, Jigarthanda, Seeraga Samba Biryani, Fish Fry).
- **User Authentication:** JWT-based login/registration with role support (**Customer**, **Restaurant Owner**, **Admin**).
- **Cart & Single-Restaurant Guard:** Full cart management (add, remove, update quantity, subtotal/tax/delivery calculation) with single-restaurant consistency check.
- **Checkout & Payment:** Support for **Cash on Delivery (COD)** and **Demo Instant Payment** (Card / UPI / NetBanking).
- **Order Tracking & History:** Real-time order timeline tracking (*Placed → Confirmed → Preparing → Out for Delivery → Delivered*) and cancellation support.
- **Admin & Restaurant Dashboards:** Dashboards for order status updates, menu item management, and system analytics.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6 Vanilla JS), Bootstrap 4, FontAwesome 5
- **Backend:** Python 3.12+, Flask 3.1.3, Flask-SQLAlchemy 3.1.1, Flask-JWT-Extended 4.7.1, Flask-CORS 5.0.1
- **Database:** MySQL 8.0+ (via `mysql-connector-python`)
- **Environment:** `python-dotenv` for configuration management

---

## ⚡ Quick Start Guide (Git Clone & Run)

### 1. Prerequisites
Make sure you have installed:
- **Python 3.12+**
- **MySQL Server 8.0+** (Running locally on port 3306)

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/Foodbooking.git
cd Foodbooking
```

### 3. Setup Virtual Environment & Dependencies
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env
```
*(If your MySQL `root` user has a password, update line 4 of `.env`: `DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/foodmunch_db`)*

### 5. Seed Database (Auto-Creates `foodmunch_db`)
```bash
python seed.py
```
*`seed.py` will automatically create the MySQL database `foodmunch_db` if it doesn't exist, build all 7 tables, download local high-res food images, and populate 6 Madurai hotels with 20 signature dishes.*

### 6. Run the Application
```bash
python run.py
```

### 7. Access in Browser
Open your browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🔐 Demo Credentials

Use any of the following accounts to test different roles:

| Role | Email | Password | Access Level |
|------|-------|----------|--------------|
| **Customer** | `customer@demo.com` | `Demo@123` | Browse, Cart, Checkout, Order Tracking, Profile |
| **Restaurant Owner** | `restaurant@demo.com` | `Demo@123` | Manage Menu Items, Update Order Status, Dashboard |
| **Admin** | `admin@demo.com` | `Demo@123` | Full System Management, User Overview, Analytics |

---

## 📁 Project Directory Structure

```text
Foodbooking/
├── .gitignore               # Git ignore file (env, pycache, logs)
├── README.md                # Project documentation & setup guide
├── frontend/                # Single-server served HTML/CSS/JS frontend
│   ├── index.html           # Landing page & Madurai Hotels showcase
│   ├── menu.html            # Food menu & restaurant dropdown filter
│   ├── cart.html            # Shopping cart page
│   ├── checkout.html        # Checkout & payment page (COD / Demo Payment)
│   ├── order-confirmation.html # Order confirmation & status summary
│   ├── orders.html          # My Orders history page
│   ├── order-detail.html    # Single order tracking & status timeline
│   ├── profile.html         # User profile page
│   ├── css/                 # Modern gold/navy design stylesheets
│   ├── js/                  # ApiClient, Auth, Menu, Cart, Orders JS logic
│   └── images/              # High-res local food photos & vector logo
├── backend/                 # Flask REST API backend
│   ├── app/
│   │   ├── models/          # User, Restaurant, Category, Food, CartItem, Order, OrderItem
│   │   ├── routes/          # Auth, Foods, Categories, Cart, Orders, Restaurant, Admin
│   │   ├── services/        # Business logic services
│   │   └── utils/           # Helper decorators & response formatters
│   ├── requirements.txt     # Python package dependencies
│   ├── .env.example         # Template for environment variables
│   ├── seed.py              # Auto database creation & Madurai dataset seeding
│   └── run.py               # Application entry point (runs on port 5000)
└── docs/                    # Architecture, Database, and API documentation
```

---

## 📄 License
This project is licensed under the MIT License.
