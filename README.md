# 🏠 Local Service Booking System

A full-stack Django web application that simulates a real-world home service platform where customers can book services and an admin (service company) manages professionals, bookings, and operations.

---

## 🚀 Project Overview

The **Local Service Booking System** is designed to replicate how modern service platforms operate.

It provides:

- A structured multi-step booking workflow  
- Admin-controlled worker assignment  
- Role-based access control  
- Booking lifecycle management  

The system separates responsibilities between **customers** and **admin**, ensuring scalable and maintainable architecture.

---

## 🧩 Core Features

### 👤 Customer Module

- Secure registration & authentication  
- Browse services by category  
- View detailed service information  
- Multi-step booking process:
  - Step 1: Select date & time  
  - Step 2: Select saved address  
  - Step 3: Payment workflow  
- View booking history  
- Track booking status  
- Manage profile & saved addresses  

---

### 🛠 Admin Module (Service Company Panel)

- Dashboard overview  
- Manage services & categories  
- Manage professionals (workers)  
- View and manage all bookings  
- Assign workers to bookings  
- Update booking status  
- Manage customers (block / unblock)  

---

## 🔁 Booking Lifecycle

The system implements a structured booking status flow:

REQUESTED → CONFIRMED → IN_PROGRESS → COMPLETED
                        ↘
                     CANCELLED / REJECTED

Each booking stores a snapshot of service details and address information to preserve historical accuracy.

---

## 🏗 Architecture Highlights

- Role-based authentication using Django’s built-in authentication system  
- Clear separation between Customer and Admin functionalities  
- Scalable database design using ForeignKey relationships  
- Multi-step booking flow with structured URL routing  
- Admin-controlled worker assignment  

This project demonstrates practical backend design and real-world workflow handling.

---

## 🛠 Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS  
- **Database:** SQLite  
- **Authentication:** Django Authentication System  

---

## ⚙️ Installation & Setup

```bash
git clone https://github.com/yourusername/local-service-booking.git
cd local-service-booking

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🎯 What This Project Demonstrates

- Full-stack Django development

- Real-world booking workflow implementation

- Multi-role system design

- Admin-based operational control

- Database modeling and relationship management

- Structured status management

## 💡 Author

Developed as a full-stack Django web application focused on building a real-world service booking platform using Django.
