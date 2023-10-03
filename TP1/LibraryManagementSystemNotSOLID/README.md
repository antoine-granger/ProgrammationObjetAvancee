# Library Management System (TP1)
This project is part of the "Programmation Objet Avancée" course at UQAC (Université du Québec à Chicoutimi). It represents a comprehensive library management system, implementing various object-oriented programming principles and techniques. However, it intentionally deviates from the SOLID principles for illustrative purposes.

## Overview
The Library Management System (LMS) is designed to manage books, transactions, reviews, and users. The system allows users to borrow, return, and purchase books. It also supports the addition of reviews for books and sends out overdue notifications.

## Features
* **Book Management:** Add, remove, and check the availability of books.
* **Transaction Management:** Handle borrow, return, and purchase transactions.
* **Review Management:** Add reviews for books.
* **User Management:** Manage user data including age, address, and email.
* **Email Notification:** Send email notifications for overdue books (mock implementation).

## Modules
* **LibraryManager:** A central component that combines functionalities of managing books, users, transactions, and sending emails.
* **Models:** Define the data structures and relationships for books, reviews, transactions, and users.
* **Utils:** Utility components such as the mock email sender.

## SOLID Principles Analysis
The current design of the Library Management System deviates from the SOLID principles in the following ways:

1. **Single Responsibility Principle (SRP):** The LibraryManager class combines the responsibilities of managing books, users, transactions, and sending emails. This makes the class multifaceted and more challenging to maintain.
2. **Open/Closed Principle (OCP):** Extensions or modifications to a specific functionality, like book management, could affect other unrelated functionalities due to the monolithic design of LibraryManager.
3. **Interface Segregation Principle (ISP):** Modules interfacing with LibraryManager are forced to depend on functionalities they might not use, e.g., a module only interested in books still has access to user management methods.
4. **Dependency Inversion Principle (DIP):** The email notification functionality is hardcoded into the LibraryManager, making it dependent on a specific email sending implementation rather than an abstraction.

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
* Refactor the code to adhere to the SOLID principles.
* Improve the email notification system to support real-world use cases.
* Integrate with a database for persistent storage.
* Enhance the user interface for a better user experience.

## Acknowledgements
This project is supervised and evaluated by the faculty of UQAC as part of the "Programmation Objet Avancée" course.

