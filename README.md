# 🍴 FoodNest – Food Delivery Web Application

FoodNest is a web-based food delivery application developed using Django. It allows customers to browse restaurants, explore food menus, add food items to a cart, and make online payments using Razorpay.

---

## 📌 Project Overview

FoodNest provides a simple and user-friendly platform for customers to discover restaurants and order food online.

The application includes separate functionality for customers and administrators.

### 👤 Customer

Customers can:

- Create an account
- Login and logout
- Browse restaurants
- View restaurant menus
- Search for food items
- View food images and descriptions
- Add food items to cart
- View cart items
- Calculate the total price
- Proceed to checkout
- Make online payments using Razorpay
- View order confirmation
- View delivery address

### 👨‍💼 Admin

Administrators can:

- Login to the admin section
- Add restaurants
- View restaurants
- Update restaurant details
- Delete restaurants
- Add menu items
- Update menu items
- Delete menu items
- Manage restaurant information and locations

---

## ✨ Features

- 🔐 Customer Registration and Login
- 👤 Customer Profile
- 🍴 Restaurant Management
- 📋 Digital Food Menu
- 🔍 Food Search
- 🛒 Shopping Cart
- 💰 Automatic Total Price Calculation
- 💳 Razorpay Payment Integration
- 📦 Order Confirmation
- 📍 Delivery Address
- 🖼️ Food and Restaurant Images
- 🎨 Responsive and Attractive UI

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Django

### Database

- SQLite

### Payment Gateway

- Razorpay

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 📂 Project Structure

```text
FoodNest/
│
├── delivery/
│   ├── migrations/
│   │
│   ├── static/
│   │   └── delivery/
│   │       ├── css/
│   │       ├── food-bg.jpg
│   │       └── style.css
│   │
│   ├── templates/
│   │   └── delivery/
│   │       ├── index.html
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── customer_home.html
│   │       ├── customer_menu.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       └── orders.html
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── foodnest/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
