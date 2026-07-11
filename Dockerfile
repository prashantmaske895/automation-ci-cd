FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app

COPY automation/ automation/

RUN pip install --no-cache-dir -r automation/requirements.txt

# Install browser binaries
RUN playwright install chromium

CMD ["pytest", "automation/tests", "-v"]