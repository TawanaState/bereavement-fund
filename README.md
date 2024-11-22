# Bereavement Fund Django Web Application

## Overview

This Django web application was initially developed for the **Harare Institute of Technology Staff Bereavement Fund** to manage contributions, balances, payment history, and member details. It is now open-sourced to help others learn and build similar systems.

Key features include:
- Email authentication for secure access.
- Comprehensive reports and data analysis for trustees.
- Member balance and payment history views.
- Trustee-specific views for member details.
- Secure management of sensitive user information.

## Features
- **Authentication:** Secure email-based authentication for members and trustees.
- **Reports & Analysis:** Tools for generating detailed financial reports.
- **Member Portal:** Personalized dashboards for members to view balances and payment history.
- **Trustee Portal:** Tools for trustees to manage and view member details.
- **Data Security:** Adherence to best practices for securing sensitive data.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bereavement-fund.git
   cd bereavement-fund
   ```

2. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Navigate to `http://127.0.0.1:8000/` to access the application.
2. Use the admin interface to create and manage users and data:
   ```bash
   python manage.py createsuperuser
   ```

## License
This project is licensed under the MIT License.
