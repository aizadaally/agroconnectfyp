AgroConnect Naryn
AgroConnect is a farm-to-table marketplace platform connecting farmers in the Naryn region of Kyrgyzstan directly with consumers. This platform eliminates middlemen, allowing farmers to sell their products at better prices while giving consumers access to fresh, locally-grown produce.
Show Image
🌱 Project Overview
AgroConnect Naryn is a Django-based web application that provides:

Direct marketplace for farmers to list and sell their products
User accounts for both farmers and buyers
Order management system for tracking purchases
Payment processing with multiple payment options
Multilingual support (English, Russian, and Kyrgyz)
Responsive design that works on mobile and desktop devices
AI-powered chatbot assistant for farming advice

🚀 Features
For Farmers

Create and manage product listings
Track orders and confirm payments
Maintain a profile with farm information
Receive direct payments from buyers

For Buyers

Browse products by category
Search for specific items
Add items to cart
Complete checkout process
Track order status
Contact farmers directly

For Everyone

Multilingual interface (English, Russian, Kyrgyz)
AI Farming Assistant chatbot for agriculture advice
Dark/light theme toggle
Responsive design for all devices

💻 Technology Stack

Backend: Django 5.2
Frontend: HTML, CSS, JavaScript, Bootstrap 5
Database: PostgreSQL
Authentication: Django built-in auth
File Storage: Cloudinary
Deployment: Railway
AI Assistant: Integration with LLaMA API
Email Service: Zoho Mail
Internationalization: Django i18n

📦 Project Structure
The project follows a modular Django architecture with these main apps:

users - User account management (farmer/buyer)
products - Product listing and management
orders - Order processing and payment
frontend - Templates and static files
api - REST API endpoints
chatbot - AI assistant integration

🛠️ Installation and Setup
Prerequisites

Python 3.10+
PostgreSQL
Git

Local Development Setup

Clone the repository:
bashgit clone https://github.com/yourusername/agroconnect.git
cd agroconnect

Create and activate a virtual environment:
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
bashpip install -r requirements.txt

Create a .env file in the project root with the following variables:
SECRET_KEY=your_secret_key
DEBUG=True

# Database configuration
ENGINE=django.db.backends.postgresql
PGNAME=agroconnect_db
PGUSER=postgres
PGPASSWORD=your_password
PGHOST=localhost
PGPORT=5432

# Email configuration
EMAIL_HOST_USER=your_email@zoho.com
EMAIL_HOST_PASSWORD=your_app_password

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# LLaMA API config
IO_INTELLIGENCE_API_KEY=your_api_key

Run migrations:
bashpython manage.py migrate

Create a superuser:
bashpython manage.py createsuperuser

Generate initial sample data:
bashpython api/create_initial_data.py

Run the development server:
bashpython manage.py runserver

Access the site at http://localhost:8000

🌐 Deployment
The production version is deployed on Railway. For deployment:

Create a Railway account and project
Connect your GitHub repository
Set the environment variables as in the .env file
Deploy the application

🔄 Internationalization
The platform supports three languages:

English (default)
Russian
Kyrgyz

To generate translation files:
bash# Mark strings for translation
python manage.py makemessages -l ru -l ky

# Compile translation files after editing
python manage.py compilemessages
Edit the .po files in the locale/ directory to update translations.
🤖 AI Assistant
The platform features an AI-powered farming assistant:

Built with LLaMA model
Provides farming advice in all three languages
Accessible via chat interface
Stores conversation history for registered users

✨ Key Components
Multi-User System
Different interfaces and capabilities for farmers and buyers.
Multilingual Product Management
Products can have details in multiple languages.
Order Processing Workflow
Step-by-step process from cart to checkout to payment confirmation.
Farm-to-Table Direct Connection
Direct messaging and payment between farmers and buyers.
📄 API Documentation
The platform provides a REST API for interacting with the system:
EndpointMethodDescription/api/auth/register/POSTRegister a new user/api/auth/login/POSTLog in a user/api/auth/logout/POSTLog out a user/api/auth/user/GETGet current user information/api/categories/GETList all categories/api/products/GETList all products/api/products/<id>/GETGet product details/api/products/my_products/GETGet farmer's products/api/orders/cart/GETGet current user's cart/api/orders/<id>/add_item/POSTAdd product to order
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Made with ❤️ for Naryn's farmers and community.