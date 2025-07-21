FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver chromium xvfb x11vnc wget unzip bsdtar \
    && rm -rf /var/lib/apt/lists/*

# Install noVNC
RUN mkdir -p /novnc && \
    wget -qO- https://github.com/novnc/noVNC/archive/refs/tags/v1.4.0.zip | bsdtar -xvf- -C /novnc --strip-components=1

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app

# Expose ports
EXPOSE 5000 5900 6080

# Start everything
CMD ["bash", "-c", "\
Xvfb :99 -screen 0 1280x720x24 & \
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 & \
/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 & \
python3 main.py \
"] 