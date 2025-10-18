# FMLP Backend API Documentation

This document provides details on the available API endpoints for the Farmers' Market Link Platform.

**Base URL**: `/api`

---

##  Authentication (`/auth`)

### 1. Register User
- **Endpoint**: `POST /auth/register`
- **Description**: Creates a new user account.
- **Roles**: `farmer` or `buyer`.
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john.doe@example.com",
    "password": "strongpassword123",
    "role": "farmer",
    "phone_number": "+254712345678"
  }
  ```
- **Response**: `201 Created`

### 2. Login User
- **Endpoint**: `POST /auth/login`
- **Description**: Authenticates a user and returns JWT tokens.
- **Request Body**:
  ```json
  {
    "email": "john.doe@example.com",
    "password": "strongpassword123"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "access_token": "...",
    "refresh_token": "..."
  }
  ```

---

## Produce (`/produce`)
*Authentication required for all endpoints.*

### 1. Create Produce Listing
- **Endpoint**: `POST /produce/`
- **Role**: `farmer`
- **Request Body**:
  ```json
  {
    "name": "Fresh Tomatoes",
    "description": "Locally grown, ripe tomatoes.",
    "price": "80.50",
    "quantity": 50,
    "unit": "kg"
  }
  ```
- **Response**: `201 Created`

### 2. Get All Produce
- **Endpoint**: `GET /produce/`
- **Role**: `any`
- **Response**: `200 OK` (Array of produce objects)

### 3. Update Produce Listing
- **Endpoint**: `PUT /produce/<int:produce_id>`
- **Role**: `farmer` (must own the listing)
- **Request Body**: (Partial updates allowed)
  ```json
  {
    "price": "85.00",
    "quantity": 45
  }
  ```
- **Response**: `200 OK`

### 4. Delete Produce Listing
- **Endpoint**: `DELETE /produce/<int:produce_id>`
- **Role**: `farmer` (must own the listing)
- **Response**: `204 No Content`

---

## Orders (`/orders`)
*Authentication required for all endpoints.*

### 1. Create an Order
- **Endpoint**: `POST /orders/`
- **Role**: `buyer`
- **Request Body**:
  ```json
  {
    "items": [
      { "produce_id": 1, "quantity": 5 },
      { "produce_id": 3, "quantity": 2 }
    ]
  }
  ```
- **Response**: `201 Created`

### 2. Get My Orders (as Buyer)
- **Endpoint**: `GET /orders/`
- **Role**: `buyer`
- **Response**: `200 OK` (Array of order objects)

### 3. Get My Orders (as Farmer)
- **Endpoint**: `GET /orders/farmer`
- **Role**: `farmer`
- **Response**: `200 OK` (Array of order objects containing the farmer's produce)

### 4. Update Order Status
- **Endpoint**: `PATCH /orders/<int:order_id>`
- **Role**: `farmer`
- **Request Body**:
  ```json
  {
    "status": "Confirmed"
  }
  ```
- **Response**: `200 OK`

---

## Payments (`/payments`)

### 1. Initiate Payment
- **Endpoint**: `POST /payments/initiate/<int:order_id>`
- **Role**: `buyer`
- **Description**: Triggers an M-Pesa STK push to the buyer's phone.
- **Response**: `200 OK`

### 2. M-Pesa Callback
- **Endpoint**: `POST /payments/callback`
- **Role**: `public`
- **Description**: Public endpoint for the Safaricom API. Do not call directly.
- **Response**: `200 OK`