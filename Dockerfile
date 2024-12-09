FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY . .

# Install dependencies and set up environment
RUN pip install -r requirements.txt && \
    pip install whitenoise gunicorn && \
    echo "DJANGO_SECRET_KEY=your-secret-key-here" > .env && \
    echo "DJANGO_DEBUG=True" >> .env && \
    echo "ALLOWED_HOSTS=localhost,127.0.0.1,34.240.218.146" >> .env && \
    echo "EMAIL_HOST_USER=your-email@example.com" >> .env && \
    echo "EMAIL_HOST_PASSWORD=your-email-password" >> .env && \
    python manage.py collectstatic --noinput

EXPOSE 8000

# Start Gunicorn with whitenoise
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "portfolio_project.wsgi:application"]