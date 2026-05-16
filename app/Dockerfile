# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production

# Stage 2: Production (The "Secure" stage)
FROM node:20-alpine
RUN apk add --no-cache tini
WORKDIR /app

# Copy only what we need from the builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Security: Create a non-privileged user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Protect the process with tini (prevents zombie processes)
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "index.js"]