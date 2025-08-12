# Housing Rental System Backend

This project is a fully functional back-end application for a housing rental system, built with Django and Django REST Framework. It provides a robust API for managing listings, handling user authentication, and managing bookings and reviews.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)

---

## Features

The application includes the following core functionalities:

### 1. Listing Management
- **Create a listing**: Landlords can add new properties with details such as title, description, location, price, number of rooms, and housing type.
- **Edit a listing**: Landlords can update their existing listings.
- **Delete a listing**: Landlords can remove their listings.
- **Toggle listing availability**: Landlords can set a listing to active or inactive to temporarily hide or show it.

### 2. Search and Filtering
- **Keyword search**: Search for listings by keywords in the title and description.
- **Advanced filtering**: Filter listings by price range, location, number of rooms, and housing type.
- **Sorting**: Sort results by price (ascending/descending), creation date (newest/oldest), views count, and number of reviews.

### 3. User Authentication and Authorization
- **User registration**: Create new user accounts (Landlord or Tenant).
- **User login**: Get JWT tokens for secure access to the API.
- **Access control**:
    - **Tenants** can view, search, and filter listings, and create bookings and reviews.
    - **Landlords** can create, edit, delete, and manage their own listings, and confirm or reject booking requests.

### 4. Booking System
- **Create a booking**: Tenants can book a listing for specific dates. The system prevents double-booking for confirmed dates.
- **View bookings**: Users can view their active and completed bookings. Landlords can view all bookings for their properties.
- **Cancel a booking**: Tenants can cancel a booking.
- **Confirm/Reject a booking**: Landlords can approve or decline booking requests from tenants.

### 5. Ratings and Reviews
- **Leave a review**: Users can leave a rating and review for a listing **only after their confirmed booking has been completed**.
- **View reviews**: View all reviews and ratings for a specific listing.

### 6. Additional Features
- **Search history**: The system records user search queries to provide insights into popular searches.
- **Listing views**: Tracks the number of times each listing has been viewed, enabling a "popular listings" feature.

---

## Technologies

This project is built using the following technologies:

- **Python**: The core programming language.
- **Django**: The web framework for building the application.
- **Django REST Framework (DRF)**: For building the RESTful API endpoints.
- **MySQL**: The relational database for data storage.
- **Docker & Docker Compose**: For containerization and easy setup of the application and database.
- **`djangorestframework-simplejwt`**: For JWT-based user authentication.
- **`django-filter`**: For robust and easy-to-implement filtering functionality.

---

## Setup and Installation

### Prerequisites
- Docker Desktop installed on your machine.

### Steps
1.  **Clone the repository**:
    ```bash
    git clone [your-repository-url]
    cd housing-rental-system
    ```

2.  **Configure the database**:
    Open `rental_system/settings.py` and ensure the `DATABASES` configuration is set for MySQL. The `docker-compose.yml` file is pre-configured to work with these settings.

3.  **Build and run the containers**:
    This command will build the Docker images and start the Django and MySQL containers.
    ```bash
    docker-compose up --build
    ```

4.  **Run migrations and create a superuser**:
    Open a new terminal window and execute these commands to set up the database.
    ```bash
    docker-compose exec app python manage.py makemigrations listings
    docker-compose exec app python manage.py makemigrations users
    docker-compose exec app python manage.py migrate
    docker-compose exec app python manage.py createsuperuser
    ```

5.  **Create user groups**:
    Access the Django Admin panel at `http://localhost:8000/admin/` and create two groups: "Landlords" and "Tenants". Assign users to these groups as needed to manage their permissions.

The application is now running and accessible at `http://localhost:8000`.

---

## API Endpoints

Below are examples of the main API endpoints.

### Listing Management
- **List listings**: `GET /api/listings/`
- **Create a listing**: `POST /api/listings/` (Requires authentication and Landlord group membership)
- **Retrieve a listing**: `GET /api/listings/{id}/`
- **Update a listing**: `PATCH /api/listings/{id}/` (Requires authentication and ownership)
- **Toggle listing status**: `PATCH /api/listings/{id}/toggle_active/` (Requires authentication and ownership)

### Search, Filter, and Sort
- **Search by keyword**: `GET /api/listings/?search=berlin`
- **Filter by price range**: `GET /api/listings/?min_price=100&max_price=200`
- **Sort by price**: `GET /api/listings/?ordering=-price_per_night` (descending)
- **Get popular searches**: `GET /api/users/me/popular_searches/`

### Booking System
- **Create a booking**: `POST /api/bookings/` (Requires authentication)
- **List user's bookings**: `GET /api/bookings/` (Requires authentication)
- **Confirm a booking**: `PATCH /api/bookings/{id}/confirm/` (Requires authentication and Landlord ownership of the listing)
- **Cancel a booking**: `PATCH /api/bookings/{id}/cancel/` (Requires authentication and booking ownership)

### Reviews
- **List reviews for a listing**: `GET /api/listings/{listing_id}/reviews/`
- **Create a review**: `POST /api/listings/{listing_id}/reviews/` (Requires authentication and a completed, confirmed booking for the listing)

---

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

- **Register**: `POST /api/users/register/`
- **Login**: `POST /api/users/login/`
- **Refresh token**: `POST /api/users/token/refresh/`

To make authenticated requests, include the `Authorization` header with your access token:
`Authorization: Bearer <your_access_token>`