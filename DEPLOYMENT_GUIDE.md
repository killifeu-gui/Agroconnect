# 📖 Guide Complet de Déploiement - AgroConnect

## Table des matières
1. [Option A : Déploiement Rapide (Render)](#option-a--déploiement-rapide-render)
2. [Option B : VPS Ubuntu avec Nginx](#option-b--vps-ubuntu-avec-nginx)
3. [Configuration Production](#configuration-production)
4. [Monitoring & Maintenance](#monitoring--maintenance)

---

## **OPTION A : Déploiement Rapide (RENDER)**

### Avantages
✅ HTTPS automatique
✅ CI/CD intégré
✅ Pas de configuration serveur
✅ Scaling automatique

### Étapes

#### 1️⃣ **Préparer le repo GitHub**

```bash
# Sur ta machine locale (dans le dossier agroconnect)
git init
git add .
git commit -m "Initial commit: AgroConnect v1.0"
git branch -M main
git remote add origin https://github.com/TON_USERNAME/agroconnect.git
git push -u origin main
```

#### 2️⃣ **Créer un compte sur Render**

- Va sur [render.com](https://render.com)
- Sign up (recommandé: via GitHub)
- Connecte ton repo GitHub

#### 3️⃣ **Créer un Web Service**

1. Dashboard Render → **New** → **Web Service**
2. Connecte ton repo `agroconnect`
3. Configuration :
   - **Name** : `agroconnect`
   - **Environment** : `Docker`
   - **Build Command** : (vide, Render l'auto-détecte)
   - **Start Command** : (vide, Render utilise Dockerfile)
   - **Publish port** : `5000`

#### 4️⃣ **Ajouter les Variables d'Environnement**

Dans le dashboard Render, ajoute ces variables sous **Environment**:

```
SECRET_KEY=<genere-une-longue-cle-aleatoire>
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/agroconnect?retryWrites=true&w=majority
FLASK_ENV=production
FLASK_DEBUG=False
```

**Pour MongoDB** :
- Crée un compte [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Crée un cluster gratuit
- Génère une chaîne de connexion `MONGO_URI`

#### 5️⃣ **Déployer**

Render déploie automatiquement à chaque `git push` sur `main`.

```bash
# Local
git push origin main

# Render va automatiquement :
# 1. Construire l'image Docker
# 2. Lancer le conteneur
# 3. Fournir un lien HTTPS public
```

**Lien public** : `https://agroconnect-xxxx.onrender.com`

---

## **OPTION B : VPS Ubuntu avec Nginx**

### Avantages
✅ Contrôle total
✅ Trafic élevé supporté
✅ Moins cher à long terme

### Prérequis

- VPS Ubuntu 22.04 (DigitalOcean, Linode, etc.)
- SSH access
- Domaine (ex: `agroconnect.sn`)

### Étapes

#### 1️⃣ **Provision du VPS**

```bash
# SSH dans le VPS
ssh root@YOUR_VPS_IP

# Update systeme
sudo apt update && sudo apt upgrade -y

# Installer dépendances systeme
sudo apt install -y python3-venv python3-pip nginx git curl wget certbot python3-certbot-nginx

# Installer MongoDB (optionnel si tu utilises MongoDB Atlas)
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Créer l'utilisateur pour l'app
sudo useradd -m -s /bin/bash agroconnect
sudo -u agroconnect mkdir -p /var/www
```

#### 2️⃣ **Cloner et Setup l'Application**

```bash
# En tant qu'utilisateur root ou avec sudo

cd /var/www
sudo git clone https://github.com/TON_USERNAME/agroconnect.git
sudo chown -R agroconnect:agroconnect agroconnect

cd agroconnect

# Créer virtualenv
sudo -u agroconnect python3 -m venv .venv

# Activer et installer dépendances
sudo -u agroconnect .venv/bin/pip install --upgrade pip
sudo -u agroconnect .venv/bin/pip install -r requirements.txt
```

#### 3️⃣ **Configurer les Variables d'Environnement**

```bash
# Créer le fichier de config
sudo mkdir -p /etc/agroconnect
sudo nano /etc/agroconnect/.env
```

**Contenu** :
```
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=<genere-une-longue-cle-aleatoire>
MONGO_URI=mongodb://localhost:27017/agroconnect
PORT=5000
```

```bash
# Permissions
sudo chown agroconnect:agroconnect /etc/agroconnect/.env
sudo chmod 600 /etc/agroconnect/.env
```

#### 4️⃣ **Créer le Service Systemd**

```bash
# Copier le fichier systemd
sudo cp /var/www/agroconnect/agroconnect.service /etc/systemd/system/

# Créer répertoire logs
sudo mkdir -p /var/log/agroconnect
sudo chown agroconnect:agroconnect /var/log/agroconnect

# Activer le service
sudo systemctl daemon-reload
sudo systemctl start agroconnect
sudo systemctl enable agroconnect
sudo systemctl status agroconnect
```

**Vérifier les logs** :
```bash
sudo journalctl -u agroconnect -f
```

#### 5️⃣ **Configurer Nginx**

```bash
# Copier la config
sudo cp /var/www/agroconnect/nginx-agroconnect.conf /etc/nginx/sites-available/agroconnect

# Éditer domaine (remplacer yourdomain.com par TON_DOMAINE.sn)
sudo nano /etc/nginx/sites-available/agroconnect

# Créer symlink
sudo ln -s /etc/nginx/sites-available/agroconnect /etc/nginx/sites-enabled/

# Tester config
sudo nginx -t

# Redémarrer nginx
sudo systemctl restart nginx
```

#### 6️⃣ **Configurer SSL avec Let's Encrypt**

```bash
# Remplacer yourdomain.com par TON DOMAINE
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Certbot va automatiquement :
# 1. Générer les certificats
# 2. Modifier la config nginx
# 3. Redémarrer nginx
```

**Auto-renewal** (déjà inclus) :
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

#### 7️⃣ **Configuration DNS**

Dans ton registraire de domaine (ex: Namecheap, OVH) :

Ajoute un enregistrement **A** :
```
Nom : @
Type : A
Valeur : YOUR_VPS_IP
TTL : 3600
```

Attends 24h pour la propagation DNS.

#### 8️⃣ **Tester l'Application**

```bash
# Vérifier que le service tourne
sudo systemctl status agroconnect

# Vérifier que nginx écoute
sudo netstat -tlnp | grep nginx

# Test local (sur le VPS)
curl http://127.0.0.1:8000

# Test depuis l'extérieur (remplacer yourdomain.com)
curl https://yourdomain.com
```

---

## **Configuration Production**

### Sécurité

#### 1. **Mise à jour automatique**

```bash
# Sur le VPS
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

#### 2. **Firewall**

```bash
sudo apt install -y ufw
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw status
```

#### 3. **Fail2Ban (protection brute-force)**

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Performance

#### 1. **Cache et Gzip** (déjà dans nginx.conf)

- Gzip compression activé
- Cache-Control headers configurés

#### 2. **Database Optimization**

```bash
# Dans MongoDB, créer des index
# SSH → mongosh → agroconnect database

mongosh
use agroconnect

# Index sur pseudo (recherche rapide)
db.utilisateurs.createIndex({ pseudo: 1 })

# Index sur date (tri rapide)
db.commandes.createIndex({ date_commande: -1 })

# Index sur catégorie produit
db.produits.createIndex({ categorie: 1 })
```

---

## **Monitoring & Maintenance**

### Logs

```bash
# Flask errors
sudo journalctl -u agroconnect -n 50 --no-pager

# Nginx access
sudo tail -f /var/log/nginx/agroconnect_access.log

# Nginx errors
sudo tail -f /var/log/nginx/agroconnect_error.log

# All system logs
sudo tail -f /var/log/syslog
```

### Updates

```bash
# Mettre à jour l'app (depuis repo)
cd /var/www/agroconnect
sudo -u agroconnect git pull origin main
sudo -u agroconnect .venv/bin/pip install -r requirements.txt

# Redémarrer l'app
sudo systemctl restart agroconnect
```

### Backup MongoDB

```bash
# Backup manual
mongodump --out=/backup/agroconnect_backup_$(date +%Y%m%d)

# Restore
mongorestore --dir=/backup/agroconnect_backup_20240425
```

### Monitoring en Temps Réel

```bash
# CPU, Memory, Disk
watch -n 1 'free -h && df -h / && ps aux | grep gunicorn'

# Stats Nginx
curl -s http://localhost:8000/api/stats  # (si tu ajoutes une route stats)
```

---

## **Troubleshooting**

### L'app ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u agroconnect -n 100

# Vérifier la connexion MongoDB
mongosh
show dbs

# Relancer manuellement pour déboguer
cd /var/www/agroconnect
.venv/bin/python3 app.py
```

### Certificat SSL expiré

```bash
# Renouveler manuellement
sudo certbot renew --dry-run
sudo certbot renew

# Vérifier la date d'expiration
sudo certbot certificates
```

### Connexion refusée (ERR_CONNECTION_REFUSED)

```bash
# Vérifier que nginx tourne
sudo systemctl status nginx

# Vérifier que le service Flask tourne
sudo systemctl status agroconnect

# Vérifier les ports
sudo netstat -tlnp
```

---

## **Checklist Final**

- [ ] Repo GitHub pushé avec tous les fichiers
- [ ] Variables d'environnement configurées
- [ ] MongoDB connecté (local ou Atlas)
- [ ] Domaine acheté
- [ ] DNS configuré
- [ ] SSL automatique (certbot)
- [ ] Nginx configuré et actif
- [ ] Service systemd actif
- [ ] Logs vérifiés
- [ ] Test accès HTTPS public

---

## **Support**

En cas de problème :
1. Vérifier les logs (`journalctl`, `tail`)
2. Tester localement (`curl`, Python shell)
3. Vérifier la connectivité MongoDB
4. Vérifier les permissions des fichiers
5. Relancer les services

**Commandes utiles** :
```bash
sudo systemctl restart agroconnect
sudo systemctl restart nginx
sudo journalctl -u agroconnect -f
```

---

**Date mise à jour** : 25 avril 2026
**Version** : 1.0 (avec améliorations UX/Admin)
