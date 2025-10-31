# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /PROJECT_1_MONGO

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port if needed (not mandatory for scripts)
# EXPOSE 5000

# Set environment variables (optional)
# ENV SENDER_EMAIL=your_email@gmail.com
# ENV RECEIVER_EMAIL=receiver_email@gmail.com
# ENV PASSWORD=your_app_password

# Run the main script
CMD ["python", "update.py"]
