#🌐 LocalServe – Local Service Booking Web Application

LocalServe is a full-stack web application built with Django that allows customers to easily book local home services such as cleaning, appliance repair, plumbing, and more. The system is designed with two user roles:

Customer – Can register, log in, browse services, book services, manage addresses, view bookings, and update profile.

Admin – Manages the entire platform: services, bookings, and workers (professionals). Admin assigns workers to bookings and monitors operations.

This project simulates a real-world service-based company where a central admin manages all workers and customer requests.

🚀 Features
Customer Side

User registration & login

Customer dashboard

Browse available services

Multi-step booking flow (Schedule → Address → Payment)

View booking history & status

Manage profile and saved addresses

Password reset via email

Admin Side

Admin dashboard with overview

Manage services (Add / Edit / Delete)

View all bookings

Assign workers to bookings

Manage professionals (workers)

Track booking status

🛠️ Tech Stack

Backend: Django

Frontend: HTML, CSS, JavaScript

Database: SQLite

Authentication: Django Auth + Google OAuth (Allauth)

Version Control: Git & GitHub

🎯 Goal of the Project

The goal of LocalServe is to demonstrate how a real-world service booking platform works, similar to apps like Urban Company or TaskRabbit, where:

Customers request services

Admin manages everything centrally

Workers are assigned by the admin

This project is built as a learning + portfolio project, covering:

Authentication

Role-based dashboards

CRUD operations

Booking workflows

Real-world Django project structure


