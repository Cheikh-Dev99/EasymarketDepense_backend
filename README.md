# EasyMarket Dépenses - Backend API

## 📋 Description
API backend développée avec Django REST Framework pour l'application EasyMarket Dépenses. Gère le stockage et le traitement des dépenses avec support pour les pièces justificatives.

## 🛠 Technologies
- Django 5.1.5
- Django REST Framework 3.15.2
- PostgreSQL
- Python 3.8+

## 📚 Documentation API

### Endpoints

#### Dépenses
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/depenses/` | Liste toutes les dépenses |
| POST | `/api/depenses/` | Crée une nouvelle dépense |
| GET | `/api/depenses/{id}/` | Détails d'une dépense |
| PUT | `/api/depenses/{id}/` | Met à jour une dépense |
| DELETE | `/api/depenses/{id}/` | Supprime une dépense |

### Exemples de Requêtes

#### Créer une dépense
```http
POST /api/depenses/
Content-Type: multipart/form-data

{
  "title": "Facture",
  "amount": "150000",
  "category": "ELECTRICITE",
  "payment_method": "WAVE",
  "piece_justificative": [fichier]
}
```

#### Réponse
```json
{
  "id": 1,
  "title": "Facture",
  "amount": "150000.00",
  "category": "ELECTRICITE",
  "payment_method": "WAVE",
  "piece_justificative": "http://api.example.com/media/pieces_justificatives/facture.pdf",
  "timestamp": "2024-03-20T10:30:00Z"
}
```

## 🚀 Installation

1. **Cloner le projet**
```bash
git clone [url-du-projet]
cd EasymarketDepense_backend
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Variables d'environnement**
Créer un fichier `.env` à la racine du projet :
```env
SECRET_KEY=votre_clé_secrète
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Migrations**
```bash
python manage.py migrate
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

## 📝 Structure du Projet
```
EasymarketDepense_backend/
├── easymarketdepense_backend/    # Configuration principale
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── easymarketdepenses/           # Application principale
│   ├── models.py                 # Modèles de données
│   ├── views.py                  # Vues API
│   ├── serializers.py           # Sérialiseurs
│   └── urls.py                  # Routes API
├── media/                       # Fichiers uploadés
├── requirements.txt            # Dépendances
└── manage.py                   # Script Django
```

## 🔧 Configuration

### Base de données
L'application utilise PostgreSQL. Assurez-vous d'avoir PostgreSQL installé et configuré.

### Stockage des fichiers
Les pièces justificatives sont stockées dans le dossier `media/pieces_justificatives/`.

### CORS
CORS est configuré pour accepter les requêtes du frontend React Native.

## 📱 Modèle de Données

### Depense
- `title`: Titre de la dépense
- `amount`: Montant (decimal)
- `category`: Type de dépense
  - Choix: SALAIRE, EAU, ELECTRICITE, LOYER, TRANSPORT, APPROVISIONNEMENT, AUTRE
- `custom_category`: Catégorie personnalisée (si AUTRE)
- `payment_method`: Moyen de paiement
  - Choix: WAVE, ORANGE MONEY, FREE MONEY, CASH
- `piece_justificative`: Document justificatif
- `timestamp`: Date de création
- `updated_at`: Date de modification

## 🔐 Sécurité
- Protection CSRF activée
- Validation des fichiers uploadés
- Limitation de la taille des fichiers
- Types de fichiers autorisés : PDF, JPEG, PNG

## 🚀 Déploiement
L'application est déployée sur Render.com
- URL de l'API : https://easymarketdepense-backend.onrender.com/api/
- Base de données : PostgreSQL hébergée sur Render

## 👥 Équipe
- Cheikh Ahmed Tidiane Gueye

---
Développé avec ❤️ pour EasyMarket
