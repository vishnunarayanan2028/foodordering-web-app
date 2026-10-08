# API Documentation

Base URL: `/api`

## Authentication Endpoints

### Register Customer
- **Method:** `POST`
- **Path:** `/auth/register`
- **Description:** Register a new customer.
- **Auth:** Public
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "password": "securepassword",
    "phone": "1234567890"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "user": { "id": 4, "name": "John Doe", "email": "johndoe@example.com", "role": "customer" },
    "token": "jwt_token_here"
  }
  ```

### Login
- **Method:** `POST`
- **Path:** `/auth/login`
- **Description:** Authenticate a user and receive a JWT.
- **Auth:** Public
- **Request Body:**
  ```json
  {
    "email": "johndoe@example.com",
    "password": "securepassword"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "user": { "id": 4, "name": "John Doe", "email": "johndoe@example.com", "role": "customer" },
    "token": "jwt_token_here"
  }
  ```

### Logout
- **Method:** `POST`
- **Path:** `/auth/logout`
- **Description:** Invalidate the current session token.
- **Auth:** Required (JWT)
- **Response:**
  ```json
  { "success": true, "message": "Logged out successfully" }
  ```

### Get Profile
- **Method:** `GET`
- **Path:** `/auth/me`
- **Description:** Fetch current user's profile.
- **Auth:** Required (JWT)
- **Response:**
  ```json
  { "success": true, "user": { "id": 4, "name": "John Doe", "email": "johndoe@example.com", "phone": "1234567890", "role": "customer" } }
  ```

### Update Profile
- **Method:** `PUT`
- **Path:** `/auth/profile`
- **Description:** Update current user's profile.
- **Auth:** Required (JWT)
- **Request Body:**
  ```json
  { "name": "John Smith", "phone": "0987654321" }
  ```
- **Response:**
  ```json
  { "success": true, "user": { ...updated_user_data } }
  ```

### Change Password
- **Method:** `PUT`
- **Path:** `/auth/password`
- **Description:** Change user password.
- **Auth:** Required (JWT)
- **Request Body:**
  ```json
  { "current_password": "securepassword", "new_password": "newsecurepassword" }
  ```
- **Response:**
  ```json
  { "success": true, "message": "Password updated successfully" }
  ```

## Food Endpoints

### List Foods
- **Method:** `GET`
- **Path:** `/foods`
- **Description:** Get a list of foods.
- **Auth:** Public
- **Query Params:** `category_id`, `search`, `is_veg`, `is_available`
- **Response:**
  ```json
  { "success": true, "foods": [ { "id": 1, "name": "Chicken Tikka", "price": 280.00, ... } ] }
  ```

### Get Food
- **Method:** `GET`
- **Path:** `/foods/:id`
- **Description:** Get food details by ID.
- **Auth:** Public
- **Response:**
  ```json
  { "success": true, "food": { "id": 1, "name": "Chicken Tikka", ... } }
  ```

### Create Food
- **Method:** `POST`
- **Path:** `/foods`
- **Description:** Create a new food item.
- **Auth:** Required (Restaurant/Admin)
- **Request Body:**
  ```json
  { "name": "Paneer Butter Masala", "description": "Rich paneer curry", "price": 260.00, "category_id": 5, "image_url": "url", "is_veg": true }
  ```
- **Response:**
  ```json
  { "success": true, "food": { ... } }
  ```

### Update Food
- **Method:** `PUT`
- **Path:** `/foods/:id`
- **Description:** Update an existing food item.
- **Auth:** Required (Restaurant/Admin)
- **Response:**
  ```json
  { "success": true, "food": { ... } }
  ```

### Delete Food
- **Method:** `DELETE`
- **Path:** `/foods/:id`
- **Description:** Delete a food item.
- **Auth:** Required (Restaurant/Admin)
- **Response:**
  ```json
  { "success": true, "message": "Food deleted successfully" }
  ```

## Category Endpoints

### List Categories
- **Method:** `GET`
- **Path:** `/categories`
- **Description:** Get all categories (with food count).
- **Auth:** Public
- **Response:**
  ```json
  { "success": true, "categories": [ { "id": 1, "name": "Starters", "food_count": 4 } ] }
  ```

### Get Category
- **Method:** `GET`
- **Path:** `/categories/:id`
- **Description:** Get category details along with associated foods.
- **Auth:** Public
- **Response:**
  ```json
  { "success": true, "category": { "id": 1, "name": "Starters", "foods": [ ... ] } }
  ```

### Create Category
- **Method:** `POST`
- **Path:** `/categories`
- **Description:** Create a new category.
- **Auth:** Required (Restaurant/Admin)
- **Request Body:**
  ```json
  { "name": "Beverages", "description": "Cold drinks and sodas", "image_url": "url" }
  ```
- **Response:**
  ```json
  { "success": true, "category": { ... } }
  ```

### Update Category
- **Method:** `PUT`
- **Path:** `/categories/:id`
- **Description:** Update category details.
- **Auth:** Required (Restaurant/Admin)
- **Response:**
  ```json
  { "success": true, "category": { ... } }
  ```

### Delete Category
- **Method:** `DELETE`
- **Path:** `/categories/:id`
- **Description:** Delete a category.
- **Auth:** Required (Restaurant/Admin)
- **Response:**
  ```json
  { "success": true, "message": "Category deleted successfully" }
  ```

## Cart Endpoints

### Get Cart
- **Method:** `GET`
- **Path:** `/cart`
- **Description:** Get user's active cart.
- **Auth:** Required (Customer)
- **Response:**
  ```json
  {
    "success": true,
    "cart": {
      "items": [ { "id": 1, "food": { ... }, "quantity": 2 } ],
      "subtotal": 560.00,
      "tax": 28.00,
      "delivery_fee": 50.00,
      "total": 638.00
    }
  }
  ```

### Add to Cart
- **Method:** `POST`
- **Path:** `/cart/items`
- **Description:** Add food to cart.
- **Auth:** Required (Customer)
- **Request Body:**
  ```json
  { "food_id": 1, "quantity": 1 }
  ```
- **Response:**
  ```json
  { "success": true, "cart": { ... } }
  ```

### Update Cart Item
- **Method:** `PUT`
- **Path:** `/cart/items/:id`
- **Description:** Update cart item quantity.
- **Auth:** Required (Customer)
- **Request Body:**
  ```json
  { "quantity": 3 }
  ```
- **Response:**
  ```json
  { "success": true, "cart": { ... } }
  ```

### Remove Cart Item
- **Method:** `DELETE`
- **Path:** `/cart/items/:id`
- **Description:** Remove item from cart.
- **Auth:** Required (Customer)
- **Response:**
  ```json
  { "success": true, "cart": { ... } }
  ```

### Clear Cart
- **Method:** `DELETE`
- **Path:** `/cart`
- **Description:** Empty the entire cart.
- **Auth:** Required (Customer)
- **Response:**
  ```json
  { "success": true, "message": "Cart cleared" }
  ```

## Order Endpoints

### Place Order
- **Method:** `POST`
- **Path:** `/orders`
- **Description:** Place an order from the cart.
- **Auth:** Required (Customer)
- **Request Body:**
  ```json
  {
    "delivery_address": "123 Main St",
    "phone": "1234567890",
    "payment_method": "cash_on_delivery",
    "notes": "Leave at door"
  }
  ```
- **Response:**
  ```json
  { "success": true, "order": { "id": 1, "order_number": "ORD-123", ... } }
  ```

### List User Orders
- **Method:** `GET`
- **Path:** `/orders`
- **Description:** Get order history for customer.
- **Auth:** Required (Customer)
- **Response:**
  ```json
  { "success": true, "orders": [ ... ] }
  ```

### Get Order Detail
- **Method:** `GET`
- **Path:** `/orders/:id`
- **Description:** Get specific order details.
- **Auth:** Required (Customer, own order only)
- **Response:**
  ```json
  { "success": true, "order": { "items": [ ... ], ... } }
  ```

### Cancel Order
- **Method:** `PUT`
- **Path:** `/orders/:id/cancel`
- **Description:** Cancel an order (only if status is 'placed').
- **Auth:** Required (Customer)
- **Response:**
  ```json
  { "success": true, "order": { ... } }
  ```

## Restaurant Endpoints

### Get Info
- **Method:** `GET`
- **Path:** `/restaurant`
- **Description:** Get public restaurant information.
- **Auth:** Public
- **Response:**
  ```json
  { "success": true, "restaurant": { "name": "Food Munch", ... } }
  ```

### Update Info
- **Method:** `PUT`
- **Path:** `/restaurant`
- **Description:** Update restaurant details.
- **Auth:** Required (Restaurant/Admin)
- **Response:**
  ```json
  { "success": true, "restaurant": { ... } }
  ```

### List Restaurant Orders
- **Method:** `GET`
- **Path:** `/restaurant/orders`
- **Description:** View all orders.
- **Auth:** Required (Restaurant)
- **Query Params:** `status`
- **Response:**
  ```json
  { "success": true, "orders": [ ... ] }
  ```

### Update Order Status
- **Method:** `PUT`
- **Path:** `/restaurant/orders/:id/status`
- **Description:** Update the status of an order.
- **Auth:** Required (Restaurant)
- **Request Body:**
  ```json
  { "status": "preparing" }
  ```
- **Response:**
  ```json
  { "success": true, "order": { ... } }
  ```

### Restaurant Dashboard
- **Method:** `GET`
- **Path:** `/restaurant/dashboard`
- **Description:** Get quick stats (sales, order count).
- **Auth:** Required (Restaurant)
- **Response:**
  ```json
  { "success": true, "stats": { "total_sales": 5000, "pending_orders": 5, ... } }
  ```

## Admin Endpoints

### Admin Dashboard
- **Method:** `GET`
- **Path:** `/admin/dashboard`
- **Description:** Get overall system statistics.
- **Auth:** Required (Admin)
- **Response:**
  ```json
  { "success": true, "stats": { "total_users": 150, "total_orders": 1200, ... } }
  ```

### List Users
- **Method:** `GET`
- **Path:** `/admin/users`
- **Description:** Get all users.
- **Auth:** Required (Admin)
- **Response:**
  ```json
  { "success": true, "users": [ ... ] }
  ```

### Update User
- **Method:** `PUT`
- **Path:** `/admin/users/:id`
- **Description:** Update user role or status.
- **Auth:** Required (Admin)
- **Request Body:**
  ```json
  { "role": "restaurant", "is_active": true }
  ```
- **Response:**
  ```json
  { "success": true, "user": { ... } }
  ```

### List All Orders
- **Method:** `GET`
- **Path:** `/admin/orders`
- **Description:** Get all system orders.
- **Auth:** Required (Admin)
- **Response:**
  ```json
  { "success": true, "orders": [ ... ] }
  ```
