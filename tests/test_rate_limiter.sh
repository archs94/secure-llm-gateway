#!/bin/bash

URL="http://127.0.0.1:8000/generate"
CONTENT_TYPE="Content-Type: application/json"

echo "========================================"
echo "🚦 Testing USER rate limit (5 per minute)"
echo "========================================"

for i in {1..6}
do
  echo "Request $i:"
  curl -s -o response.txt -w "Status: %{http_code}\n" \
    -X POST $URL \
    -H "x-api-key: supersecretkey" \
    -H "x-role: user" \
    -H "$CONTENT_TYPE" \
    -d '{"prompt":"Rate limit test"}'
  
  cat response.txt
  echo -e "\n--------------------------"
done

echo ""
echo "========================================"
echo "👑 Testing ADMIN (should be unlimited)"
echo "========================================"

for i in {1..7}
do
  echo "Admin Request $i:"
  curl -s -o response.txt -w "Status: %{http_code}\n" \
    -X POST $URL \
    -H "x-api-key: supersecretkey" \
    -H "x-role: admin" \
    -H "$CONTENT_TYPE" \
    -d '{"prompt":"Admin test"}'
  
  cat response.txt
  echo -e "\n--------------------------"
done

rm response.txt

echo "✅ Rate limit test completed"