# Stage 1: Build the application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --force

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Stage 2: Production image
FROM node:20-alpine AS runner

WORKDIR /app

# Copy necessary files from builder
COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

# Environment variables
ENV NODE_ENV development
ENV PORT 3000
ENV BACKEND_URL http://api:8000

# Expose the port
EXPOSE 3000