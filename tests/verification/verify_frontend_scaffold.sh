#!/bin/bash
if [ ! -d "frontend" ]; then
  echo "FAIL: frontend directory does not exist"
  exit 1
fi
if [ ! -f "frontend/package.json" ]; then
  echo "FAIL: frontend/package.json does not exist"
  exit 1
fi
if ! grep -q "next" "frontend/package.json"; then
  echo "FAIL: next dependency not found"
  exit 1
fi
if ! grep -q "tailwindcss" "frontend/package.json"; then
  echo "FAIL: tailwindcss dependency not found"
  exit 1
fi
echo "PASS: Frontend scaffolding verified"
exit 0
