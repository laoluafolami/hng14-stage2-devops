# syntax=docker/dockerfile:1

FROM node:18-alpine AS builder

WORKDIR /build

COPY package*.json ./
RUN npm ci --omit=dev

FROM node:18-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /build/node_modules ./node_modules
COPY app.js .
COPY views/ ./views/

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=10s --start-period=30s --retries=5 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) }).on('error', () => process.exit(1))"

CMD ["node", "app.js"]
