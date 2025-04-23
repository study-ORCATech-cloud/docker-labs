-- Init script for MongoDB
-- Note: MongoDB uses JavaScript for init scripts, not SQL
-- This file is included for demonstration purposes only
-- Actual initialization is handled by the service Python code

-- Create microservices database
-- db = db.getSiblingDB('microservices');

-- Create collections
-- db.createCollection('users');
-- db.createCollection('products');

-- Create indexes
-- db.users.createIndex({ "email": 1 }, { unique: true });
-- db.products.createIndex({ "name": 1 });
-- db.products.createIndex({ "category": 1 });

-- Insert sample data
-- db.users.insertMany([
--   { "name": "John Doe", "email": "john@example.com", "role": "admin" },
--   { "name": "Jane Smith", "email": "jane@example.com", "role": "user" },
--   { "name": "Bob Johnson", "email": "bob@example.com", "role": "user" }
-- ]);

-- db.products.insertMany([
--   { "name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": true },
--   { "name": "Office Chair", "price": 149.99, "category": "Furniture", "in_stock": true },
--   { "name": "Coffee Maker", "price": 89.99, "category": "Appliances", "in_stock": false }
-- ]); 