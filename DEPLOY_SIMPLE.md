# 🎯 Déploiement Express AgroConnect (30 minutes)

## ✅ AVANT DE DÉPLOYER - Vérifier localement

```bash
# 1. Arrête le serveur (Ctrl+C)

# 2. Redémarre et teste
python app.py

# 3. Accède à http://127.0.0.1:5000/login
# 4. Essaie de te connecter:
#    Pseudo: babacar_agro
#    Mot de passe: agroconnect2024
# 5. Vérifie le Marché → Les images s'affichent?

# Si OK → Ferme le serveur (Ctrl+C)
```

---

## 🔧 ÉTAPE 1: Initialiser Git et GitHub (5 min)

### A. Terminal - Initialise le repo local:

```bash
cd c:\RONDOMNUMBER9\SD\agroconnect

# Vérifie que git est initialisé
git status

# Si erreur "not a git repository":
git init

# Ajoute tous les fichiers
git add .

# Crée le premier commit
git commit -m "AgroConnect v1.0 - Initial deployment"
```

### B. GitHub - Crée le repo:

1. Va à https://github.com/new
2. Remplis:
   - **Repository name**: `agroconnect`
   - **Description**: "Plateforme agricole du Sénégal"
   - Sélectionne: **Public**
   - Clique: **Create repository**

3. Copie l'URL du repo (ex: `https://github.com/tonusername/agroconnect.git`)

### C. Terminal - Connecte GitHub:

```bash
# Remplace par ton URL GitHub
git remote add origin https://github.com/tonusername/agroconnect.git

# Push le code
git branch -M main
git push -u origin main

# Confirmé? Ton code est maintenant sur GitHub!
```

---

## 🚀 ÉTAPE 2: Configurer MongoDB Atlas (10 min)

1. Va à https://www.mongodb.com/cloud/atlas
2. Clique **Sign Up** (avec email)
3. Crée un cluster:
   - Clique **Build a Database**
   - Choisir **M0 (Free Forever)**
   - Region: **Europe (Ireland)**
   - Clique **Create**

4. **Database Access**:
   - Clique **Add New Database User**
   - Username: `agroconnect_user`
   - Password: Génère un mot de passe (ex: `Agroconnect2024!Secure`)
   - Clique **Create Database User**

5. **Network Access**:
   - Clique **Add IP Address**
   - Sélectionne **Allow Access from Anywhere** (0.0.0.0/0)
   - Clique **Confirm**

6. **Connection String**:
   - Clique **Connect** (le bouton vert)
   - Choisir **Drivers**
   - Copie la chaîne de connexion:
   ```
   mongodb+srv://agroconnect_user:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   - **REMPLACE** `PASSWORD` par ton mot de passe exact

---

## 🌐 ÉTAPE 3: Déployer sur Render (10 min)

1. Va à https://render.com
2. Clique **Sign Up** → **Connect with GitHub** (rapide!)
3. Autorise Render à accéder à GitHub
4. Sur le dashboard Render:
   - Clique **+ New** → **Web Service**
   - Sélectionne ton repo `agroconnect`
   - Clique **Connect**

5. **Configure**:
   - **Name**: `agroconnect`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free** (gratuit)

6. **Environment Variables** (IMPORTANT):
   - Clique **Advanced** → **Add Environment Variable**
   - Ajoute deux variables:

   **Variable 1:**
   - Key: `MONGO_URI`
   - Value: `mongodb+srv://agroconnect_user:TONMOTDEPASSE@cluster0.xxxxx.mongodb.net/agroconnect?retryWrites=true&w=majority`
   - (Remplace `TONMOTDEPASSE` et le cluster)

   **Variable 2:**
   - Key: `SECRET_KEY`
   - Value: `agroconnect_production_secret_2024_render`

7. Clique **Create Web Service**

8. **Attends** 3-5 minutes (Render construit)
9. Tu verras une URL comme: `https://agroconnect-xxxx.onrender.com`

---

## ✅ ÉTAPE 4: Tester en ligne

1. Accède à ton URL Render (ex: `https://agroconnect-xxxx.onrender.com`)
2. Connecte-toi:
   - **Pseudo**: `babacar_agro`
   - **Mot de passe**: `agroconnect2024`
3. Visite le Marché → Les images s'affichent?
4. **SUCCÈS** 🎉

---

## 📝 ÉTAPES FUTURES (Modifications)

Après le déploiement, tu peux modifier le code à tout moment:

```bash
# 1. Change ce que tu veux dans le code local
# (ex: app.py, templates, etc.)

# 2. Enregistre et commit
git add .
git commit -m "Description du changement"

# 3. Push sur GitHub
git push

# 4. Render va redéployer AUTOMATIQUEMENT en 1-2 minutes
# Tu n'as rien à faire d'autre!
```

Exemple:
- Tu veux ajouter un produit? Modifie `app.py`, puis `git push`
- Tu veux changer le design? Modifie `templates/`, puis `git push`
- Render s'en charge! ✨

---

## 📊 Récapitulatif

| Étape | Plateforme | Temps | Coût |
|-------|-----------|-------|------|
| 1. Git + GitHub | GitHub | 5 min | **0€** |
| 2. MongoDB Atlas | MongoDB | 10 min | **0€** |
| 3. Déployer | Render | 10 min | **0€** |
| **TOTAL** | | **25 min** | **0€** ✅ |

---

## 🆘 Problèmes courants

### "MONGO_URI not set" ou erreur database
- Vérifiez que la variable d'environnement est correcte dans Render
- Regarde les logs: Render dashboard → Logs

### "Bad Gateway" ou "Application Error"
- Attends 5 minutes (construction en cours)
- Rafraîchis la page

### Les images ne s'affichent pas
- Les URLs Pixabay sont valides? Teste-les dans un onglet
- Regarde la console (F12) pour voir les erreurs

---

## 🎓 Commandes Git importantes

```bash
# Voir les fichiers modifiés
git status

# Ajouter tous les changements
git add .

# Valider les changements
git commit -m "Description courte"

# Envoyer sur GitHub
git push

# Récupérer les changements du serveur
git pull
```

---

**Tu es prêt(e)? Commence par l'ÉTAPE 1!** 🚀
