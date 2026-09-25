# Module 4: CRUD Operations

## 🎯 Learning Objectives

1. Implement complete CRUD operations (Create, Read, Update, Delete)
2. Understand the difference between PUT (full update) and PATCH (partial update)
3. Use proper HTTP methods and status codes
4. Implement data validation and error handling

## 📚 CRUD Operations

### Create (POST)
```bash
POST /shipment
{
  "content": "gaming laptop",
  "weight": 3.5
}