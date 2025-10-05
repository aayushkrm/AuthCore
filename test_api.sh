#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000/api"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Custom Auth System - API Tests${NC}"
echo -e "${BLUE}================================${NC}\n"

# Test 1: Register new user
echo -e "${YELLOW}Test 1: Register new user${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "password_confirmation": "password123"
  }')
echo $REGISTER_RESPONSE | python -m json.tool
echo -e "\n"

# Test 2: Login as regular user
echo -e "${YELLOW}Test 2: Login as regular user${NC}"
USER_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user1@test.com",
    "password": "password123"
  }' | python -c "import sys, json; print(json.load(sys.stdin)['token'])")
echo -e "${GREEN}✓ Token obtained${NC}\n"

# Test 3: Get user profile
echo -e "${YELLOW}Test 3: Get user profile${NC}"
curl -s -X GET "$BASE_URL/auth/profile/" \
  -H "Authorization: Bearer $USER_TOKEN" | python -m json.tool
echo -e "\n"

# Test 4: List products (user should see only their products)
echo -e "${YELLOW}Test 4: List products as regular user${NC}"
curl -s -X GET "$BASE_URL/products/" \
  -H "Authorization: Bearer $USER_TOKEN" | python -m json.tool
echo -e "\n"

# Test 5: Create product
echo -e "${YELLOW}Test 5: Create product${NC}"
curl -s -X POST "$BASE_URL/products/" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Test Product",
    "price": 99.99,
    "category": "Test"
  }' | python -m json.tool
echo -e "\n"

# Test 6: Try to access admin endpoint (should fail with 403)
echo -e "${YELLOW}Test 6: Try to access admin endpoint as regular user (expect 403)${NC}"
curl -s -X GET "$BASE_URL/access-rules/" \
  -H "Authorization: Bearer $USER_TOKEN" | python -m json.tool
echo -e "\n"

# Test 7: Login as admin
echo -e "${YELLOW}Test 7: Login as admin${NC}"
ADMIN_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "password123"
  }' | python -c "import sys, json; print(json.load(sys.stdin)['token'])")
echo -e "${GREEN}✓ Admin token obtained${NC}\n"

# Test 8: List all access rules as admin
echo -e "${YELLOW}Test 8: List all access rules as admin${NC}"
curl -s -X GET "$BASE_URL/access-rules/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python -m json.tool | head -20
echo -e "... (truncated)\n"

# Test 9: List all products as admin (should see all)
echo -e "${YELLOW}Test 9: List all products as admin${NC}"
curl -s -X GET "$BASE_URL/products/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python -m json.tool
echo -e "\n"

# Test 10: List orders
echo -e "${YELLOW}Test 10: List orders as admin${NC}"
curl -s -X GET "$BASE_URL/orders/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python -m json.tool
echo -e "\n"

# Test 11: List stores
echo -e "${YELLOW}Test 11: List stores as admin${NC}"
curl -s -X GET "$BASE_URL/stores/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python -m json.tool
echo -e "\n"

# Test 12: Update profile
echo -e "${YELLOW}Test 12: Update user profile${NC}"
curl -s -X PUT "$BASE_URL/auth/profile/" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name"
  }' | python -m json.tool
echo -e "\n"

# Test 13: Test with invalid token (should get 401)
echo -e "${YELLOW}Test 13: Test with invalid token (expect 401)${NC}"
curl -s -X GET "$BASE_URL/products/" \
  -H "Authorization: Bearer invalid_token_here" | python -m json.tool
echo -e "\n"

# Test 14: Test without token (should get 401)
echo -e "${YELLOW}Test 14: Test without token (expect 401)${NC}"
curl -s -X GET "$BASE_URL/products/" | python -m json.tool
echo -e "\n"

# Test 15: Logout
echo -e "${YELLOW}Test 15: Logout${NC}"
curl -s -X POST "$BASE_URL/auth/logout/" \
  -H "Authorization: Bearer $USER_TOKEN" | python -m json.tool
echo -e "\n"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}All Tests Complete!${NC}"
echo -e "${GREEN}================================${NC}"
