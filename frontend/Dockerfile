# syntax=docker/dockerfile:1

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /build

COPY package*.json ./
RUN npm ci --omit=dev

# ── Stage 2: final image ──────────────────────────────────────────────────────
FROM node:18-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /build/node_modules ./node_modules
COPY app.js .
COPY views/ ./views/

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "app.js"]