FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY . .

# Install dependencies, create .env file, and collect static files in a single layer
RUN pip install -r requirements.txt && \
    echo "DJANGO_SECRET_KEY=development-key-replace-in-production" > .env && \
    echo "DJANGO_DEBUG=True" >> .env && \
    echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env && \
    echo "EMAIL_HOST_USER=your-email@example.com" >> .env && \
    echo "EMAIL_HOST_PASSWORD=your-email-password" >> .env && \
    python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Start command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]