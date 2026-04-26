# ⚡ AgroConnect - 60 Secondes

## 🎯 Qu'est-ce que c'est ?

**AgroConnect** = Plateforme web pour agriculteurs sénégalais
- 🛒 Marché agricole (vendre/acheter produits)
- 👥 Communauté d'agriculteurs
- ⭐ Avis produits (1-5 étoiles)
- 👨‍💼 Dashboard admin avancé
- 🚀 Production-ready (Docker, SSL, VPS)

---

## ✨ Quoi de Nouveau (v1.0)

✅ **Séparation Admin/User** - Chacun ne voit que ce qu'il faut
✅ **Avis Produits** - Notes, commentaires, calcul auto moyenne
✅ **Profils Vendeurs** - Page publique avec produits
✅ **Follow System** - Suivre vendeurs préférés
✅ **Recherche Avancée** - Filtres prix, région, catégorie
✅ **Dashboard Admin** - Stats complètes, gestion users
✅ **Production-Ready** - Docker, Nginx, SSL, Security

---

## 🚀 Déployer en 5-30 min

### Option 1️⃣ : Render (5 min - ⭐ Recommandé)
```bash
1. Git push sur GitHub
2. Connecter à Render.com
3. Ajouter env vars (SECRET_KEY, MONGO_URI)
4. Deploy automatique → Lien HTTPS public !
```

### Option 2️⃣ : VPS (30 min - Plus de contrôle)
```bash
1. Louer VPS Ubuntu (DigitalOcean $5/mois)
2. Clone repo + setup systemd
3. Configure Nginx + SSL (Certbot)
4. Point DNS → App live !
```

### Voir [QUICK_START.md](QUICK_START.md) pour détails

---

## 📚 Documentation

| Fichier | Lire Si | Temps |
|---------|---------|-------|
| **INDEX.md** | Tu cherches un guide | 2 min |
| **README.md** | Tu veux comprendre l'app | 10 min |
| **QUICK_START.md** | Tu veux déployer | 5-30 min |
| **DEPLOYMENT_GUIDE.md** | Tu veux tous les détails | 2h |
| **IMPROVEMENTS.md** | Tu veux voir quoi de nouveau | 15 min |
| **SUMMARY.md** | Tu veux un résumé complet | 10 min |
| **CHECKLIST.md** | Tu veux un checklist | 5 min |
| **Ce fichier** | Tu as 60 sec | 1 min |

**👉 Commencer par [INDEX.md](INDEX.md) ou [QUICK_START.md](QUICK_START.md)**

---

## 🔑 Comptes Test

```
Pseudo: babacar_agro
Mot de passe: agroconnect2024
Rôle: Admin

Pseudo: aissatou_farmers
Mot de passe: agroconnect2024
Rôle: Admin
```

Test sur http://localhost:5000/login

---

## 📁 Fichiers Clés

```
app.py                          ← Code principal (NOUVEAU)
requirements.txt                ← Dépendances (NOUVEAU)
Dockerfile                      ← Docker build (NOUVEAU)
nginx-agroconnect.conf         ← Nginx config (NOUVEAU)
agroconnect.service            ← Systemd service (NOUVEAU)
.env.example                   ← Variables d'env (NOUVEAU)

+ Documentation complète (7 fichiers)
```

---

## 🎯 Prochains Pas

1. **Tester localement** (5 min)
   ```bash
   cd /mnt/c/RONDOMNUMBER9/SD/agroconnect
   source .venv/bin/activate
   python3 app.py
   # → http://localhost:5000/login
   ```

2. **Créer repo GitHub** (5 min)
   ```bash
   git init && git add . && git commit -m "v1.0"
   git remote add origin https://github.com/USERNAME/agroconnect.git
   git push -u origin main
   ```

3. **Déployer** (5-30 min)
   - Render : [QUICK_START.md](QUICK_START.md#option-1--render-recommandé---5-min-)
   - VPS : [QUICK_START.md](QUICK_START.md#option-2--vps-ubuntu-plus-de-contrôle)

4. **Tester en production** (5 min)
   - Accéder lien publique
   - Tester login, marché, avis
   - Vérifier admin panel

5. **✅ Lancé !** 🎉

---

## 🔥 Features Clés

🛒 **Marché** - Voir/commander produits, filtrer
⭐ **Avis** - Laisser notes/commentaires
👨‍🌾 **Profils** - Voir détails vendeurs
❤️ **Follow** - Suivre vendeurs
📊 **Admin** - Dashboard complet + gestion

---

## 💬 Support Rapide

| Q | A |
|---|---|
| Erreur MongoDB ? | Utiliser MongoDB Atlas (cloud) |
| Module pas trouvé ? | `pip install -r requirements.txt` |
| Port 5000 occupé ? | `lsof -i :5000` + kill |
| SSL certificat ? | Certbot auto-configure (VPS) |
| Deploy pas marche ? | Vérifier logs + [CHECKLIST.md](CHECKLIST.md) |

---

## 📊 Tech Stack

- **Backend** : Flask 3.0 (Python)
- **Database** : MongoDB 4.6
- **Frontend** : HTML/CSS/JS
- **Server** : Gunicorn + Nginx
- **SSL** : Let's Encrypt
- **Deploy** : Render / VPS Ubuntu

---

## ⏱️ Temps Total

| Activité | Temps |
|----------|-------|
| Lire ce fichier | 1 min |
| Lire README | 10 min |
| Tester local | 5 min |
| Créer GitHub | 5 min |
| **Deploy Render** | **5 min** |
| **= TOTAL RENDER** | **26 min** |
| **Deploy VPS** | **30 min** |
| **= TOTAL VPS** | **50 min** |

---

## 🎓 Après Déploiement

- Monitoring logs
- Backup automatisé
- Updates Git → Auto-deploy (Render)
- Add features (chat, paiements, etc.)

Voir [IMPROVEMENTS.md](IMPROVEMENTS.md) pour roadmap

---

## ✅ Status

- ✅ **v1.0 Production Ready**
- ✅ **Toutées documented**
- ✅ **Secured & scalable**
- ✅ **Prête pour production**

---

## 🚀 GO !

### 👉 Prochaine étape ?

Choisis une option :

| Veut | Lire | Temps |
|------|------|-------|
| Déployer maintenant | [QUICK_START.md](QUICK_START.md) | 30 min |
| Comprendre code | [README.md](README.md) | 10 min |
| Tous les détails | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | 2h |
| Naviger docs | [INDEX.md](INDEX.md) | 2 min |

---

**Version** : 1.0 Production Ready
**Date** : 25 avril 2026
**Créé pour** : Déploiement facile & rapide

Bon courage ! 🚀 Tu vas réussir !
