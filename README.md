# Django Blog

A complete blog website built with Django.

## Features

- User authentication (login/register)
- Google & GitHub login (OAuth2)
- Create, edit, delete articles
- Categories & tags system
- Comment system
- User profiles with avatar
- Search articles
- Article views count & reading time
- Admin panel with django-jet
- Responsive design with Bootstrap 5

## Tech Stack

- Django 4.2
- PostgreSQL
- Bootstrap 5
- django-allauth
- django-jet
- django-taggit
- crispy-forms



## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yazdan552/django-blog.git
cd django-blog
```

### 2. Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin user

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Environment Variables

Create a `.env` file with these variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
DB_NAME=blog_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Project Structure

```
pro_blog/
├── accounts/           # Authentication & profiles
├── blog/               # Main blog app
├── pro_blog/           # Project settings
├── templates/          # HTML templates
├── static/             # CSS, JS files
├── media/              # Uploaded files
├── screenshots/        # Screenshots for README
├── .env.example        # Example environment file
├── .gitignore
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Author

**Yazdan** - [GitHub](https://github.com/yazdan552)

---

⭐ Star this repository if you like it!
