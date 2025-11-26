# Tour Package Management System (Django Backend)

A Django-based web application that manages tour packages, vendors, customers, bookings, and admin approvals. Supports multi-role authentication and dashboards.

## Features

### 1. User System

* Custom user model (Customer, Vendor, Admin)
* Email/password authentication
* Profile fields: name, email, phone, address
* Separate dashboards for each role

### 2. Package Management

* Vendors create, update, delete packages
* Admin approves or rejects packages
* Package fields: title, location, description, price, days, nights, thumbnail, status
* Customers browse and filter packages

### 3. Customer Features

* Browse approved packages
* View package details
* Book packages
* Booking history
* Customer dashboard

### 4. Vendor Features

* Manage own packages
* Track bookings
* View package approval status
* Vendor insights dashboard

### 5. Admin Features

* Manage all users
* Approve or reject packages
* View bookings
* Admin analytics dashboard

### 6. Additional Features

* Homepage with carousel
* Search and filtering
* Image uploads
* Booking notifications
* Responsive Bootstrap UI

## Technology Stack

* Django 3/4
* MySQL
* Bootstrap 4
* Django Auth + Custom User Model
* Pillow for media handling

## Setup & Installation

### Prerequisites

* Python 3.8+
* MySQL
* Virtualenv

### Installation Steps

Clone project → create virtual environment → install requirements → configure .env → migrate → create admin
