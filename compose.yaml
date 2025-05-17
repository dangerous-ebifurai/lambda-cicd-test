version: '3.8'

services:
  lambda:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "9000:8080"
    environment:
      - AWS_LAMBDA_RUNTIME_API=http://localhost:9000
    command: ["app.lambda_handler"]
