# 🚀 GUIDE DE DÉPLOIEMENT RAPIDE - AgroConnect

Trois options simples pour mettre l'app en production.

---

## **OPTION 1 : Render (Recommandé - 5 min) ⭐**

### ✅ Avantages
- HTTPS automatique
- Pas de gestion serveur
- Déploiement via GitHub
- Gratuit pendant 1 mois

### 📋 Étapes

1. **Créer un repo GitHub**
   ```bash
   cd c:\RONDOMNUMBER9\SD\agroconnect
   git init
   git add .
   git commit -m "Initial: AgroConnect v1.0"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/agroconnect.git
   git push -u origin main
   ```

2. **S'inscrire sur [render.com](https://render.com)**
   - Cliquer "Sign up with GitHub"

3. **Créer un Web Service**
   - New → Web Service
   - Connecter repo `agroconnect`
   - Name: `agroconnect`
   - Environment: `Docker`
   - Laisser les autres par défaut

4. **Ajouter les variables d'environnement**
   - Dans Render dashboard, aller à **Environment**
   - Ajouter :
     ```
     SECRET_KEY=<genere-une-cle-random-longue>
     MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/agroconnect?retryWrites=true&w=majority
     FLASK_ENV=production
     ```

   **Pour MONGO_URI** :
   - Créer compte gratuit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Créer un cluster gratuit
   - Copier la chaîne de connexion

5. **Déployer**
   - Cliquer **Deploy**
   - Attendre ~5 min
   - Lien public HTTPS fourni ! 🎉

**Résultat** : `https://agroconnect-xxxx.onrender.com`

---

## **OPTION 2 : VPS Ubuntu (Plus de contrôle)**

### ✅ Avantages
- Contrôle total
- Meilleures performances
- Moins cher long terme

### 📋 Étapes

1. **Louer un VPS**
   - DigitalOcean ($5/mois), Linode, Hetzner
   - Ubuntu 22.04
   - Note l'IP

2. **SSH dans le VPS**
   ```bash
   ssh root@VOTRE_IP
   ```

3. **Installer les dépendances**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3-venv python3-pip nginx git certbot python3-certbot-nginx
   ```

4. **Cloner l'app**
   ```bash
   cd /var/www
   sudo git clone https://github.com/VOTRE_USERNAME/agroconnect.git
   cd agroconnect
   sudo python3 -m venv .venv
   sudo .venv/bin/pip install -r requirements.txt
   ```

5. **Copier les fichiers config**
   ```bash
   # Systemd service
   sudo cp agroconnect.service /etc/systemd/system/
   
   # Nginx
   sudo cp nginx-agroconnect.conf /etc/nginx/sites-available/agroconnect
   
   # Éditer domaine dans le fichier nginx
   sudo nano /etc/nginx/sites-available/agroconnect
   # Remplacer "yourdomain.com" par TON_DOMAINE.sn
   
   # Activer nginx
   sudo ln -s /etc/nginx/sites-available/agroconnect /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **Configurer SSL**
   ```bash
   sudo certbot --nginx -d ton-domaine.sn -d www.ton-domaine.sn
   ```

7. **Créer variables d'env**
   ```bash
   sudo mkdir -p /etc/agroconnect
   sudo nano /etc/agroconnect/.env
   ```
   
   Copier :
   ```
   SECRET_KEY=<genere-une-cle-random>
   MONGO_URI=mongodb://localhost:27017/agroconnect
   FLASK_ENV=production
   ```

8. **Lancer l'app**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start agroconnect
   sudo systemctl enable agroconnect
   sudo systemctl status agroconnect
   ```

9. **Configurer le domaine DNS**
   - Chez ton registraire (Namecheap, OVH, etc.)
   - Ajouter enregistrement **A** :
     ```
     @ → VPS_IP
     ```

**Résultat** : `https://ton-domaine.sn`

---

## **OPTION 3 : Docker Local (Pour tester)**

```bash
# Construire l'image
docker build -t agroconnect .

# Lancer le conteneur
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY="test_key" \
  -e MONGO_URI="mongodb://localhost:27017/" \
  --name agroconnect \
  agroconnect

# Accéder à http://localhost:5000
```

---

## 📋 Comparaison Rapide

| Critère | Render | VPS Ubuntu |
|---------|--------|-----------|
| **Setup** | 5 min ⚡ | 30 min |
| **Coût/mois** | $7+ | $5+ |
| **HTTPS** | Auto ✅ | Manual (Certbot) |
| **Uptime** | 99.9% | Dépend du VPS |
| **Scaling** | Auto | Manual |
| **Contrôle** | Limité | Complet |
| **Débutants** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Production** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recommandation** : Render pour débuter, VPS pour production.

---

## 🔧 Troubleshooting

### Erreur "MongoDB connection refused"

**Solution** :
1. Vérifier que MongoDB fonctionne
2. Utiliser MongoDB Atlas (cloud) au lieu de local
3. Mettre à jour `MONGO_URI`

### Erreur "Module not found: pymongo"

**Solution** :
```bash
# Dans Render/VPS
pip install -r requirements.txt
```

### Domaine ne fonctionne pas

**Solution** :
```bash
# Attendre propagation DNS (24h)
# Vérifier DNS : nslookup ton-domaine.sn
# Ou réinitialiser le DNS du registraire
```

### App crash au démarrage

**Logs** :
```bash
# Render
Logs tab dans Render dashboard

# VPS
sudo journalctl -u agroconnect -n 50
```

---

## ✅ Checklist Final

Avant d'aller en production :

- [ ] Repo GitHub créé et pushé
- [ ] Variables d'environnement configurées
- [ ] MongoDB connectée (local ou Atlas)
- [ ] Domaine acheté (si VPS)
- [ ] SSL activé (Render auto, VPS via Certbot)
- [ ] App testée en local
- [ ] Tests en production validés
- [ ] Domaine pointe vers l'app

---

## 🎓 Après le Déploiement

### Monitoring
```bash
# Render : Check "Log" tab
# VPS : sudo journalctl -u agroconnect -f
```

### Mises à Jour
```bash
# Git push → Render déploie auto
# VPS : git pull + systemctl restart agroconnect
```

### Backups
```bash
# MongoDB
mongodump --out=/backup/agroconnect_$(date +%Y%m%d)
```

---

## 📞 Support Rapide

| Problème | Solution |
|----------|----------|
| **Erreur 404** | Vérifier routes dans app.py |
| **Erreur 500** | Vérifier logs (journalctl/Render) |
| **Connexion DB** | Vérifier MONGO_URI |
| **SSL expired** | `sudo certbot renew` |
| **Port 5000 occupé** | `lsof -i :5000` then kill |

---

**Date** : 25 avril 2026  
**Version** : 1.0 Production Ready  
**Auteur** : Killifeu GUI  

Besoin d'aide ? Voir [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) pour le guide détaillé.
