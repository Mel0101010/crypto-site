# CryptoTools

Suite d'outils cryptographiques pour l'analyse et le déchiffrement, incluant factorisation de nombres, cracking de hash et analyse RSA.

## 🔧 Fonctionnalités

- **Factorisation de nombres** - Plusieurs algorithmes disponibles :
  - Recherche dans FactorDB
  - Division par essai
  - Algorithme Rho de Pollard
  - Crible quadratique
- **Cracking de hash** - Test de différents types de hash contre des wordlists
- **Analyse RSA** - Extraction et analyse des composants d'une clé RSA

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

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

## 💻 Utilisation

Lancez l'application :
```bash
python app.py
```

Accédez à l'interface web sur `http://localhost:5000`

## 🧰 Méthodes de factorisation

- **FactorDB** : Recherche dans une base de données de nombres déjà factorisés
- **Division par essai** : Méthode simple pour les petits nombres
- **Pollard Rho** : Algorithme probabiliste efficace pour des facteurs de taille moyenne
- **Crible quadratique** : Algorithme avancé pour la factorisation de grands nombres

## 📁 Structure du projet

```
crypto-tools/
├── app.py                 # Point d'entrée de l'application
├── routes.py              # Définition des routes Flask
├── crypto_utils/          # Modules cryptographiques
│   ├── factorizer.py      # Algorithmes de factorisation
│   ├── hash_cracker.py    # Outils de cracking de hash
│   └── rsa_utils.py       # Outils d'analyse RSA
├── static/                # Fichiers statiques
│   ├── css/               # Styles
│   └── js/                # Scripts client
└── templates/             # Templates HTML
    ├── index.html
    ├── factorizer.html
    ├── hash-cracker.html
    └── rsa-extractor.html
```

## 🔒 Avertissement de sécurité

Cet outil est conçu à des fins éducatives et d'analyse de sécurité. N'utilisez pas ces outils pour des activités non autorisées ou illégales.

## 📝 License

[MIT License](LICENSE)
