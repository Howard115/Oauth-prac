#!/bin/bash

# Test dependencies with valid headers
# 使用有效的请求头测试依赖项
echo "Testing with valid headers..."
curl -X GET "http://localhost:8000/items/" \
-H "X-Token: fake-super-secret-token" \
-H "X-Key: fake-super-secret-key" \
-w "\nStatus code: %{http_code}\n"

echo -e "\n"

# Test dependencies with invalid token
# 使用无效令牌测试依赖项
echo "Testing with invalid token..."
curl -X GET "http://localhost:8000/items/" \
-H "X-Token: wrong-token" \
-H "X-Key: fake-super-secret-key" \
-w "\nStatus code: %{http_code}\n"

echo -e "\n"

# Test dependencies with invalid key
# 使用无效密钥测试依赖项
echo "Testing with invalid key..."
curl -X GET "http://localhost:8000/items/" \
-H "X-Token: fake-super-secret-token" \
-H "X-Key: wrong-key" \
-w "\nStatus code: %{http_code}\n"

echo -e "\n"

# Test dependencies with both invalid token and key
# 使用无效的令牌和密钥测试依赖项
echo "Testing with both invalid token and key..."
curl -X GET "http://localhost:8000/items/" \
-H "X-Token: wrong-token" \
-H "X-Key: wrong-key" \
-w "\nStatus code: %{http_code}\n"

echo -e "\n"


# Test dependencies with missing headers
# 使用缺失的请求头测试依赖项
echo "Testing with missing headers..."
curl -X GET "http://localhost:8000/items/" \
-w "\nStatus code: %{http_code}\n"

echo -e "\n"
