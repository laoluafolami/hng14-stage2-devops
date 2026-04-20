# syntax=docker/dockerfile:1

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.11-alpine AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: final image ──────────────────────────────────────────────────────
FROM python:3.11-alpine

RUN addgroup -S appuser && adduser -S appuser -G appuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY worker.py .

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), password=os.getenv('REDIS_PASSWORD',None)); r.ping()" || exit 1

CMD ["python", "worker.py"]
