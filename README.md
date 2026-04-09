# WebPress — High-Performance Visual Site Builder

WebPress is a professional, Django-powered platform designed for creating and managing modern, high-performance websites with a sophisticated visual builder. Inspired by modular CMS architectures, it provides a seamless "no-code" experience for site owners while maintaining technical excellence on the backend.

## 🚀 Key Features

*   **Advanced Visual Builder**: A drag-and-drop editor featuring real-time rendering, block-based design, and instant typography/color customization.
*   **Comprehensive Management Portal**: Centralized administration for users, websites, and system-wide resources.
*   **Adaptive Design Canvas**: Built-in responsiveness controls for Desktop, Tablet, and Mobile views.
*   **Instant Publishing**: One-click deployment system that generates clean, SEO-optimized HTML.
*   **Scalable Architecture**: Developed with a focus on performance, utilize CSS variables for global styling and lightweight JavaScript for interactions.

## 🛠️ Technology Stack

*   **Backend**: Python / Django
*   **Database**: PostgreSQL
*   **Frontend**: Vanilla JavaScript (ES6+), Modern CSS (Variables & HSL colors)
*   **Icons**: Lucide Icons
*   **Authentication**: Django Allauth (Standard + Google OAuth support)

## 📦 Installation & Setup

### 1. Environment Configuration
Clone the repository and create a virtual environment:
```bash
py -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
Ensure PostgreSQL is running and create the database credentials in a `.env` file (see `.env.example` if available).

```bash
# Example .env
DB_NAME=my_database
DB_USER=my_database_user
DB_PASS=my_database_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Initialize System
Run migrations and create an administrative account:
```bash
py manage.py migrate
py manage.py createsuperuser
```

### 5. Run Server
```bash
py manage.py runserver
```

## 🏗️ Project Structure

*   `core_app/`: The heart of the platform; contains models for Websites, Pages, and the core routing logic.
*   `core_engine/`: Main project configurations, settings, and global URL routing.
*   `theme_modern/`: Centralized template and static directory featuring the "Terminal Midnight" and "Modern White" aesthetics.
    *   `templates/core_app/builder/`: The frontend logic for the visual editor and its diverse set of blocks.
*   `media/`: Content storage for user-uploaded images and assets.

## 🎨 Aesthetic Design
The platform is designed with a high-contrast, premium aesthetic. It utilizes dynamic HSL color palettes, smooth transitions, and a technical "Terminal Midnight" theme for the administrative dashboard, ensuring a professional workspace for creators.

---
*Created with passion by the WebPress Engineering Team.*
