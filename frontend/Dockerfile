# syntax=docker/dockerfile:1

FROM node:20-bullseye AS base
WORKDIR /app

# Install deps
COPY package*.json /app/
RUN npm ci --no-audit --no-fund

# Copy source
COPY . /app

# Expose and run dev server
EXPOSE 4200
ENV HOST=0.0.0.0 PORT=4200 ROLLUP_SKIP_NODEJS_NATIVE=1
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]


