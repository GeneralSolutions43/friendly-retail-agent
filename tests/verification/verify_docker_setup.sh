#!/bin/bash
if [ ! -f "backend/Dockerfile" ]; then
  echo "FAIL: backend/Dockerfile does not exist"
  exit 1
fi
if [ ! -f "frontend/Dockerfile" ]; then
  echo "FAIL: frontend/Dockerfile does not exist"
  exit 1
fi
if [ ! -f "docker-compose.yml" ]; then
  echo "FAIL: docker-compose.yml does not exist"
  exit 1
fi
echo "PASS: Docker configuration files verified"
exit 0