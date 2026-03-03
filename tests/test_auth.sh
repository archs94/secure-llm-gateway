#!/bin/bash

URL="http://127.0.0.1:8000/generate"
CONTENT_TYPE="Content-Type: application/json"

echo "=== 1️⃣ Valid key + allowed role (user) ==="
curl -s -X POST $URL \
  -H "x-api-key: supersecretkey" \
  -H "x-role: user" \
  -H "$CONTENT_TYPE" \
  -d '{"prompt":"Hello LLM"}'
echo -e "\n"

echo "=== 2️⃣ Valid key + admin role ==="
curl -s -X POST $URL \
  -H "x-api-key: supersecretkey" \
  -H "x-role: admin" \
  -H "$CONTENT_TYPE" \
  -d '{"prompt":"Hello Admin LLM"}'
echo -e "\n"

echo "=== 3️⃣ Valid key + forbidden role (guest) ==="
curl -s -X POST $URL \
  -H "x-api-key: supersecretkey" \
  -H "x-role: guest" \
  -H "$CONTENT_TYPE" \
  -d '{"prompt":"Hello Guest LLM"}'
echo -e "\n"

echo "=== 4️⃣ Wrong API key ==="
curl -s -X POST $URL \
  -H "x-api-key: wrongkey" \
  -H "x-role: user" \
  -H "$CONTENT_TYPE" \
  -d '{"prompt":"Hello LLM"}'
echo -e "\n"

echo "=== 5️⃣ Missing API key ==="
curl -s -X POST $URL \
  -H "x-role: user" \
  -H "$CONTENT_TYPE" \
  -d '{"prompt":"Hello LLM"}'
echo -e "\n"

echo "=== 6️⃣ Missing role (defaults to guest) ==="
curl -s -X POST $URL \
  -H "x-api-key: supersecretkey" \
  -H "$CONTENT_TYPE" \
  -d '{"prompt":"Hello LLM"}'
echo -e "\n"

echo "✅ All auth tests executed"