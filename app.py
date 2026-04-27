from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import json
from datetime import datetime, timedelta
import random
from faker import Faker
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "agroconnect_secret_2024")

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    client.admin.command('ping')  # Test connection
    db = client["agroconnect"]
except Exception as e:
    print(f"❌ MongoDB CONNECTION ERROR: {e}")
    print("Make sure MongoDB is running on localhost:27017")
    db = None

# Collections
utilisateurs = db["utilisateurs"]
publications = db["publications"]
communautes = db["communautes"]
produits = db["produits"]
commandes = db["commandes"]
notifications = db["notifications"]
avis = db["avis"]  # NEW: Product reviews

REGIONS = ["Dakar","Thiès","Saint-Louis","Ziguinchor","Kaolack","Diourbel","Tambacounda","Kolda","Fatick","Kaffrine"]
CULTURES = ["Mil","Arachide","Riz","Maïs","Coton","Sorgho","Niébé","Sésame","Pastèque","Tomate"]
TAGS_LIST = ["irrigation","semences","engrais","récolte","élevage","maraîchage","exportation","météo","marché","technologie"]
AVATARS = ["🌾","🌻","🌽","🥜","🍅","🌿","🐄","🐑","🌱","🍃"]

fake = Faker('fr_FR')

def serialize(obj):
    return json.loads(dumps(obj))

# ===== DECORATEURS =====
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
        if not me or me.get("role") != "admin":
            return jsonify({"error": "Accès refusé. Admin requis."}), 403
        return f(*args, **kwargs)
    return decorated_function

# ===== DATABASE INITIALIZATION =====
def init_db():
    utilisateurs.delete_many({})
    publications.delete_many({})
    produits.delete_many({})
    commandes.delete_many({})
    notifications.delete_many({})
    communautes.delete_many({})
    avis.delete_many({})
    
    if True:
        NOMS_SN = [
            ("Babacar Cisse", "babacar_agro"),
            ("Aissatou Diagne", "aissatou_farmers"),
        ]
        users = []
        for i in range(2):
            nom, pseudo = NOMS_SN[i]
            u = {
                "pseudo": pseudo,
                "nom": nom,
                "region": random.choice(REGIONS),
                "type_culture": random.choice(CULTURES),
                "bio": f"Agriculteur passionné de {random.choice(CULTURES).lower()}",
                "avatar": AVATARS[i],
                "followers": [],
                "following": [],
                "date_inscription": datetime.now(),
                "cover_color": random.choice(["#2d6a4f","#1b4332","#40916c","#52b788","#1d3557","#457b9d","#6b4226","#a67c52"]),
                "password_hash": generate_password_hash("agroconnect2024"),
                "role": "admin",
                "email": f"{pseudo}@agroconnect.sn",
                "verified": True,
                "blocked": False
            }
            users.append(u)
        
        result = utilisateurs.insert_many(users)
        ids = result.inserted_ids
        
        # Mutual follow
        if len(ids) == 2:
            utilisateurs.update_one({"_id": ids[0]}, {"$set": {"following": [ids[1]]}})
            utilisateurs.update_one({"_id": ids[1]}, {"$set": {"following": [ids[0]]}})
            utilisateurs.update_one({"_id": ids[0]}, {"$set": {"followers": [ids[1]]}})
            utilisateurs.update_one({"_id": ids[1]}, {"$set": {"followers": [ids[0]]}})
        
        # Sample publications
        contenu_exemples = [
            "Belle récolte ce matin ! Les pluies ont été généreuses cette saison. 🌧️",
            "Nouveau système d'irrigation installé. Économie d'eau remarquable !",
            "Qui connaît un bon fournisseur de semences certifiées à Kaolack ?",
            "Marché de Thiès demain matin. J'amène 200 kg d'arachides fraîches.",
        ]
        all_users = list(utilisateurs.find())
        for i, c in enumerate(contenu_exemples):
            auteur = all_users[i % len(all_users)]
            pub = {
                "auteur_id": auteur["_id"],
                "auteur_pseudo": auteur["pseudo"],
                "auteur_avatar": auteur["avatar"],
                "contenu": c,
                "tags": random.sample(TAGS_LIST, random.randint(1,3)),
                "likes": random.sample([u["_id"] for u in all_users], random.randint(0, len(all_users))),
                "commentaires": [],
                "date": datetime(2024, random.randint(1,12), random.randint(1,28))
            }
            publications.insert_one(pub)
        
        # Communities
        comms = [
            {"nom":"Irrigateurs du Sahel","description":"Techniques d'irrigation adaptées au climat sahélien.","emoji":"💧","membres":[],"tags":["irrigation"]},
            {"nom":"Éleveurs Sénégalais","description":"Communauté des éleveurs de bovins, ovins et caprins.","emoji":"🐄","membres":[],"tags":["élevage"]},
            {"nom":"Marché Agro Export","description":"Connexion entre producteurs et marchés internationaux.","emoji":"🌍","membres":[],"tags":["exportation"]},
            {"nom":"Agriculture Bio","description":"Pratiques agroécologiques et agriculture durable.","emoji":"🌿","membres":[],"tags":["bio"]},
        ]
        communautes.insert_many(comms)
        
        # Products with working images from Unsplash (free stock photos)
        all_users = list(utilisateurs.find())
        produits_data = [
            # LEGUMES
            {"nom":"Tomates fraîches", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 500, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ff4444' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3ETomatoes%3C/text%3E%3C/svg%3E", "description": "Tomates rouges juteuses directement du champ", "stock": 50, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.5, "nb_avis": 8},
            {"nom":"Oignons blancs", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Légumes", "prix": 300, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23f4d03f' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EOnions%3C/text%3E%3C/svg%3E", "description": "Oignons blancs de qualité supérieure", "stock": 75, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.2, "nb_avis": 6},
            {"nom":"Carottes orange", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 400, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ff8800' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3ECarrots%3C/text%3E%3C/svg%3E", "description": "Carottes fraîches pleines de vitamines", "stock": 60, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.7, "nb_avis": 10},
            {"nom":"Poivrons rouges", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Légumes", "prix": 600, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23dd2222' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EPeppers%3C/text%3E%3C/svg%3E", "description": "Poivrons rouges juteux et savoureux", "stock": 45, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.6, "nb_avis": 11},
            {"nom":"Aubergines violettes", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Légumes", "prix": 550, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23662277' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EEggplants%3C/text%3E%3C/svg%3E", "description": "Aubergines violettes de qualité premium", "stock": 55, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.1, "nb_avis": 5},
            {"nom":"Laitue fraîche", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 350, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%2390ee90' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3ELettuce%3C/text%3E%3C/svg%3E", "description": "Laitue verte tendre et croquante", "stock": 80, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.4, "nb_avis": 9},
            {"nom":"Piments verts", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 400, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%2399dd00' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EPeppers%3C/text%3E%3C/svg%3E", "description": "Piments verts frais pour vos plats", "stock": 40, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.3, "nb_avis": 7},
            # FRUITS
            {"nom":"Pastèques sucrées", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Fruits", "prix": 2000, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ee3311' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EWatermelons%3C/text%3E%3C/svg%3E", "description": "Pastèques juteuses et sucrées du Sénégal", "stock": 20, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.8, "nb_avis": 12},
            {"nom":"Mangues Ataulfo", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Fruits", "prix": 1500, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ffaa33' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EMangoes%3C/text%3E%3C/svg%3E", "description": "Mangues de saison au goût exceptionnel", "stock": 35, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.9, "nb_avis": 15},
            {"nom":"Papayes jaunes", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Fruits", "prix": 1200, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ff9944' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EPapayas%3C/text%3E%3C/svg%3E", "description": "Papayes jaunes bien mûres et juteuses", "stock": 40, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.3, "nb_avis": 7},
            {"nom":"Agrumes mélangés", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Fruits", "prix": 1800, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ffcc00' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3ECitrus%3C/text%3E%3C/svg%3E", "description": "Oranges, citrons, pamplemousses frais", "stock": 100, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.5, "nb_avis": 8},
            {"nom":"Bananes plantain", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Fruits", "prix": 700, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23ffdd00' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EBananas%3C/text%3E%3C/svg%3E", "description": "Bananes plantain mûres et savoureuses", "stock": 60, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.4, "nb_avis": 9},
            {"nom":"Goyaves roses", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Fruits", "prix": 900, "image": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect fill='%23dd9955' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='24' fill='white' font-weight='bold'%3EGuavas%3C/text%3E%3C/svg%3E", "description": "Goyaves roses fraîches et parfumées", "stock": 50, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now(), "note_moyenne": 4.6, "nb_avis": 10},
        ]
        produits.insert_many(produits_data)
        print("✅ Database initialized successfully")

# Initialize DB on startup
if db is not None:
    try:
        init_db()
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
else:
    print("❌ Cannot initialize database - MongoDB not connected")

# ===== AUTH ROUTES =====
@app.route("/login", methods=["GET","POST"])
def login():
    print(f"📌 /login {request.method}")
    
    if request.method == "POST":
        pseudo_or_nom = request.form.get("pseudo","").strip()
        password = request.form.get("password","").strip()
        
        print(f"🔐 Login attempt: {pseudo_or_nom}")
        
        if not pseudo_or_nom or not password:
            print("❌ Missing pseudo or password")
            return render_template("login.html", error="Pseudo/Nom et mot de passe requis")
        
        # Cherche par pseudo OU par nom
        user = utilisateurs.find_one({"$or": [
            {"pseudo": pseudo_or_nom},
            {"nom": pseudo_or_nom}
        ]})
        
        if not user:
            print(f"❌ User not found: {pseudo_or_nom}")
            return render_template("login.html", error="Identifiants incorrects")
        
        if not check_password_hash(user["password_hash"], password):
            print(f"❌ Wrong password for {user.get('pseudo')}")
            return render_template("login.html", error="Identifiants incorrects")
        
        session["user_id"] = str(user["_id"])
        session["pseudo"] = user["pseudo"]
        session["role"] = user.get("role", "user")
        print(f"✅ Login successful: {user.get('pseudo')}")
        return redirect(url_for("home"))
    
    # GET /login
    try:
        users = list(utilisateurs.find({}, {"pseudo": 1, "nom": 1}))
        print(f"✅ Found {len(users)} test users")
    except Exception as e:
        print(f"❌ Error finding users: {e}")
        users = []
    
    return render_template("login.html", test_accounts=users)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        pseudo = request.form.get("pseudo","").strip()
        nom = request.form.get("nom","").strip()
        region = request.form.get("region")
        type_culture = request.form.get("type_culture")
        password = request.form.get("password","").strip()
        password_confirm = request.form.get("password_confirm","").strip()
        
        errors = []
        if len(pseudo) < 3:
            errors.append("Pseudo: minimum 3 caractères")
        if len(password) < 6:
            errors.append("Mot de passe: minimum 6 caractères")
        if password != password_confirm:
            errors.append("Les mots de passe ne correspondent pas")
        if utilisateurs.find_one({"pseudo": pseudo}):
            errors.append("Ce pseudo est déjà utilisé")
        if not nom or not region or not type_culture:
            errors.append("Tous les champs sont requis")
        
        if errors:
            return render_template("register.html", errors=errors), 400
        
        new_user = {
            "pseudo": pseudo,
            "nom": nom,
            "region": region,
            "type_culture": type_culture,
            "bio": "",
            "avatar": random.choice(AVATARS),
            "followers": [],
            "following": [],
            "date_inscription": datetime.now(),
            "cover_color": random.choice(["#2d6a4f","#1b4332","#40916c","#52b788","#1d3557","#457b9d","#6b4226","#a67c52"]),
            "password_hash": generate_password_hash(password),
            "role": "user",
            "email": f"{pseudo}@agroconnect.sn",
            "verified": False,
            "blocked": False
        }
        
        result = utilisateurs.insert_one(new_user)
        session["user_id"] = str(result.inserted_id)
        session["pseudo"] = pseudo
        session["role"] = "user"
        
        return redirect(url_for("home"))
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===== MAIN ROUTES =====
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("home"))

@app.route("/home")
@login_required
def home():
    print(f"📌 /home accessed, user_id: {session.get('user_id')}")
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    if not me:
        print(f"❌ User not found in /home: {session.get('user_id')}")
        session.clear()
        return redirect(url_for("login"))
    print(f"✅ /home loading for {me.get('pseudo')}")
    is_admin = me.get("role") == "admin"
    return render_template("home.html", me=serialize(me), is_admin=is_admin)

@app.route("/marche")
@login_required
def marche():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    if not me:
        session.clear()
        return redirect(url_for("login"))
    is_admin = me.get("role") == "admin"
    
    # Get cart from session
    cart = session.get("cart", [])
    
    return render_template("marche.html", me=serialize(me), is_admin=is_admin, cart=cart)

@app.route("/vendeur/<pseudo>")
@login_required
def vendeur_profile(pseudo):
    """Public vendor profile"""
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    if not me:
        session.clear()
        return redirect(url_for("login"))
    
    vendeur = utilisateurs.find_one({"pseudo": pseudo})
    
    if not vendeur:
        return "Vendeur non trouvé", 404
    
    vendeur_products = list(produits.find({"vendeur_id": vendeur["_id"]}, limit=20))
    
    return render_template("vendeur_profile.html", 
                         me=serialize(me), 
                         vendeur=serialize(vendeur), 
                         products=serialize(vendeur_products))

@app.route("/admin")
@admin_required
def admin_dashboard():
    # Admin-only statistics
    total_users = utilisateurs.count_documents({})
    total_admins = utilisateurs.count_documents({"role": "admin"})
    total_publications = publications.count_documents({})
    total_communities = communautes.count_documents({})
    total_orders = commandes.count_documents({})
    total_products = produits.count_documents({})
    
    # Recent orders
    recent_orders = list(commandes.find().sort("date_commande", -1).limit(10))
    
    # Top products
    top_products = list(produits.find().sort("nb_avis", -1).limit(5))
    
    return render_template("admin.html",
                         total_users=total_users,
                         total_admins=total_admins,
                         total_publications=total_publications,
                         total_communities=total_communities,
                         total_orders=total_orders,
                         total_products=total_products,
                         recent_orders=serialize(recent_orders),
                         top_products=serialize(top_products))

# ===== API: PRODUCTS =====
@app.route("/api/me")
@login_required
def api_me():
    try:
        if db is None:
            print("❌ Database not connected in /api/me")
            return jsonify({"error": "Database not connected"}), 503
        
        user_id = session.get("user_id")
        print(f"📌 /api/me called with user_id: {user_id}")
        
        if not user_id:
            print("❌ No user_id in session")
            return jsonify({"error": "No user_id"}), 401
        
        me = utilisateurs.find_one({"_id": ObjectId(user_id)})
        if not me:
            print(f"❌ User not found: {user_id}")
            return jsonify({"error": "Utilisateur non trouvé"}), 404
        
        me_data = serialize(me)
        me_data["nb_followers"] = len(me_data.get("followers", []))
        me_data["nb_following"] = len(me_data.get("following", []))
        print(f"✅ Returning user: {me_data.get('pseudo')}")
        return jsonify(me_data)
    except Exception as e:
        print(f"❌ Error in /api/me: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/feed")
@login_required
def api_feed():
    """Retourne le fil d'actualité avec les publications"""
    try:
        tag = request.args.get("tag")
        user_id = request.args.get("user_id")
        
        filters = {}
        if tag:
            filters["tags"] = tag
        if user_id:
            filters["auteur_id"] = ObjectId(user_id)
        
        pubs = list(publications.find(filters).sort("date", -1).limit(50))
        result = []
        
        for pub in pubs:
            result.append({
                "_id": str(pub.get("_id")),
                "auteur_id": str(pub.get("auteur_id")),
                "auteur_pseudo": pub.get("auteur_pseudo"),
                "auteur_avatar": pub.get("auteur_avatar"),
                "contenu": pub.get("contenu"),
                "tags": pub.get("tags", []),
                "nb_likes": len(pub.get("likes", [])),
                "liked_by_me": ObjectId(session.get("user_id")) in pub.get("likes", []),
                "commentaires": pub.get("commentaires", []),
                "date": str(pub.get("date", ""))
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in /api/feed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/utilisateurs")
def api_utilisateurs():
    """Retourne la liste des utilisateurs (pseudos et avatars) pour la page login"""
    try:
        if db is None:
            return jsonify({"error": "Database not connected"}), 503
        users = list(utilisateurs.find({}, {"pseudo": 1, "avatar": 1, "nom": 1}))
        result = []
        for u in users:
            result.append({
                "pseudo": u["pseudo"],
                "avatar": u.get("avatar", "🌾"),
                "nom": u.get("nom", "")
            })
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in /api/utilisateurs: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/produits")
def api_produits():
    categorie = request.args.get("categorie", "")
    prix_min = request.args.get("prix_min", type=int, default=0)
    prix_max = request.args.get("prix_max", type=int, default=999999)
    region = request.args.get("region", "")
    search = request.args.get("search", "")
    
    filters = {}
    if categorie:
        filters["categorie"] = categorie
    filters["prix"] = {"$gte": prix_min, "$lte": prix_max}
    if region:
        filters["region"] = region
    if search:
        filters["nom"] = {"$regex": search, "$options": "i"}
    
    prods = list(produits.find(filters))
    result = []
    for p in prods:
        result.append({
            "_id": str(p["_id"]),
            "nom": p["nom"],
            "categorie": p["categorie"],
            "prix": p["prix"],
            "image": p["image"],
            "description": p["description"],
            "stock": p["stock"],
            "disponible": p["disponible"],
            "vendeur_pseudo": p["vendeur_pseudo"],
            "vendeur_avatar": p["vendeur_avatar"],
            "region": p["region"],
            "note_moyenne": p.get("note_moyenne", 0),
            "nb_avis": p.get("nb_avis", 0)
        })
    
    return jsonify(result)

# ===== API: ORDERS & CART =====
@app.route("/api/commander", methods=["POST"])
@login_required
def commander():
    data = request.json
    produit_id = data.get("produit_id")
    quantite = data.get("quantite", 1)
    
    if not produit_id or quantite < 1:
        return jsonify({"error": "Données invalides"}), 400
    
    prod = produits.find_one({"_id": ObjectId(produit_id)})
    if not prod or prod["stock"] < quantite:
        return jsonify({"error": "Stock insuffisant"}), 400
    
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    
    commande = {
        "acheteur_id": me["_id"],
        "acheteur_pseudo": me["pseudo"],
        "vendeur_id": prod["vendeur_id"],
        "vendeur_pseudo": prod["vendeur_pseudo"],
        "produit_id": prod["_id"],
        "produit_nom": prod["nom"],
        "quantite": quantite,
        "prix_unitaire": prod["prix"],
        "prix_total": prod["prix"] * quantite,
        "date_commande": datetime.now(),
        "statut": "En attente",
        "livrable": False
    }
    
    result = commandes.insert_one(commande)
    
    # Decrease stock
    produits.update_one({"_id": prod["_id"]}, {"$inc": {"stock": -quantite}})
    
    # Notify vendor
    notif = {
        "destinataire_id": prod["vendeur_id"],
        "type": "nouvelle_commande",
        "titre": f"Nouvelle commande de {me['pseudo']}",
        "message": f"{me['pseudo']} a commandé {quantite}x {prod['nom']}",
        "acheteur_pseudo": me["pseudo"],
        "acheteur_avatar": me["avatar"],
        "produit_nom": prod["nom"],
        "quantite": quantite,
        "prix_total": commande["prix_total"],
        "date": datetime.now(),
        "lue": False
    }
    notifications.insert_one(notif)
    
    return jsonify({"success": True, "commande_id": str(result.inserted_id)})

@app.route("/api/mes-commandes")
@login_required
def mes_commandes():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    cmds = list(commandes.find({"acheteur_id": me["_id"]}).sort("date_commande", -1))
    return jsonify(serialize(cmds))

@app.route("/api/commandes-recues")
@login_required
def commandes_recues():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    cmds = list(commandes.find({"vendeur_id": me["_id"]}).sort("date_commande", -1))
    return jsonify(serialize(cmds))

# ===== API: REVIEWS =====
@app.route("/api/produit/<produit_id>/avis", methods=["GET"])
def get_avis(produit_id):
    """Get reviews for a product"""
    reviews = list(avis.find({"produit_id": ObjectId(produit_id)}).sort("date", -1).limit(10))
    return jsonify(serialize(reviews))

@app.route("/api/avis/creer", methods=["POST"])
@login_required
def creer_avis():
    """Create a review for a product"""
    data = request.json
    produit_id = data.get("produit_id")
    note = data.get("note", 5)
    commentaire = data.get("commentaire", "")
    
    if not produit_id or not (1 <= note <= 5):
        return jsonify({"error": "Données invalides"}), 400
    
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    prod = produits.find_one({"_id": ObjectId(produit_id)})
    
    if not prod:
        return jsonify({"error": "Produit non trouvé"}), 404
    
    # Check if user already reviewed
    existing = avis.find_one({"produit_id": prod["_id"], "auteur_id": me["_id"]})
    if existing:
        return jsonify({"error": "Vous avez déjà évalué ce produit"}), 400
    
    review = {
        "produit_id": prod["_id"],
        "produit_nom": prod["nom"],
        "auteur_id": me["_id"],
        "auteur_pseudo": me["pseudo"],
        "auteur_avatar": me["avatar"],
        "note": note,
        "commentaire": commentaire,
        "date": datetime.now(),
        "modere": False
    }
    
    result = avis.insert_one(review)
    
    # Update product rating
    all_reviews = list(avis.find({"produit_id": prod["_id"]}))
    avg_note = sum(r["note"] for r in all_reviews) / len(all_reviews) if all_reviews else 0
    nb_avis = len(all_reviews)
    
    produits.update_one({"_id": prod["_id"]}, {"$set": {"note_moyenne": avg_note, "nb_avis": nb_avis}})
    
    return jsonify({"success": True, "avis_id": str(result.inserted_id)})

# ===== API: NOTIFICATIONS =====
@app.route("/api/notifications")
@login_required
def get_notifications():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    notifs = list(notifications.find({"destinataire_id": me["_id"]}).sort("date", -1).limit(20))
    return jsonify(serialize(notifs))

@app.route("/api/notification/<notif_id>/lire", methods=["POST"])
@login_required
def marquer_lue(notif_id):
    notifications.update_one({"_id": ObjectId(notif_id)}, {"$set": {"lue": True}})
    return jsonify({"success": True})

# ===== API: FOLLOW/UNFOLLOW =====
@app.route("/api/utilisateur/<user_id>/follow", methods=["POST"])
@login_required
def follow_user(user_id):
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    target = utilisateurs.find_one({"_id": ObjectId(user_id)})
    
    if not target:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    
    # Add to my following
    if ObjectId(user_id) not in me.get("following", []):
        utilisateurs.update_one({"_id": me["_id"]}, {"$push": {"following": target["_id"]}})
    
    # Add me to their followers
    if me["_id"] not in target.get("followers", []):
        utilisateurs.update_one({"_id": target["_id"]}, {"$push": {"followers": me["_id"]}})
    
    return jsonify({"success": True})

@app.route("/api/utilisateur/<user_id>/unfollow", methods=["POST"])
@login_required
def unfollow_user(user_id):
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    
    utilisateurs.update_one({"_id": me["_id"]}, {"$pull": {"following": ObjectId(user_id)}})
    utilisateurs.update_one({"_id": ObjectId(user_id)}, {"$pull": {"followers": me["_id"]}})
    
    return jsonify({"success": True})

# ===== API: ADMIN ONLY =====
@app.route("/api/admin/stats")
@admin_required
def admin_stats():
    return jsonify({
        "total_users": utilisateurs.count_documents({}),
        "total_admins": utilisateurs.count_documents({"role": "admin"}),
        "total_publications": publications.count_documents({}),
        "total_communities": communautes.count_documents({})
    })

@app.route("/api/admin/utilisateurs")
@admin_required
def admin_utilisateurs():
    users = list(utilisateurs.find())
    return jsonify(serialize(users))

@app.route("/api/admin/utilisateur/<user_id>/role", methods=["POST"])
@admin_required
def toggle_role(user_id):
    user = utilisateurs.find_one({"_id": ObjectId(user_id)})
    new_role = "user" if user.get("role") == "admin" else "admin"
    utilisateurs.update_one({"_id": user["_id"]}, {"$set": {"role": new_role}})
    return jsonify({"success": True, "new_role": new_role})

@app.route("/api/admin/utilisateur/<user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    utilisateurs.delete_one({"_id": ObjectId(user_id)})
    commandes.delete_many({"acheteur_id": ObjectId(user_id)})
    return jsonify({"success": True})

@app.route("/api/admin/utilisateur/<user_id>/block", methods=["POST"])
@admin_required
def block_user(user_id):
    utilisateurs.update_one({"_id": ObjectId(user_id)}, {"$set": {"blocked": True}})
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False") == "True", host="0.0.0.0", port=5000)
