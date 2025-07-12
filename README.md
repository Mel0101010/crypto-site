# CryptoTools

Suite d'outils cryptographiques pour l'analyse et le déchiffrement, incluant factorisation de nombres, cracking de hash et analyse RSA.

## 🔧 Fonctionnalités

- **Factorisation de nombres** – Plusieurs algorithmes disponibles :
  - Recherche dans FactorDB
  - Division par essai
  - Algorithme Rho de Pollard
  - Crible quadratique
- **Cracking de hash** – Test de différents types de hash contre des wordlists
- **Analyse RSA** – Extraction et analyse des composants d'une clé RSA

## 🚀 Accès & Installation

### Accès en ligne

Utilisation directe via l’interface web :  
[https://crypto-site-three.vercel.app](https://crypto-site-three.vercel.app)

Vous pouvez accéder à CryptoTools à tout moment via l’URL suivante :  
**https://crypto-site-three.vercel.app**

### Accès en local

> **Astuce** : En local, vous pouvez utiliser votre propre base de données pour la factorisation des nombres. Chaque nouveau nombre factorisé sera automatiquement ajouté à votre BDD personnelle.

#### Prérequis
- Python 3.8+
- pip

#### Étapes d'installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Mel0101010/crypto-tools.git
   cd crypto-tools
   ```
2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancez l'application :
   ```bash
   python app.py
   ```
5. Accédez à l'interface web sur [http://localhost:5000](http://localhost:5000)

## 🧰 Méthodes de factorisation

- **FactorDB** : Recherche dans une base de données de nombres déjà factorisés
- **Division par essai** : Méthode simple pour les petits nombres
- **Pollard Rho** : Algorithme probabiliste efficace pour des facteurs de taille moyenne
- **Crible quadratique** : Algorithme avancé pour la factorisation de grands nombres

## 🔒 Avertissement de sécurité

Cet outil est conçu à des fins éducatives et d'analyse de sécurité. N'utilisez pas ces outils pour des activités non autorisées ou illégales.

## 📝 Licence

Projet sous licence MIT. Voir le fichier `LICENSE` pour plus d’informations.
