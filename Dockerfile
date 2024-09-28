FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port your application runs on
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Apply database migrations
RUN python manage.py migrate

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Educationtracker.wsgi:application"]
