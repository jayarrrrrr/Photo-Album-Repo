# Photo Album Management System

This project is a Django-based Photo Album Management application with Cloudinary media storage and role-based access control (RBAC). It's prepared for deployment on Render with PostgreSQL.

Environment variables required:
- `DJANGO_SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL database URL
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` - Cloudinary credentials
- `USE_CLOUDINARY` - set to `True` in production

A local `.env` file is included for development; update it with your own values and keep it private.

Quick local setup:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Deploying to Render:
- Create a new Web Service using the public GitHub repository.
- Set build command: `pip install -r requirements.txt`
- Start command: `gunicorn photo_album.wsgi`
- Add environment variables listed above in Render dashboard.
