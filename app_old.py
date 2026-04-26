from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import json
from datetime import datetime
import random
from faker import Faker
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "agroconnect_secret_2024"
fake = Faker('fr_FR')

client = MongoClient("mongodb://localhost:27017/")
db = client["agroconnect"]
utilisateurs = db["utilisateurs"]
publications = db["publications"]
communautes = db["communautes"]
produits = db["produits"]
commandes = db["commandes"]
notifications = db["notifications"]

REGIONS = ["Dakar","Thiès","Saint-Louis","Ziguinchor","Kaolack","Diourbel","Tambacounda","Kolda","Fatick","Kaffrine"]
CULTURES = ["Mil","Arachide","Riz","Maïs","Coton","Sorgho","Niébé","Sésame","Pastèque","Tomate"]
TAGS_LIST = ["irrigation","semences","engrais","récolte","élevage","maraîchage","exportation","météo","marché","technologie"]
AVATARS = ["🌾","🌻","🌽","🥜","🍅","🌿","🐄","🐑","🌱","🍃"]

def serialize(obj):
    return json.loads(dumps(obj))

# Décorateurs de protection
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
        if me.get("role") != "admin":
            return jsonify({"error": "Accès refusé. Admin requis."}), 403
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    # Réinitialiser complètement les collections
    utilisateurs.delete_many({})
    publications.delete_many({})
    produits.delete_many({})
    commandes.delete_many({})
    notifications.delete_many({})
    # Garder les communautés ou les réinitialiser aussi
    communautes.delete_many({})
    
    if True:  # Forcer la création des données de base
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
                "bio": fake.sentence(nb_words=10),
                "avatar": AVATARS[i],
                "followers": [],
                "following": [],
                "date_inscription": datetime.now(),
                "cover_color": random.choice(["#2d6a4f","#1b4332","#40916c","#52b788","#1d3557","#457b9d","#6b4226","#a67c52"]),
                "password_hash": generate_password_hash("agroconnect2024"),
                "role": "admin"
            }
            users.append(u)
        result = utilisateurs.insert_many(users)
        ids = result.inserted_ids
        # Les 2 utilisateurs se suivent mutuellement
        if len(ids) == 2:
            utilisateurs.update_one({"_id": ids[0]}, {"$set": {"following": [ids[1]]}})
            utilisateurs.update_one({"_id": ids[1]}, {"$set": {"following": [ids[0]]}})
            utilisateurs.update_one({"_id": ids[0]}, {"$set": {"followers": [ids[1]]}})
            utilisateurs.update_one({"_id": ids[1]}, {"$set": {"followers": [ids[0]]}})
        contenu_exemples = [
            "Belle récolte ce matin ! Les pluies ont été généreuses cette saison. 🌧️",
            "Nouveau système d'irrigation installé. Économie d'eau remarquable !",
            "Qui connaît un bon fournisseur de semences certifiées à Kaolack ?",
            "Marché de Thiès demain matin. J'amène 200 kg d'arachides fraîches.",
            "Mon troupeau de moutons se porte à merveille après la vaccination. 🐑",
            "Technique de compostage naturel partagée par un voisin — révolutionnaire !",
            "Alerte météo : risque de sécheresse à Diourbel. Préparez vos réserves d'eau.",
            "Premier partenariat avec un exportateur européen. Très fier ! 🌍",
            "Conseil : associez le niébé avec le sorgho pour enrichir votre sol.",
            "Rendement x3 pour mes serres tomates cette année ! 🍅",
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

        # Créer les communautés
        comms = [
            {"nom":"Irrigateurs du Sahel","description":"Techniques d'irrigation adaptées au climat sahélien.","emoji":"💧","membres":[],"tags":["irrigation"]},
            {"nom":"Éleveurs Sénégalais","description":"Communauté des éleveurs de bovins, ovins et caprins.","emoji":"🐄","membres":[],"tags":["élevage"]},
            {"nom":"Marché Agro Export","description":"Connexion entre producteurs et marchés internationaux.","emoji":"🌍","membres":[],"tags":["exportation"]},
            {"nom":"Agriculture Bio","description":"Pratiques agroécologiques et agriculture durable.","emoji":"🌿","membres":[],"tags":["bio"]},
        ]
        communautes.insert_many(comms)

        # Créer les produits du marché
        all_users = list(utilisateurs.find())
        produits_data = [
            {"nom":"Tomates fraîches", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 500, "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop", "description": "Tomates rouges juteuses directement du champ", "stock": 50, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now()},
            {"nom":"Oignons blancs", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Légumes", "prix": 300, "image": "https://images.unsplash.com/photo-1629451034900-d9a1e6fa7a5c?w=400&h=300&fit=crop", "description": "Oignons blancs de qualité supérieure", "stock": 75, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now()},
            {"nom":"Carottes orange", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 400, "image": "https://images.unsplash.com/photo-1584588694380-4d71bcdd2160?w=400&h=300&fit=crop", "description": "Carottes fraîches pleines de vitamines", "stock": 60, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now()},
            {"nom":"Pastèques sucrées", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Fruits", "prix": 2000, "image": "https://images.unsplash.com/photo-1590981268773-a7bb4f61c8e3?w=400&h=300&fit=crop", "description": "Pastèques juteuses et sucrées", "stock": 20, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now()},
            {"nom":"Mangues Ataulfo", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Fruits", "prix": 1500, "image": "https://images.unsplash.com/photo-1585518419759-37f4ea6a66e3?w=400&h=300&fit=crop", "description": "Mangues de saison au goût exceptionnel", "stock": 35, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now()},
            {"nom":"Papayes", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Fruits", "prix": 1200, "image": "https://images.unsplash.com/photo-1590080876004-13a4fcf22d4e?w=400&h=300&fit=crop", "description": "Papayes jaunes bien mûres", "stock": 40, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now()},
            {"nom":"Laitue fraîche", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Légumes", "prix": 350, "image": "https://images.unsplash.com/photo-1516895921230-8ac86ef6e7b0?w=400&h=300&fit=crop", "description": "Laitue verte tendre", "stock": 80, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now()},
            {"nom":"Poivrons rouges", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Légumes", "prix": 600, "image": "https://images.unsplash.com/photo-1599599811035-8dd37388c328?w=400&h=300&fit=crop", "description": "Poivrons rouges juteux et savoureux", "stock": 45, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now()},
            {"nom":"Agrumes mélangés", "vendeur_id": all_users[0]["_id"], "vendeur_pseudo": all_users[0]["pseudo"], "vendeur_avatar": all_users[0]["avatar"], "categorie": "Fruits", "prix": 1800, "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=300&fit=crop", "description": "Oranges, citrons, pamplemousses frais", "stock": 100, "disponible": True, "region": all_users[0]["region"], "date_ajout": datetime.now()},
            {"nom":"Aubergines", "vendeur_id": all_users[1]["_id"], "vendeur_pseudo": all_users[1]["pseudo"], "vendeur_avatar": all_users[1]["avatar"], "categorie": "Légumes", "prix": 550, "image": "https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400&h=300&fit=crop", "description": "Aubergines violettes de qualité", "stock": 55, "disponible": True, "region": all_users[1]["region"], "date_ajout": datetime.now()},
        ]
        produits.insert_many(produits_data)

init_db()

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("home"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        pseudo = request.form.get("pseudo","").strip()
        password = request.form.get("password","").strip()
        u = utilisateurs.find_one({"pseudo": pseudo})
        if u and check_password_hash(u.get("password_hash",""), password):
            session["user_id"] = str(u["_id"])
            session["pseudo"] = u["pseudo"]
            session["role"] = u.get("role","user")
            return redirect(url_for("home"))
        return render_template("login.html", error="Pseudo ou mot de passe incorrect.")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        pseudo = request.form.get("pseudo","").strip()
        nom = request.form.get("nom","").strip()
        password = request.form.get("password","").strip()
        password_confirm = request.form.get("password_confirm","").strip()
        region = request.form.get("region","Dakar")
        type_culture = request.form.get("type_culture","Mil")
        
        # Validations
        if not pseudo or not nom or not password:
            return render_template("register.html", error="Tous les champs sont requis.")
        
        if len(pseudo) < 3:
            return render_template("register.html", error="Le pseudo doit avoir au moins 3 caractères.")
        
        if len(password) < 6:
            return render_template("register.html", error="Le mot de passe doit avoir au moins 6 caractères.")
        
        if password != password_confirm:
            return render_template("register.html", error="Les mots de passe ne correspondent pas.")
        
        # Vérifier que le pseudo n'existe pas
        if utilisateurs.find_one({"pseudo": pseudo}):
            return render_template("register.html", error="Ce pseudo est déjà utilisé. Choisissez un autre.")
        
        # Créer le nouvel utilisateur
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
            "role": "user"
        }
        
        result = utilisateurs.insert_one(new_user)
        
        # Auto-login
        session["user_id"] = str(result.inserted_id)
        session["pseudo"] = pseudo
        session["role"] = "user"
        
        return redirect(url_for("home"))
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    is_admin = me.get("role") == "admin"
    return render_template("home.html", me=serialize(me), is_admin=is_admin)

# ===== API UTILISATEURS =====
@app.route("/api/utilisateurs")
def api_utilisateurs():
    users = list(utilisateurs.find())
    result = []
    for u in users:
        result.append({
            "_id": str(u["_id"]),
            "pseudo": u["pseudo"],
            "nom": u["nom"],
            "region": u["region"],
            "type_culture": u["type_culture"],
            "avatar": u["avatar"],
            "bio": u.get("bio",""),
            "nb_followers": len(u.get("followers",[])),
            "nb_following": len(u.get("following",[]))
        })
    return jsonify(result)

@app.route("/api/me")
@login_required
def api_me():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    if not me:
        return jsonify({"error": "Utilisateur introuvable"}), 401
    return jsonify({
        "_id": str(me["_id"]),
        "pseudo": me["pseudo"],
        "nom": me["nom"],
        "region": me["region"],
        "type_culture": me["type_culture"],
        "avatar": me["avatar"],
        "bio": me.get("bio",""),
        "cover_color": me.get("cover_color","#2d6a4f"),
        "nb_followers": len(me.get("followers",[])),
        "nb_following": len(me.get("following",[])),
        "role": me.get("role","user")
    })

@app.route("/api/profil/<user_id>")
def api_profil(user_id):
    u = utilisateurs.find_one({"_id": ObjectId(user_id)})
    if not u:
        return jsonify({"error": "Introuvable"}), 404
    me_id = session.get("user_id")
    is_following = False
    if me_id:
        me = utilisateurs.find_one({"_id": ObjectId(me_id)})
        if me:
            is_following = ObjectId(user_id) in me.get("following",[])
    return jsonify({
        "_id": str(u["_id"]),
        "pseudo": u["pseudo"],
        "nom": u["nom"],
        "region": u["region"],
        "type_culture": u["type_culture"],
        "avatar": u["avatar"],
        "bio": u.get("bio",""),
        "cover_color": u.get("cover_color","#2d6a4f"),
        "nb_followers": len(u.get("followers",[])),
        "nb_following": len(u.get("following",[])),
        "is_following": is_following
    })

@app.route("/api/abonner/<user_id>", methods=["POST"])
def api_abonner(user_id):
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    me_id = ObjectId(session["user_id"])
    target_id = ObjectId(user_id)
    me = utilisateurs.find_one({"_id": me_id})
    if target_id in me.get("following",[]):
        utilisateurs.update_one({"_id": me_id}, {"$pull": {"following": target_id}})
        utilisateurs.update_one({"_id": target_id}, {"$pull": {"followers": me_id}})
        following = False
    else:
        utilisateurs.update_one({"_id": me_id}, {"$push": {"following": target_id}})
        utilisateurs.update_one({"_id": target_id}, {"$push": {"followers": me_id}})
        following = True
    target = utilisateurs.find_one({"_id": target_id})
    return jsonify({"following": following, "nb_followers": len(target.get("followers",[]))})

# ===== API PUBLICATIONS =====
@app.route("/api/feed")
def api_feed():
    tag = request.args.get("tag")
    user_filter = request.args.get("user_id")
    query = {}
    if tag:
        query["tags"] = tag
    if user_filter:
        query["auteur_id"] = ObjectId(user_filter)
    pubs = list(publications.find(query).sort("date", -1).limit(30))
    user_id = session.get("user_id")
    result = []
    for p in pubs:
        p["_id"] = str(p["_id"])
        p["auteur_id"] = str(p["auteur_id"])
        p["date"] = p["date"].strftime("%d/%m/%Y %H:%M") if p.get("date") else ""
        p["nb_likes"] = len(p.get("likes",[]))
        p["liked_by_me"] = ObjectId(user_id) in p.get("likes",[]) if user_id else False
        p["likes"] = [str(x) for x in p.get("likes",[])]
        for c in p.get("commentaires",[]):
            c["_id"] = str(c.get("_id",""))
            c["auteur_id"] = str(c.get("auteur_id",""))
            c["date"] = c["date"].strftime("%d/%m/%Y %H:%M") if c.get("date") else ""
        result.append(p)
    return jsonify(result)

@app.route("/api/publier", methods=["POST"])
def api_publier():
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    data = request.get_json()
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    tags = [t.strip().lower() for t in data.get("tags","").split(",") if t.strip()]
    pub = {
        "auteur_id": me["_id"],
        "auteur_pseudo": me["pseudo"],
        "auteur_avatar": me["avatar"],
        "contenu": data.get("contenu",""),
        "tags": tags,
        "likes": [],
        "commentaires": [],
        "date": datetime.now()
    }
    r = publications.insert_one(pub)
    return jsonify({"ok": True, "id": str(r.inserted_id)})

@app.route("/api/like/<pub_id>", methods=["POST"])
def api_like(pub_id):
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    uid = ObjectId(session["user_id"])
    pub = publications.find_one({"_id": ObjectId(pub_id)})
    if uid in pub.get("likes",[]):
        publications.update_one({"_id": ObjectId(pub_id)}, {"$pull": {"likes": uid}})
        liked = False
    else:
        publications.update_one({"_id": ObjectId(pub_id)}, {"$push": {"likes": uid}})
        liked = True
    nb = publications.find_one({"_id": ObjectId(pub_id)})
    return jsonify({"liked": liked, "nb_likes": len(nb.get("likes",[]))})

@app.route("/api/commenter/<pub_id>", methods=["POST"])
def api_commenter(pub_id):
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    data = request.get_json()
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    comment = {
        "_id": ObjectId(),
        "auteur_id": me["_id"],
        "auteur_pseudo": me["pseudo"],
        "auteur_avatar": me["avatar"],
        "texte": data.get("texte",""),
        "date": datetime.now()
    }
    publications.update_one({"_id": ObjectId(pub_id)}, {"$push": {"commentaires": comment}})
    return jsonify({"ok": True, "pseudo": me["pseudo"], "avatar": me["avatar"], "texte": comment["texte"]})

@app.route("/api/top3")
def api_top3():
    pubs = list(publications.find())
    pubs.sort(key=lambda x: len(x.get("likes",[])), reverse=True)
    result = []
    for p in pubs[:3]:
        result.append({
            "_id": str(p["_id"]),
            "auteur_pseudo": p["auteur_pseudo"],
            "auteur_avatar": p["auteur_avatar"],
            "contenu": p["contenu"][:80] + "...",
            "nb_likes": len(p.get("likes",[]))
        })
    return jsonify(result)

# ===== API COMMUNAUTES =====
@app.route("/api/communautes")
def api_communautes():
    comms = list(communautes.find())
    user_id = session.get("user_id")
    result = []
    for c in comms:
        is_member = ObjectId(user_id) in c.get("membres",[]) if user_id else False
        result.append({
            "_id": str(c["_id"]),
            "nom": c["nom"],
            "description": c["description"],
            "emoji": c["emoji"],
            "nb_membres": len(c.get("membres",[])),
            "tags": c.get("tags",[]),
            "is_member": is_member
        })
    return jsonify(result)

@app.route("/api/rejoindre/<comm_id>", methods=["POST"])
def api_rejoindre(comm_id):
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    uid = ObjectId(session["user_id"])
    c = communautes.find_one({"_id": ObjectId(comm_id)})
    if uid in c.get("membres",[]):
        communautes.update_one({"_id": ObjectId(comm_id)}, {"$pull": {"membres": uid}})
        joined = False
    else:
        communautes.update_one({"_id": ObjectId(comm_id)}, {"$push": {"membres": uid}})
        joined = True
    c2 = communautes.find_one({"_id": ObjectId(comm_id)})
    return jsonify({"joined": joined, "nb_membres": len(c2.get("membres",[]))})

@app.route("/api/creer_communaute", methods=["POST"])
def api_creer_communaute():
    if "user_id" not in session:
        return jsonify({"error": "Non connecté"}), 401
    data = request.get_json()
    c = {
        "nom": data.get("nom",""),
        "description": data.get("description",""),
        "emoji": data.get("emoji","🌱"),
        "membres": [ObjectId(session["user_id"])],
        "tags": [t.strip() for t in data.get("tags","").split(",") if t.strip()],
        "createur_id": ObjectId(session["user_id"])
    }
    r = communautes.insert_one(c)
    return jsonify({"ok": True, "id": str(r.inserted_id)})

# ===== ROUTES ADMIN =====
@app.route("/admin")
@admin_required
def admin_panel():
    total_users = utilisateurs.count_documents({})
    total_pubs = publications.count_documents({})
    total_comms = communautes.count_documents({})
    return render_template("admin.html", total_users=total_users, total_pubs=total_pubs, total_comms=total_comms)

@app.route("/api/admin/utilisateurs", methods=["GET"])
@admin_required
def api_admin_utilisateurs():
    users = list(utilisateurs.find())
    result = []
    for u in users:
        result.append({
            "_id": str(u["_id"]),
            "pseudo": u["pseudo"],
            "nom": u["nom"],
            "region": u["region"],
            "role": u.get("role","user"),
            "nb_followers": len(u.get("followers",[])),
            "date_inscription": u["date_inscription"].strftime("%d/%m/%Y")
        })
    return jsonify(result)

@app.route("/api/admin/utilisateur/<user_id>/role", methods=["POST"])
@admin_required
def api_admin_change_role(user_id):
    data = request.get_json()
    new_role = data.get("role","user")
    if new_role not in ["admin","user"]:
        return jsonify({"error": "Rôle invalide"}), 400
    utilisateurs.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": new_role}})
    return jsonify({"ok": True, "message": f"Utilisateur passe en {new_role}"})

@app.route("/api/admin/utilisateur/<user_id>/delete", methods=["POST"])
@admin_required
def api_admin_delete_user(user_id):
    utilisateurs.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"ok": True, "message": "Utilisateur supprimé"})

@app.route("/api/admin/stats")
@admin_required
def api_admin_stats():
    total_users = utilisateurs.count_documents({})
    total_pubs = publications.count_documents({})
    total_comms = communautes.count_documents({})
    admins = utilisateurs.count_documents({"role": "admin"})
    return jsonify({
        "total_users": total_users,
        "total_admins": admins,
        "total_publications": total_pubs,
        "total_communautes": total_comms
    })

# ===== ROUTES MARCHE =====
@app.route("/marche")
@login_required
def marche():
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    return render_template("marche.html", me=serialize(me))

@app.route("/api/produits")
def api_produits():
    categorie = request.args.get("categorie")
    query = {}
    if categorie and categorie != "Tous":
        query["categorie"] = categorie
    query["disponible"] = True
    query["stock"] = {"$gt": 0}
    prods = list(produits.find(query).sort("date_ajout", -1))
    result = []
    for p in prods:
        result.append({
            "_id": str(p["_id"]),
            "nom": p["nom"],
            "vendeur_id": str(p["vendeur_id"]),
            "vendeur_pseudo": p["vendeur_pseudo"],
            "vendeur_avatar": p["vendeur_avatar"],
            "categorie": p["categorie"],
            "prix": p["prix"],
            "image": p["image"],
            "description": p["description"],
            "stock": p["stock"],
            "region": p["region"],
            "disponible": p["disponible"]
        })
    return jsonify(result)

@app.route("/api/commander", methods=["POST"])
@login_required
def api_commander():
    data = request.get_json()
    produit_id = data.get("produit_id")
    quantite = data.get("quantite", 1)
    
    prod = produits.find_one({"_id": ObjectId(produit_id)})
    if not prod:
        return jsonify({"error": "Produit introuvable"}), 404
    if prod["stock"] < quantite:
        return jsonify({"error": "Stock insuffisant"}), 400
    
    me = utilisateurs.find_one({"_id": ObjectId(session["user_id"])})
    vendeur = utilisateurs.find_one({"_id": prod["vendeur_id"]})
    
    commande = {
        "acheteur_id": me["_id"],
        "acheteur_pseudo": me["pseudo"],
        "acheteur_avatar": me["avatar"],
        "vendeur_id": prod["vendeur_id"],
        "vendeur_pseudo": prod["vendeur_pseudo"],
        "produit_id": ObjectId(produit_id),
        "produit_nom": prod["nom"],
        "quantite": quantite,
        "prix_total": prod["prix"] * quantite,
        "prix_unitaire": prod["prix"],
        "date_commande": datetime.now(),
        "statut": "en attente"
    }
    
    r = commandes.insert_one(commande)
    
    # Diminuer le stock
    new_stock = prod["stock"] - quantite
    produits.update_one({"_id": ObjectId(produit_id)}, {
        "$set": {"stock": new_stock, "disponible": new_stock > 0}
    })
    
    # Créer une notification pour le vendeur
    notification = {
        "destinataire_id": prod["vendeur_id"],
        "type": "nouvelle_commande",
        "titre": f"Nouvelle commande de {me['pseudo']}",
        "message": f"{me['pseudo']} a commandé {quantite}x {prod['nom']}",
        "commande_id": r.inserted_id,
        "acheteur_pseudo": me["pseudo"],
        "acheteur_avatar": me["avatar"],
        "produit_nom": prod["nom"],
        "quantite": quantite,
        "prix_total": prod["prix"] * quantite,
        "date": datetime.now(),
        "lue": False
    }
    notifications.insert_one(notification)
    
    return jsonify({
        "ok": True,
        "commande_id": str(r.inserted_id),
        "message": f"Commande créée ! Le vendeur a été notifié."
    })

@app.route("/api/mes-commandes")
@login_required
def api_mes_commandes():
    user_id = ObjectId(session["user_id"])
    mes_cdes = list(commandes.find({"acheteur_id": user_id}).sort("date_commande", -1))
    result = []
    for c in mes_cdes:
        result.append({
            "_id": str(c["_id"]),
            "produit_nom": c["produit_nom"],
            "vendeur_pseudo": c["vendeur_pseudo"],
            "vendeur_avatar": c["vendeur_avatar"],
            "quantite": c["quantite"],
            "prix_unitaire": c["prix_unitaire"],
            "prix_total": c["prix_total"],
            "date": c["date_commande"].strftime("%d/%m/%Y %H:%M"),
            "statut": c["statut"]
        })
    return jsonify(result)

@app.route("/api/commandes-recues")
@login_required
def api_commandes_recues():
    user_id = ObjectId(session["user_id"])
    cdes_recues = list(commandes.find({"vendeur_id": user_id}).sort("date_commande", -1))
    result = []
    for c in cdes_recues:
        result.append({
            "_id": str(c["_id"]),
            "produit_nom": c["produit_nom"],
            "acheteur_pseudo": c["acheteur_pseudo"],
            "acheteur_avatar": c["acheteur_avatar"],
            "quantite": c["quantite"],
            "prix_unitaire": c["prix_unitaire"],
            "prix_total": c["prix_total"],
            "date": c["date_commande"].strftime("%d/%m/%Y %H:%M"),
            "statut": c["statut"]
        })
    return jsonify(result)

@app.route("/api/notifications")
@login_required
def api_notifications():
    user_id = ObjectId(session["user_id"])
    notifs = list(notifications.find({"destinataire_id": user_id}).sort("date", -1).limit(50))
    result = []
    for n in notifs:
        result.append({
            "_id": str(n["_id"]),
            "type": n["type"],
            "titre": n["titre"],
            "message": n["message"],
            "acheteur_pseudo": n.get("acheteur_pseudo", ""),
            "acheteur_avatar": n.get("acheteur_avatar", ""),
            "produit_nom": n.get("produit_nom", ""),
            "quantite": n.get("quantite", 0),
            "prix_total": n.get("prix_total", 0),
            "date": n["date"].strftime("%d/%m/%Y %H:%M"),
            "lue": n["lue"]
        })
    return jsonify(result)

@app.route("/api/notification/<notif_id>/lire", methods=["POST"])
@login_required
def api_marquer_notif_lue(notif_id):
    notifications.update_one({"_id": ObjectId(notif_id)}, {"$set": {"lue": True}})
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
