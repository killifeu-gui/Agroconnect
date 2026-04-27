# 🚀 Guide de Déploiement AgroConnect sur Render

## Phase 1: Préparer MongoDB Atlas (Base de données cloud)

1. Accédez à https://www.mongodb.com/cloud/atlas
2. Créez un compte gratuit
3. Créez un cluster gratuit "M0"
4. Allez dans "Database Access" et créez un utilisateur:
   - Username: `agroconnect_user`
   - Password: Générez un mot de passe fort
5. Allez dans "Network Access" et ajoutez `0.0.0.0/0` (Allow from anywhere)
6. Cliquez sur "Connect" et copiez la chaîne de connexion:
   ```
   mongodb+srv://agroconnect_user:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Phase 2: Préparer GitHub

1. Créez un compte à https://github.com
2. Créez un nouveau repository:
   - Name: `agroconnect`
   - Description: "Agricultural marketplace for Senegal"
   - Public (visible à tous)
   - Init with README

3. Dans votre terminal local:
   ```bash
   cd c:\RONDOMNUMBER9\SD\agroconnect
   git init
   git add .
   git commit -m "Initial commit - AgroConnect v1.0"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/agroconnect.git
   git push -u origin main
   ```

## Phase 3: Créer un compte Render

1. Accédez à https://render.com
2. Créez un compte (Sign up with GitHub pour faciliter)
3. Connectez votre compte GitHub

## Phase 4: Déployer sur Render

1. Sur le dashboard Render, cliquez "New +" → "Web Service"
2. Sélectionnez votre repo `agroconnect`
3. Configurez:
   - **Name**: agroconnect
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (gratuit!)

4. Cliquez "Create Web Service"

## Phase 5: Configurer les variables d'environnement

Sur la page du service Render:

1. Allez à l'onglet "Environment"
2. Ajoutez les variables:
   ```
   MONGO_URI = mongodb+srv://agroconnect_user:PASSWORD@cluster0.xxxxx.mongodb.net/agroconnect?retryWrites=true&w=majority
   SECRET_KEY = votre_clé_secrète_complexe_ici
   FLASK_ENV = production
   ```

3. Sauvegardez

## Phase 6: Vérifier le déploiement

1. Attendez 2-3 minutes (Render construit et déploie)
2. Vous verrez un lien comme: `https://agroconnect-xxxx.onrender.com`
3. Accédez à ce lien
4. Testez la connexion avec les comptes:
   - Pseudo/Nom: **babacar_agro** / **Babacar Cisse**
   - Mot de passe: **agroconnect2024**

## Phase 7: Faire des modifications après déploiement

Après le déploiement, tu peux toujours modifier le code:

```bash
# 1. Modifie le code localement
# (ex: change les images, ajoute des produits, etc.)

# 2. Commit et push
git add .
git commit -m "Description du changement"
git push

# 3. Render va auto-redéployer en 1-2 minutes
# Regarde les logs dans Render dashboard
```

## 📊 Tableau des commandes Git

| Commande | Fonction |
|----------|----------|
| `git status` | Voir les fichiers modifiés |
| `git add .` | Ajouter tous les changements |
| `git commit -m "message"` | Valider les changements |
| `git push` | Envoyer sur GitHub |
| `git pull` | Récupérer les changements |

## 🔒 Sécurité

Ne JAMAIS commit:
- `.env` (utilise `.env.example` à la place)
- `__pycache__/`
- `.venv/`
- `node_modules/` (si applicable)

Le `.gitignore` s'en charge déjà.

## 💰 Coûts

- **Render**: Gratuit (tier free)
- **MongoDB Atlas**: Gratuit (512 MB données)
- **Total**: **0€** ✅

## 🆘 Troubleshooting

### L'app ne démarre pas
- Vérifiez les logs dans Render → "Logs"
- Vérifiez que `MONGO_URI` est correct

### Les images ne s'affichent pas
- Les URLs Pixabay doivent être accessibles
- Si bloques, utilisez des URLs d'autres sources

### La base de données est vide
- Render redéploie et relance `init_db()`
- Les données test seront créées automatiquement

## 📞 Support

En cas de problème:
1. Vérifiez les logs Render
2. Testez localement avec `python app.py`
3. Comparez avec ce guide
