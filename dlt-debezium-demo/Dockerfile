# Dockerfile for dlt-debezium-demo CDC Loader
# Includes Java 17+ (for Debezium) and Python with all dependencies

FROM python:3.11-slim

# Install Java 21 JRE (required for Debezium engine - Java 17+ works)
# Using jre-headless instead of full JDK to reduce image size (~300-400MB smaller)
# Note: Debian Trixie has OpenJDK 21, which is compatible
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Verify Java installation
RUN java -version

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY debezium_dlt_loader.py .
COPY debezium_dlt_loader_mysql.py .
COPY config_helper_universal.py .

# Create .dlt directory for configuration
RUN mkdir -p .dlt

# Default command (can be overridden in docker-compose)
CMD ["python", "debezium_dlt_loader.py"]
