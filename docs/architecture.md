# Architecture Documentation

## System Overview

```
[ Client (Web/Mobile) ]
          │
          ▼ (HTTP/REST APIs)
[ Backend Server (Python/Flask/FastAPI/Node.js) ]
          │
          ├───────── [ JWT Auth Module ]
          │
          ├───────── [ Order Management ]
          │
          ├───────── [ Menu Management ]
          │
          ▼
[ MySQL Database (foodmunch_db) ]
```

## Technology Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| Frontend  | (TBD) | Web or Mobile App |
| Backend   | Python / Node.js | REST API Server |
| Database  | MySQL 8.0+ | Relational Data Storage |
| Auth      | JWT | Token-based authentication |

## Request Flow

1. **Client** sends an HTTP request to an API endpoint.
2. **Auth Middleware** intercepts the request to validate the JWT (if required).
3. **Controller/Router** processes the request and calls the relevant service logic.
4. **Service Layer** interacts with the **Database** using SQL queries.
5. **Database** returns the result.
6. The Backend formats the result as JSON and sends an HTTP response to the client.

## Directory Structure

```
Foodbooking/
├── database/
│   ├── schema.sql      # Database DDL
│   └── seed.sql        # Demo data insert script
├── docs/
│   ├── architecture.md # Architecture overview
│   ├── api.md          # REST API documentation
│   └── database.md     # DB Schema documentation
├── backend/            # Source code (to be added)
└── README.md           # Project setup and overview
```

## Authentication Flow

1. User submits credentials (email/password) to `/api/auth/login`.
2. Backend verifies credentials against `users.password_hash`.
3. If valid, a JSON Web Token (JWT) is generated containing the user ID and role.
4. Token is returned to the client and stored (e.g., in localStorage or cookies).
5. Subsequent authenticated requests must include the token in the `Authorization` header (`Bearer <token>`).

## Order Workflow

1. **Placed**: Customer adds items to cart and submits an order.
2. **Confirmed**: Restaurant reviews and accepts the order.
3. **Preparing**: Restaurant starts preparing the food.
4. **Ready**: Food is ready for pickup/delivery.
5. **Out for Delivery**: Delivery agent picks up the order.
6. **Delivered**: Order reaches the customer.
*(Alternatively, an order can be marked **Cancelled** by the customer or restaurant before it is confirmed/prepared).*

## Role-Based Access Matrix

| Feature | Customer | Restaurant | Admin |
|---------|----------|------------|-------|
| Browse Menu | Yes | Yes | Yes |
| Manage Cart | Yes | No | No |
| Place Order | Yes | No | No |
| View Own Orders | Yes | No | No |
| View Restaurant Orders | No | Yes | Yes |
| Update Order Status | No | Yes | Yes |
| Manage Foods/Categories | No | Yes | Yes |
| Manage Users | No | No | Yes |
