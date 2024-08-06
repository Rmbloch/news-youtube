FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

RUN sed -i 's/<policymap domain="resource" name="width" value=".*"/<policymap domain="resource" name="width" value="1920"/' /etc/ImageMagick-6/policy.xml && \
    sed -i 's/<policymap domain="resource" name="height" value=".*"/<policymap domain="resource" name="height" value="1080"/' /etc/ImageMagick-6/policy.xml && \
    sed -i '/pattern="@\*"/s/rights="none"/rights="read|write"/' /etc/ImageMagick-6/policy.xml

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container at /app
COPY script.py /app/script.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Run script.py when the container launches
CMD ["python", "script.py"]
