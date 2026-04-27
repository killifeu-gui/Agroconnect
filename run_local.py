#!/usr/bin/env python3
"""
Quick deployment script - Lance AgroConnect localement avec tunnel public
"""
import os
import sys
import subprocess
import time

print("=" * 60)
print("🚀 AGROCONNECT - DÉPLOIEMENT RAPIDE")
print("=" * 60)

# 1. Vérifier MongoDB
print("\n📊 Vérification MongoDB...")
try:
    from pymongo import MongoClient
    # Test de connexion locale
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.admin.command('ping')
    print("✅ MongoDB local détecté sur localhost:27017")
    os.environ['MONGO_URI'] = 'mongodb://localhost:27017/'
except Exception as e:
    print(f"⚠️  MongoDB local non détecté: {e}")
    print("   → Utilisation de mongoDB cloud (si configuré)")

# 2. Lancer le serveur Flask
print("\n🌐 Lancement du serveur Flask...")
print("   → Adresse locale: http://127.0.0.1:5000")
print("   → Adresse réseau: http://192.168.1.XXX:5000 (remplacez XXX)")
print("\n🔐 Identifiants test:")
print("   Username: babacar_agro")
print("   Password: agroconnect2024")
print("\n" + "=" * 60)

# Lancer Flask
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = 'False'

try:
    # Lancer directement Python app.py
    subprocess.run([sys.executable, 'app.py'], cwd=os.getcwd())
except KeyboardInterrupt:
    print("\n\n❌ Serveur arrêté")
    sys.exit(0)
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)
