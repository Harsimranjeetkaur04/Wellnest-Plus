# CareSync 🩺

CareSync is a comprehensive healthcare platform designed to serve both patients and doctors. It provides an end-to-end solution that includes an **AI-powered symptom checker**, personalized dashboards, and a robust appointment management system to streamline healthcare interactions.

---

### Progress & Key Features ✨

* **AI Symptom Checker**: Our core feature is a machine learning model, developed with **scikit-learn**, that predicts potential diseases based on user-inputted symptoms. This is integrated with a **Django backend** to handle data and provide prediction APIs.

* **Personalized Dashboards**: Separate, secure dashboards have been implemented for patients and doctors with role-based access control. These dashboards display appointments, medical history, diagnoses, and allow for profile management.

* **Appointment Management**: The platform includes a full suite of appointment management features, offering Create, Read, Update, and Delete (CRUD) operations with real-time status updates and user notifications.

* **Robust Backend**: The backend is built with **Django** and uses a **PostgreSQL** database. The database schema is carefully normalized to manage users, doctors, patients, diagnoses, appointments, and symptom records.

* **RESTful API**: **Django REST Framework** was used to design and develop a set of RESTful endpoints, ensuring seamless interaction with the frontend and future third-party integrations.

* **Responsive UI/UX**: The frontend uses responsive Django templates, styled with **Tailwind CSS** and enhanced with **JavaScript** for dynamic and intuitive user interactions.

* **Detailed Documentation**: Comprehensive documentation has been created to cover the AI model integration, database schema, API routes, and user workflows, which facilitates future development and onboarding.

---

### Requirements 📋

To run this project, you will need the following dependencies:

* **Python 3.x**
* **Django**
* **Django REST Framework**
* **scikit-learn**
* **psycopg2-binary** (for PostgreSQL connectivity)
* **Tailwind CSS**
* **PostgreSQL** database

---
