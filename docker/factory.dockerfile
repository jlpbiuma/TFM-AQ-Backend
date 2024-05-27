FROM python:latest

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./sql-scripts/factories/ .

CMD ["python", "-u", "factory.py"]