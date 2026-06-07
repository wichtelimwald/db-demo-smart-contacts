FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore --upgrade pip \
    && pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY yaml_to_json.py .
COPY main.py .

# YAML → JSON beim Start, dann Server hochfahren
CMD ["sh", "-c", "python3 yaml_to_json.py && python3 main.py"]
