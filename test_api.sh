#!/bin/bash

# Configuration
API_URL="http://localhost:8000/api"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxODgyNzc0LCJpYXQiOjE3ODE3OTYzNzQsImp0aSI6IjBjMDc0YWRkMGU2YjRkMmNhNjdhNjc4NzA0MTFiOTg5IiwidXNlcl9pZCI6IjIifQ.eqhBzfvVkaBxVNDyM194LC6vNz0iCcUDymSM1K7PD5k"


echo "========================================="
echo "🔍 TEST COMPLET DE L'API EMPREINTE"
echo "========================================="

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction de test
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"

    echo -e "\n${YELLOW}📌 Test: ${name}${NC}"
    echo "➜ $method $endpoint"

    if [ "$method" = "GET" ]; then
        response=$(curl -s -X GET "${API_URL}${endpoint}" \
            -H "Authorization: Bearer $TOKEN")
    else
        response=$(curl -s -X $method "${API_URL}${endpoint}" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d "$data")
    fi

    # Vérifier si la réponse est vide
    if [ -z "$response" ] || [ "$response" = "[]" ]; then
        echo -e "${RED}❌ Réponse vide ou erreur${NC}"
    else
        echo -e "${GREEN}✅ Succès${NC}"
        echo "$response" | python -m json.tool 2>/dev/null || echo "$response"
    fi
}

# === TESTS ===

# Produits
test_endpoint "Liste des produits" "GET" "/products/"
test_endpoint "Produits Homme" "GET" "/products/?gender=H"
test_endpoint "Produits Femme" "GET" "/products/?gender=F"
test_endpoint "Détail produit #1" "GET" "/products/1/"
test_endpoint "Produits catégorie chaussures-homme" "GET" "/products/category/chaussures-homme/"

# Catégories
test_endpoint "Liste des catégories" "GET" "/products/categories/"
test_endpoint "Détail catégorie sacs" "GET" "/products/categories/sacs/"

# Panier
test_endpoint "Ajouter au panier" "POST" "/orders/cart/" '{"product_id":1,"color":"Noir","size":"41","quantity":1}'
test_endpoint "Voir le panier" "GET" "/orders/cart/"

# Commande
test_endpoint "Valider commande" "POST" "/orders/checkout/" '{"delivery_address":"Cotonou, Bénin","phone":"97000000"}'
test_endpoint "Historique commandes" "GET" "/orders/orders/"

# Profil
test_endpoint "Voir le profil" "GET" "/accounts/profile/"

echo -e "\n${GREEN}✅ Tests terminés !${NC}"
