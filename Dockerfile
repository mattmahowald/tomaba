# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml poetry.lock ./
COPY tomaba ./tomaba
COPY README.md ./

# Install Poetry and dependencies
RUN pip install poetry && poetry install --no-interaction

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the bot with the FastAPI server
CMD ["poetry", "run", "python", "tomaba/bot.py"]
