# Empreintes — Backend

API REST pour l'application Empreintes, construite avec Django et Django REST Framework.

## Stack technique

- Python 3.10
- Django 4.2
- Django REST Framework
- Simple JWT (authentification par jetons)
- django-cors-headers
- SQLite (développement)
- Pillow (gestion des images produits)

## Structure du projet

```text
Backend/
├── config/            # Configuration Django (settings, urls, wsgi/asgi)
├── apps/
│   ├── accounts/       # Utilisateurs, inscription, connexion, profil
│   ├── products/       # Catégories, produits, images produits
│   └── orders/         # Panier, commandes, checkout
├── media/              # Fichiers uploadés (images produits)
├── manage.py
└── requirements.txt
```

## Installation

```bash
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration de la base de données

Le projet utilise SQLite par défaut, aucune configuration supplémentaire n'est requise en développement.

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Lancer le serveur

```bash
python manage.py runserver
```

L'API est disponible sur `http://localhost:8000/`, l'admin Django sur `http://localhost:8000/admin/`.

## Principaux points d'entrée de l'API

| Ressource | Préfixe |
| --- | --- |
| Comptes | `/api/accounts/` (register, login, token/refresh, profile, ...) |
| Produits | `/api/products/` (catégories, produits, images) |
| Commandes | `/api/orders/` (cart, checkout, orders) |

## CORS

Les origines suivantes sont autorisées par défaut pour le développement :

- `http://localhost:5173` (Vite)
- `http://localhost:3000`

## Tests

```bash
python manage.py test
```
