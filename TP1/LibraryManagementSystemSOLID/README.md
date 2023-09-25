# Library Management System (TP1)

This project is part of the "Programmation Objet Avancée" course at UQAC (Université du Québec à Chicoutimi). It
represents a comprehensive library management system, implementing various object-oriented programming principles and
techniques.

## Overview
The Library Management System (LMS) is designed to manage books, transactions, reviews, and users. The system allows
users to borrow, return, and purchase books. It also supports the addition of reviews for books and generates reports
for reviews and sales.

## Features
* **Book Management:** Add, remove, and check the availability of books.
* **Transaction Management:** Handle borrow, return, and purchase transactions.
* **Review Management:** Add reviews for books and generate review reports.
* **User Management:** Manage user data including age, address, and email.
* **Report Generation:** Generate reports for reviews and sales.
* **Email Notification:** Send email notifications (mock implementation).

## Modules
* **Managers:** Central components that handle the core functionalities of the system.
* **Models:** Define the data structures and relationships for books, reviews, transactions, and users.
* **Reports:** Modules for generating various types of reports.
* **Utils:** Utility components such as the mock email sender.

## Installation & Usage
Ensure you have Python 3.x installed.
Clone the repository.
```bash
git clone https://github.com/antoine-granger/ProgrammationObjetAvancee.git
```
Navigate to the project directory and run main.py to test the implemented functionalities.
```bash
python main.py
```

## Future Improvements

* Improve the email notification system to support real-world use cases.
* Integrate with a database for persistent storage.
* Enhance the user interface for a better user experience.

## Acknowledgements

This project is supervised and evaluated by the faculty of UQAC as part of the "Programmation Objet Avancée" course.