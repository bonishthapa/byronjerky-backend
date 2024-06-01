# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.local_settings

# Create and set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1
# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
