FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver chromium xvfb x11vnc \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code (including static/novnc)
COPY . /app

# Ensure novnc_proxy is executable
RUN chmod +x /app/static/novnc/utils/novnc_proxy

# Expose ports
EXPOSE 5000 5900 6080

# Start everything
CMD ["bash", "-c", "\
rm -f /tmp/.X99-lock; \
Xvfb :99 -screen 0 1280x720x24 & \
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 & \
/app/static/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 & \
python3 main.py \
"] 