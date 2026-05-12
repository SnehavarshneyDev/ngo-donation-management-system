# NGO Donation Management System

A Django-based web application for managing fundraising campaigns and donations for a **single NGO**. Administrators manage campaigns, while end-users register for campaigns and make donations.

---

## Overview

The system is built using **Django** and follows the **Model–View–Template (MVT)** architecture. It is modular, scalable, and designed for real-world NGO donation workflows.

---

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML with static CSS served by Django
- **Database:**  
  - SQLite (initial development)  
  - MySQL (current, for scalability)
- **ORM:** Django ORM

---

## Core Modules

- `accounts` – User authentication and roles  
- `campaigns` – Fundraising campaign management  
- `registrations` – User registration for campaigns  
- `donations` – Donation and payment tracking  
- `pages` – Static informational pages  

---

## User Roles

- **Admin:** Creates and manages campaigns, views donations  
- **End-User (Donor):** Browses campaigns and makes donations  

---

## Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/C0deEnigma/ngo-donation-management-system.git
cd ngo-donation-management-system
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```
#### For Linux/MacOS:
```bash
source venv/bin/activate
```

#### For Windows:
```bash
venv\Scripts\activate
```

### 3. Install Project Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### 4.1 Create Database
Ensure MySQL is running, and use the following command:
```sql
CREATE DATABASE ngo_db;
```

#### 4.2 Configure Database Settings
In config/settings.py, update the DATABASE section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ngo_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 4.3 Apply Migrations
Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```
Follow the prompts to enter username, email and password

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser at
```bash
https://127.0.0.1:8000/
```

For admin dashboard, open

```bash
https://127.0.0.1:8000/admin/
```

## Checkout the demo video of the project here
[![Video Title](https://img.youtube.com/vi/4tOhBh61BD8/0.jpg)](https://www.youtube.com/watch?v=4tOhBh61BD8)
