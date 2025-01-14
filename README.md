# Backend - Django API for E-Commerce

## Project Description
This repository contains the backend for an e-commerce website built using Django. The backend provides a RESTful API to handle the core functionality of the e-commerce platform, including user authentication, product management, order processing, and payment integration.  

## Key Features  
- **REST API**: Built using Django REST Framework to provide a clean and easy-to-use API for the frontend.
- **Authentication**: User registration, login, and token-based authentication for secure access to the platform.
- **Product Management**: CRUD operations for product listings, categories, and inventories.
- **Admin Dashboard**: Built-in Django admin panel for managing users, products, and orders.
- **Payment Integration**: Integration with payment gateways (e.g., Stripe or PayPal) for secure transactions.
- **Order Management**: APIs for users to place, track, and manage orders.

## Technologies Used  
- **Django**: The main framework used for the backend.
- **Django REST Framework**: For building the REST API.


## Setup Instructions  
1. **Clone the repository**
    ```bash
    git clone git@github.com:EmmanuelOnyekachi21/VioletteStores_api.git
    ```
2. **Backend Setup**
    - Navigate to the Backend folder
    ```bash
    cd VioletteStores_api
    ```
    - Create a virtual environment: ```python -m venv .venv```
    - Activate the environment:
        - On windows: ```.venv\Scripts\activate```
        - On Mac/Linux: ```source .venv/bin/activate```
        - Install dependencies: ```pip install -r requirements.txt```.
3. **Run databse migrations**
    ```bash
    python manage.py migrate
4.**Start the development server.**
    ```bash
    python manage.py runserver
    ```

#### The API will be available at http://127.0.0.1:8000/.
## API DOCUMENTATION
(To be added later after API development.)

## CHATGPT NOTES
[Click here](https://chatgpt.com/c/676d310a-250c-8005-8c5a-1b118aa8a77b)