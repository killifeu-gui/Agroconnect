# 📋 Guide: Images, Commandes et Code

## 1️⃣ POURQUOI "MES ACHATS" ET "MES VENTES" N'AFFICHENT RIEN ?

### Réponse courte:
Les endpoints existent MAIS personne n'a fait de commandes encore! 

**C'est normal** = Les sections sont vides si:
- ❌ Aucune commande n'a été créée
- ❌ Ou les commandes ne s'affichent pas bien

### Les endpoints qui existent:

#### 1. **MES ACHATS** (Les produits que j'ai achetés)
```
GET /api/mes-commandes
Fichier: app.py ligne 550
Fonction: mes_commandes()

Cherche: commandes.find({"acheteur_id": MON_ID})
```

#### 2. **MES VENTES** (Les produits que j'ai vendus)
```
GET /api/commandes-recues
Fichier: app.py ligne 556
Fonction: commandes_recues()

Cherche: commandes.find({"vendeur_id": MON_ID})
```

#### 3. **CRÉER UNE COMMANDE** (Acheter un produit)
```
POST /api/commander
Fichier: app.py ligne 485
Fonction: commander()

Actions:
- Crée la commande
- Diminue le stock
- Envoie notification au vendeur
```

---

## 2️⃣ OÙ CHANGER LES PHOTOS DANS LE MARCHÉ ?

### 📍 LOCALISATION DU CODE DES IMAGES

Les images se trouvent dans **UN SEUL ENDROIT** dans le code:

**Fichier**: `c:\RONDOMNUMBER9\SD\agroconnect\app.py`  
**Ligne**: 149 à 165 (environ)  
**Fonction**: `init_db()` - Section "Products"

### 🔍 Code exact:

```python
# Dans app.py, ligne ~149
produits_data = [
    # LEGUMES
    {
        "nom":"Tomates fraîches",
        "vendeur_id": all_users[0]["_id"],
        "vendeur_pseudo": all_users[0]["pseudo"],
        "vendeur_avatar": all_users[0]["avatar"],
        "categorie": "Légumes",
        "prix": 500,
        "image": "https://cdn.pixabay.com/photo-1558618666-fcd25c85cd64_1280.jpg",  ← URL DE L'IMAGE
        "description": "Tomates rouges juteuses directement du champ",
        "stock": 50,
        ...
    },
    # AUTRES PRODUITS...
]
produits.insert_many(produits_data)
```

### ✏️ COMMENT CHANGER LES IMAGES

#### Méthode 1: Remplacer une URL
```python
# AVANT:
"image": "https://cdn.pixabay.com/photo-1558618666-fcd25c85cd64_1280.jpg",

# APRÈS (nouvelle image):
"image": "https://cdn.pixabay.com/photo-1111111111-aaaaaaaaaa_1280.jpg",
```

#### Méthode 2: Trouver des images gratuites
1. Va à https://pixabay.com
2. Cherche: "tomato" (ou le produit)
3. Copie l'URL de l'image (format: ...1280.jpg)
4. Remplace dans le code

#### Méthode 3: Utiliser d'autres sources
- **Unsplash**: https://unsplash.com (copie l'URL directe)
- **Pexels**: https://pexels.com
- **Pixabay**: https://pixabay.com
- **Freepik**: https://freepik.com

---

## 📋 STRUCTURE COMPLÈTE D'UN PRODUIT

```python
{
    "nom": "Tomates fraîches",                    # Nom du produit
    "vendeur_id": all_users[0]["_id"],          # ID du vendeur
    "vendeur_pseudo": all_users[0]["pseudo"],   # Pseudo du vendeur
    "vendeur_avatar": all_users[0]["avatar"],   # Avatar (emoji) vendeur
    "categorie": "Légumes",                      # Catégorie: "Légumes" ou "Fruits"
    "prix": 500,                                  # Prix en FCFA
    "image": "https://cdn.pixabay.com/...",     # URL de l'image
    "description": "Tomates rouges...",         # Description courte
    "stock": 50,                                 # Quantité disponible
    "disponible": True,                          # Disponible oui/non
    "region": all_users[0]["region"],           # Région (Dakar, Thiès, etc.)
    "date_ajout": datetime.now(),               # Date d'ajout
    "note_moyenne": 4.5,                        # Note sur 5
    "nb_avis": 8,                               # Nombre d'avis
}
```

---

## 🔄 FLUX COMPLET D'UNE COMMANDE

### 1. Utilisateur Lambda clique "Acheter"

```javascript
// Dans marche.html, ligne ~400
function acheter(produit_id) {
    fetch('/api/commander', {
        method: 'POST',
        body: JSON.stringify({
            produit_id: produit_id,
            quantite: 1
        })
    })
    .then(r => r.json())
    .then(data => {
        if(data.success) {
            alert('Commande créée!');
            // Recharge les commandes
            loadMesAchats();
        }
    })
}
```

### 2. Le serveur crée la commande

```python
# app.py ligne 485
@app.route("/api/commander", methods=["POST"])
def commander():
    # 1. Récupère le produit
    # 2. Vérifie le stock
    # 3. Crée la commande
    # 4. Diminue le stock
    # 5. Envoie notification au vendeur
```

### 3. Affichage dans "Mes achats"

```javascript
// app.html, appelle:
fetch('/api/mes-commandes')
    .then(cmds => affiche(cmds))
```

---

## 🛠️ FICHIERS À CONNAÎTRE

| Fichier | Contenu | Ligne | Fonction |
|---------|---------|-------|----------|
| `app.py` | Images des produits | 149-165 | `init_db()` |
| `app.py` | Créer commande | 485-540 | `commander()` |
| `app.py` | Mes achats API | 550-552 | `mes_commandes()` |
| `app.py` | Mes ventes API | 556-558 | `commandes_recues()` |
| `marche.html` | Interface marché | - | `acheter()` |
| `home.html` | Page d'accueil | - | `loadMesAchats()` |

---

## 🧪 TEST: Créer une commande manuellement

Depuis le terminal, tu peux tester:

```bash
# 1. Ouvre la console du navigateur (F12)
# 2. Copie ce code et exécute:

fetch('/api/commander', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        produit_id: 'ID_D_UN_PRODUIT_ICI',
        quantite: 1
    })
})
.then(r => r.json())
.then(data => console.log(data))
```

Si ça fonctionne: `{success: true, commande_id: "..."}`

---

## ❓ PROBLÈMES COURANTS

### "Mes achats" vide
**Raison**: Aucune commande créée  
**Solution**: Clique "Acheter" sur un produit

### Images ne s'affichent pas
**Raison**: URL Pixabay incorrecte  
**Solution**: Teste l'URL dans un onglet

### "Stock insuffisant"
**Raison**: Plus assez de stock  
**Solution**: Ajoute plus de stock dans `app.py`

### Erreur lors de la commande
**Raison**: Produit ou utilisateur non trouvé  
**Solution**: Vérifiez que vous êtes connecté

---

## 🚀 AJOUTER UN NOUVEAU PRODUIT

Pour ajouter un produit dans le marché:

1. Va à `app.py` ligne 149
2. Ajoute un nouvel objet dans la liste `produits_data`:

```python
produits_data = [
    # PRODUITS EXISTANTS...
    
    # NOUVEAU PRODUIT:
    {
        "nom": "Mangues Keitt",
        "vendeur_id": all_users[0]["_id"],
        "vendeur_pseudo": all_users[0]["pseudo"],
        "vendeur_avatar": all_users[0]["avatar"],
        "categorie": "Fruits",
        "prix": 1800,
        "image": "https://cdn.pixabay.com/photo-1234567890-abcdef_1280.jpg",
        "description": "Mangues Keitt juteuses et savoureuses",
        "stock": 30,
        "disponible": True,
        "region": all_users[0]["region"],
        "date_ajout": datetime.now(),
        "note_moyenne": 4.7,
        "nb_avis": 12,
    }
]
```

3. Redémarre le serveur
4. Le produit apparaît dans le marché!

---

**Besoin d'aide? Dis-moi quel changement tu veux faire!** 🎯
