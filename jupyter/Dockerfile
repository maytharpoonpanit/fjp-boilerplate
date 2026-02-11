FROM jupyter/scipy-notebook:latest

USER root

# ติดตั้ง Chromium สำหรับ Selenium
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# ติดตั้ง Python Libraries
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt