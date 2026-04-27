# 🚀 AGROCONNECT - DÉPLOIEMENT IMMÉDIAT

## Option 1: Déployer sur RENDER (RECOMMANDÉ - 5-10 minutes)

### Étape 1: Créer compte MongoDB Atlas (gratuit)
1. Aller à: https://www.mongodb.com/cloud/atlas/register
2. S'inscrire avec email
3. Créer un cluster **M0 (gratuit)**
4. Copier la **connection string** (format: `mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/agroconnect?retryWrites=true&w=majority`)

### Étape 2: Créer application sur Render
1. Aller à: https://dashboard.render.com/
2. Cliquer **"New +"** → **"Web Service"**
3. Connecter GitHub: https://github.com/killifeu-gui/Agroconnect
4. Sélectionner le dépôt **Agroconnect**

### Étape 3: Configurer Render
- **Name**: `agroconnect`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
- **Instance Type**: `Free`

### Étape 4: Ajouter variable d'environnement
- Cliquer **"Environment"**
- Ajouter variable:
  - **Key**: `MONGO_URI`
  - **Value**: *(Votre MongoDB Atlas connection string)*

### Étape 5: Déployer
- Cliquer **"Deploy"**
- Attendre 2-3 minutes
- **Votre URL**: `https://agroconnect-xxxxx.onrender.com`

---

## Option 2: Déployer sur HEROKU (Alternative)

### Étape 1: Créer compte Heroku
1. Aller à: https://signup.heroku.com/
2. S'inscrire gratuitement

### Étape 2: Installer Heroku CLI
- Windows: https://devcenter.heroku.com/articles/heroku-cli
- Ou via Chocolatey: `choco install heroku-cli`

### Étape 3: Déployer
```bash
cd c:\RONDOMNUMBER9\SD\agroconnect
heroku login
heroku create agroconnect
git push heroku main
```

---

## Option 3: Déployer en LOCAL (Test rapide)

### Étape 1: Installer MongoDB Local
- Télécharger: https://www.mongodb.com/try/download/community
- Installer et lancer le service

### Étape 2: Lancer l'app
```bash
cd c:\RONDOMNUMBER9\SD\agroconnect
python -m pip install -r requirements.txt
python app.py
```

### Étape 3: Accéder
- URL: `http://127.0.0.1:5000`
- **Login**: 
  - Username: `babacar_agro`
  - Password: `agroconnect2024`

### Étape 4: Rendre PUBLIC (ngrok)
```bash
pip install pyngrok
python
>>> from pyngrok import ngrok
>>> ngrok.connect(5000)
# Copier l'URL publique
```

---

## 🎯 Identifiants de TEST

```
Compte Admin:
- Username: babacar_agro
- Password: agroconnect2024
- Rôle: Admin

Compte Utilisateur:
- Username: aissatou_farmers
- Password: agroconnect2024
- Rôle: User
```

---

## 📊 Produits disponibles (13)

### Légumes (500-600 FCFA):
- Tomates fraîches (500)
- Oignons blancs (300)
- Carottes orange (400)
- Poivrons rouges (600)
- Aubergines violettes (550)
- Laitue fraîche (350)
- Piments verts (400)

### Fruits (700-2000 FCFA):
- Pastèques sucrées (2000)
- Mangues Ataulfo (1500)
- Papayes jaunes (1200)
- Agrumes mélangés (1800)
- Bananes plantain (700)
- Goyaves roses (900)

---

## ❓ Support

Si vous avez besoin d'aide:
1. Vérifier les **logs** sur le platform (Render/Heroku)
2. Confirmer MongoDB Atlas est **actif**
3. Vérifier les **variables d'environnement**
4. Vérifier l'**URL de connection** MongoDB

---

## 📝 Notes

- La version **RENDER** est la plus simple (gratuite, pas de crédit requis)
- Les images sont **SVG inline** (100% fiable, pas de serveur d'images)
- L'app supporte **Mobile** et **Desktop**
- Tous les prix sont en **FCFA** (Franc CFA)
