# 🌾 AgroConnect - Plateforme Agricole Sénégalaise

![AgroConnect Logo](https://via.placeholder.com/300x100?text=AgroConnect)

Une plateforme web complète pour connecter les agriculteurs sénégalais, faciliter le commerce de produits agricoles, et créer une communauté.

## ✨ Caractéristiques Principales

### 👥 Pour les Utilisateurs Réguliers
- 🔐 **Authentification sécurisée** : Login/Register avec hash de mots de passe
- 🛒 **Marché agricole** : Parcourir produits (légumes/fruits) filtrés par catégorie, prix, région
- ⭐ **Avis produits** : Laisser des notes et commentaires (1-5 étoiles)
- 📦 **Gestion commandes** : Historique d'achats et suivi
- 👨‍🌾 **Profils vendeurs** : Voir les détails des vendeurs, leurs produits, les avis
- 🔔 **Notifications** : Alertes pour new commandes, messages
- ❤️ **Follow vendeurs** : Suivre vos vendeurs préférés
- 🏠 **Feed social** : Publications, tags, partage d'expériences

### 🛡️ Pour les Administrateurs
- 📊 **Dashboard complet** : Stats utilisateurs, produits, commandes, publications
- 👥 **Gestion utilisateurs** : Promouvoir/rétrograder en admin, bloquer, supprimer
- 📈 **Analytics** : Produits top-vendus, tendances marché
- 🗑️ **Modération** : Gérer contenu, avis, publications
- ⚙️ **Configuration système** : Régions, types de cultures, catégories

## 🚀 Quick Start (Développement)

### Prérequis
- Python 3.11+
- MongoDB (running sur localhost:27017)
- pip / virtualenv

### Installation

```bash
# Cloner le repo
git clone https://github.com/username/agroconnect.git
cd agroconnect

# Créer virtualenv
python3 -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt

# Lancer l'app
python3 app.py
```

Accéder à : **http://localhost:5000/login**

### Comptes Test
| Pseudo | Mot de passe | Rôle |
|--------|------------|------|
| `babacar_agro` | `agroconnect2024` | Admin |
| `aissatou_farmers` | `agroconnect2024` | Admin |

## 📁 Structure du Projet

```
agroconnect/
├── app.py                      # App Flask principale
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Docker image
├── Procfile                    # Config Heroku/Render
├── agroconnect.service         # Systemd service (VPS)
├── nginx-agroconnect.conf     # Config Nginx (VPS)
├── .env.example               # Template variables d'environnement
├── DEPLOYMENT_GUIDE.md        # Guide complet de déploiement
├── templates/
│   ├── login.html            # Page de connexion
│   ├── register.html         # Page d'inscription
│   ├── home.html             # Feed principal
│   ├── marche.html           # Marketplace
│   ├── vendeur_profile.html  # Profil vendeur
│   └── admin.html            # Dashboard admin
├── static/
│   ├── css/                  # Styles
│   └── js/                   # Scripts frontend
├── db.py                     # (Ancien - utilise app.py maintenant)
├── interface.py              # (Ancien)
└── main.py                   # (Ancien)
```

## 🔌 API Endpoints

### Auth
- `POST /login` - Connexion
- `POST /register` - Inscription
- `GET /logout` - Déconnexion

### Marché
- `GET /api/produits` - Lister produits (avec filtres)
- `POST /api/commander` - Placer une commande
- `GET /api/mes-commandes` - Historique achats
- `GET /api/commandes-recues` - Ventes reçues

### Avis
- `GET /api/produit/<id>/avis` - Lister avis d'un produit
- `POST /api/avis/creer` - Créer un avis

### Utilisateurs
- `GET /vendeur/<pseudo>` - Profil public vendeur
- `POST /api/utilisateur/<id>/follow` - Suivre
- `POST /api/utilisateur/<id>/unfollow` - Ne plus suivre

### Admin
- `GET /admin` - Dashboard admin
- `GET /api/admin/utilisateurs` - Lister tous utilisateurs
- `POST /api/admin/utilisateur/<id>/role` - Toggle role
- `POST /api/admin/utilisateur/<id>/delete` - Supprimer utilisateur
- `POST /api/admin/utilisateur/<id>/block` - Bloquer utilisateur

## 🗄️ Schéma Base de Données

### Collections MongoDB

**utilisateurs**
```javascript
{
  _id: ObjectId,
  pseudo: String,
  nom: String,
  email: String,
  password_hash: String,
  role: "user" | "admin",
  region: String,
  type_culture: String,
  bio: String,
  avatar: String,
  followers: [ObjectId],
  following: [ObjectId],
  blocked: Boolean,
  verified: Boolean,
  date_inscription: Date,
  cover_color: String
}
```

**produits**
```javascript
{
  _id: ObjectId,
  nom: String,
  categorie: "Légumes" | "Fruits",
  prix: Number,
  image: String,
  description: String,
  stock: Number,
  disponible: Boolean,
  vendeur_id: ObjectId,
  vendeur_pseudo: String,
  vendeur_avatar: String,
  region: String,
  note_moyenne: Number,
  nb_avis: Number,
  date_ajout: Date
}
```

**avis**
```javascript
{
  _id: ObjectId,
  produit_id: ObjectId,
  auteur_id: ObjectId,
  auteur_pseudo: String,
  note: Number (1-5),
  commentaire: String,
  date: Date,
  modere: Boolean
}
```

**commandes**
```javascript
{
  _id: ObjectId,
  acheteur_id: ObjectId,
  vendeur_id: ObjectId,
  produit_id: ObjectId,
  quantite: Number,
  prix_unitaire: Number,
  prix_total: Number,
  statut: String,
  date_commande: Date
}
```

## 🔐 Sécurité

- ✅ **Hashage mots de passe** : Werkzeug.security
- ✅ **Sessions Flask** : Protégées par SECRET_KEY
- ✅ **Decorateurs @login_required** : Protection routes
- ✅ **Decorateurs @admin_required** : Accès admin seulement
- ✅ **Validation input** : Côté serveur
- ✅ **HTTPS SSL** : Let's Encrypt (production)
- ✅ **CORS** : Configurable

### À améliorer
- [ ] Authentification 2FA
- [ ] Rate limiting API
- [ ] Protection CSRF tokens
- [ ] Audit logs
- [ ] Encryption données sensibles

## 📊 Améliorations v1.0 vs v0.5

| Fonctionnalité | v0.5 | v1.0 |
|---|---|---|
| Séparation Admin/User | ⚠️ Partielle | ✅ Complète |
| Avis produits | ❌ | ✅ |
| Profils vendeurs | ❌ | ✅ |
| Recherche avancée | ⚠️ Basique | ✅ Filtres avancés |
| Dashboard Admin | ⚠️ Simple | ✅ Complet |
| Gestion utilisateurs | ⚠️ Basique | ✅ Avancée |
| Variables d'env | ❌ | ✅ |
| Docker | ❌ | ✅ |
| Nginx config | ❌ | ✅ |
| SSL/HTTPS | ❌ | ✅ |
| Guides déploiement | ❌ | ✅ Complets |

## 🚀 Déploiement

### Option 1 : Render (Recommandé pour débuter)

Voir [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#option-a--déploiement-rapide-render)

```bash
# 5 minutes pour aller en production!
1. GitHub push
2. Connecter Render
3. Ajouter env vars
4. Deploy
```

### Option 2 : VPS Ubuntu + Nginx

Voir [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#option-b--vps-ubuntu-avec-nginx)

```bash
# Plus de contrôle, meilleure performance
# Étapes : provision VPS → clone repo → setup systemd → nginx → SSL
```

### Option 3 : Docker (n'importe où)

```bash
docker build -t agroconnect .
docker run -p 5000:5000 \
  -e MONGO_URI="mongodb://localhost:27017/" \
  -e SECRET_KEY="votre_cle" \
  agroconnect
```

## 📚 Documentation

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Guide complet déploiement
- [API.md](API.md) - Référence API détaillée *(À créer)*
- [SECURITY.md](SECURITY.md) - Best practices sécurité *(À créer)*

## 🛠️ Développement

### Ajouter une fonctionnalité

1. Créer une branch : `git checkout -b feature/ma-feature`
2. Modifier app.py et templates
3. Tester localement
4. Push et PR

### Stack technique

- **Backend** : Flask 3.0 (Python)
- **Database** : MongoDB 4.6
- **Frontend** : HTML/CSS/JS vanilla
- **Server** : Gunicorn + Nginx
- **Infrastructure** : Render / VPS Ubuntu
- **SSL** : Let's Encrypt Certbot

## 📞 Support

- **Issues** : GitHub Issues
- **Email** : dev@agroconnect.sn
- **Slack** : [Workspace AgroConnect](https://agroconnect.slack.com)

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE)

## 👨‍💻 Auteurs

- Killifeu GUI - Développeur Principal
- Babacar Cisse - Conseiller Agricole
- Aissatou Diagne - Test Lead

---

**Status** : ✅ Production Ready (v1.0)  
**Last Updated** : 25 avril 2026  
**Next Release** : v1.1 (Mobile app, gamification)
