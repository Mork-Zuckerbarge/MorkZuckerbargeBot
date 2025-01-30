# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Start the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
