# Microservice Architecture with Payment Gateway (Stripe) 💳

This project demonstrates a microservice architecture using **Python**, **Flask**, **MongoDB**, **Docker**, and **Proxmox**. It includes three microservices: **User Service**, **Order Service**, and **Payment Service**. The **Payment Service** integrates with **Stripe** to handle secure payments.

---

## Project Structure 📂

The project is organized into the following services:

1. **User Service** (`user_service.py`): Manages user information.
2. **Order Service** (`order_service.py`): Manages customer orders.
3. **Payment Service** (`payment_service.py`): Integrates with Stripe to process payments.
4. **Dockerfile**: Containerizes the Payment Service.
5. **docker-compose.yml** (Optional): Docker Compose file for orchestration.

---

## Prerequisites ✅

Before you begin, ensure you have the following:

- **Python 3.x** installed.
- **MongoDB** running (locally or via MongoDB Atlas).
- **Stripe API Key**: Sign up for Stripe and get your secret API key.
- **Docker** installed (if using Docker).
- **Proxmox** (optional, for scaling using virtual machines or containers).
- **curl** or any HTTP client to interact with the services.

---

## Setup Instructions 🛠️

### 1. Install Required Python Dependencies 🐍

First, create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows
```

Then, install the required dependencies:

```bash
pip install Flask pymongo requests stripe
```

### 2. Docker Setup (Optional) 🐳

If you'd like to use Docker to containerize the Payment Service, make sure Docker is installed on your machine. You can follow the official Docker installation guide if you haven't already.

To build and run the Payment Service using Docker:

```bash
docker build -t payment-service .
docker run -d -p 5002:5002 payment-service
```

### 3. Proxmox Setup (Optional) 🖥️

For scaling, Proxmox can be used to create and manage virtual machines or containers that host your microservices.

You can deploy each service (User, Order, Payment) in separate virtual machines or containers, or use Docker Swarm or Kubernetes for orchestration.

---

## Services Overview 🔍

### 1. User Service (`user_service.py`)

This service manages users. It provides endpoints to create and fetch user information.

Endpoints:

- `POST /users`: Create a new user.
- `GET /users/{user_id}`: Fetch details of a user.

### 2. Order Service (`order_service.py`)

This service handles orders. It allows for creating orders and updating order statuses (e.g., marking as paid after a successful payment).

Endpoints:

- `POST /orders`: Create a new order.
- `PUT /orders/{order_id}/pay`: Update the payment status of an order.

### 3. Payment Service (`payment_service.py`)

This service interacts with Stripe to handle payments. It processes payments and stores transaction records in MongoDB.

Endpoints:

- `POST /pay`: Process a payment via Stripe.
- `GET /payments/{user_id}`: Retrieve all payments made by a specific user.

---

## Payment Gateway Integration (Stripe) 💳

### 1. Configure Stripe API Key 🔑

In `payment_service.py`, replace the placeholder for the Stripe secret key:

```python
stripe.api_key = "sk_test_XXXXXXXXXXXXXXXXXXXXXXXX"
```

### 2. Payment Process 💸

The `/pay` endpoint allows users to process payments by providing their `user_id`, `order_id`, and `amount`. The service then interacts with Stripe to charge the user and updates the Order Service to mark the order as paid.

---

## MongoDB Schema 🗄️

The Payment Service stores transaction details in MongoDB under the `payments` collection with the following schema:

```json
{
  "user_id": "63d4c56ad7b6be5f8996e5f9",
  "order_id": "63d4c66dd7b6be5f8996e5fa",
  "amount": 10000,
  "currency": "usd",
  "payment_status": "succeeded",
  "transaction_id": "ch_1JXXXXXXXXX"
}
```

---

## Dockerize Payment Service 🐳

To containerize the Payment Service, use the provided Dockerfile.

### 1. Build Docker Image 🏗️

Run the following commands to build the Docker image:

```bash
docker build -t payment-service .
```

### 2. Run Docker Container 🚀

After building the image, run the container:

```bash
docker run -d -p 5002:5002 payment-service
```

---

## Scaling with Docker and Proxmox 📈

To scale the services using Docker Swarm or Kubernetes, you can deploy multiple instances of each service. Alternatively, you can use Proxmox to manage virtual machines or containers and deploy each service on different machines or nodes.

### Scaling with Docker Swarm 🐝

First, initialize Docker Swarm:

```bash
docker swarm init
```

Then, create a Docker service for the Payment Service with multiple replicas:

```bash
docker service create --name payment-service --replicas 3 -p 5002:5002 payment-service
```

---

## Testing the Services 🧪

### 1. Create a User

```bash
curl -X POST http://localhost:5001/users -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}'
```

Response:

```json
{
  "message": "User created",
  "user_id": "63d4c56ad7b6be5f8996e5f9"
}
```

### 2. Create an Order

```bash
curl -X POST http://localhost:5000/orders -H "Content-Type: application/json" -d '{"user_id": "63d4c56ad7b6be5f8996e5f9", "product": "Laptop"}'
```

Response:

```json
{
  "message": "Order created",
  "order_id": "63d4c66dd7b6be5f8996e5fa"
}
```

### 3. Process a Payment

```bash
curl -X POST http://localhost:5002/pay -H "Content-Type: application/json" -d '{"user_id": "63d4c56ad7b6be5f8996e5f9", "order_id": "63d4c66dd7b6be5f8996e5fa", "amount": 10000, "currency": "usd"}'
```

Response:

```json
{
  "message": "Payment Successful",
  "transaction_id": "ch_1JXXXXXXXXX",
  "status": "succeeded"
}
```

### 4. Retrieve Payment History

```bash
curl -X GET http://localhost:5002/payments/63d4c56ad7b6be5f8996e5f9
```

Response:

```json
[
  {
    "_id": "63d4c8dcd7b6be5f8996e5fb",
    "user_id": "63d4c56ad7b6be5f8996e5f9",
    "order_id": "63d4c66dd7b6be5f8996e5fa",
    "amount": 10000,
    "currency": "usd",
    "payment_status": "succeeded",
    "transaction_id": "ch_1JXXXXXXXXX"
  }
]
```

---

## Conclusion 🎉

This project demonstrates how to integrate a payment gateway (Stripe) into a Python-based microservices architecture. The services are containerized with Docker and can be scaled using Docker Swarm or Kubernetes. The use of Proxmox allows for better scaling management through virtualization.

---

## Steps to Deploy to GitHub 🚀

1. Create a new GitHub repository.
2. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/microservice-payment.git
cd microservice-payment
```

3. Create a `README.md` file and paste the content above.
4. Commit and push your changes:

```bash
git add .
git commit -m "Add README with project details"
git push origin main
```

This will create a well-documented GitHub repository for your project.
