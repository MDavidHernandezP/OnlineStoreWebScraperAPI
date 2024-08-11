# Use an official Python 3.10 image as the base image.
FROM python:3.10-slim

# Set the working directory to /app.
WORKDIR /app

# Copy the requirements.txt file and install dependencies.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container.
COPY . .

# Define the command to run your FastAPI app with Uvicorn.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]