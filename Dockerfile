FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=portfolio_project.settings

# Set work directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY . .

# Install Gunicorn and other dependencies
RUN pip install -r requirements.txt gunicorn && \
    echo "DJANGO_SECRET_KEY=your-secret-key-here" > .env && \
    echo "DJANGO_DEBUG=False" >> .env && \
    echo "ALLOWED_HOSTS=localhost,127.0.0.1,34.240.218.146" >> .env && \
    echo "EMAIL_HOST_USER=your-email@example.com" >> .env && \
    echo "EMAIL_HOST_PASSWORD=your-email-password" >> .env && \
    python manage.py collectstatic --noinput

# Create and set permissions for media directory
RUN mkdir -p /app/media && \
    chmod -R 755 /app/media

EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "portfolio_project.wsgi:application"]