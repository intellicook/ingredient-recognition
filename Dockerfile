# Pull official base image
FROM python:3.12.2-slim

# Set work directory
WORKDIR /usr/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-compile --no-cache-dir -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/app/entrypoint.sh
RUN chmod +x /usr/app/entrypoint.sh

# Copy project
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/usr/app/entrypoint.sh"]
