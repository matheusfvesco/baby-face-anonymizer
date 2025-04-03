FROM python:3.10-slim-bookworm

COPY requirements.txt .

COPY api.py .

RUN mkdir -p runs/detect/train/weights

COPY runs/detect/train/weights/best.pt runs/detect/train/weights

RUN pip install -r requirements.txt

RUN apt update \
    && apt install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

CMD ["fastapi", "run", "api.py"]