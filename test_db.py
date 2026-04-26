#!/usr/bin/env python
"""Test MongoDB connection and initialization"""
from pymongo import MongoClient
import sys

MONGO_URI = "mongodb://localhost:27017/"

try:
    print("🔍 Testing MongoDB connection...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB is running!")
    
    db = client["agroconnect"]
    users = db["utilisateurs"].count_documents({})
    print(f"📊 Users in database: {users}")
    
    if users > 0:
        user = db["utilisateurs"].find_one({})
        print(f"   First user: {user.get('pseudo')}")
    
except Exception as e:
    print(f"❌ MongoDB ERROR: {e}")
    print("   Make sure MongoDB is running with: mongod")
    sys.exit(1)
