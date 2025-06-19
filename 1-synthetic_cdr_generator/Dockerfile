# Use slim Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only necessary files, ignoring .venv and other junk
COPY . .

# Delete .venv if it accidentally got copied (safety)
RUN rm -rf .venv

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run the generator
CMD ["python", "main.py"]
