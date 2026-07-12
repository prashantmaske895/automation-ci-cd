FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app

COPY automation/ automation/

RUN pip install --no-cache-dir -r automation/requirements.txt

# Install browser binaries
RUN playwright install chromium

# Create reports directory
RUN mkdir -p /app/automation/reports

CMD pytest automation/tests -v \
    --html=automation/reports/report.html \
    --self-contained-html \
    --junitxml=automation/reports/results.xml