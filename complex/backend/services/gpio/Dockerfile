FROM python:3.10-slim

# Install system dependencies and git in one layer, then clean apt lists
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential make gcc libpq-dev python3-dev python3-setuptools git && \
    rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . .

RUN git clone https://gitflic.ru/project/repka_pi/repkapigpiofs.git \
 && cd repkapigpiofs \
 && SKIP_DRIVER=1 python3 setup.py install || true \
 && rm -rf /repkapigpiofs

    
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python3 health_check.py

# Command to run the application
CMD ["python3", "gpio.py"]
