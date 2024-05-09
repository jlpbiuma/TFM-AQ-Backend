# Use the official Python image from Docker Hub
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which your Flask app will run
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
