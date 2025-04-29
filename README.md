```yaml
# CryptoTools Web

**CryptoTools Web** est une application web dédiée à la cryptographie, offrant plusieurs outils :

- 🔢 **Factorisateur de nombres** : décomposez un entier en facteurs premiers.

- 🔐 **Craqueur de hash** : essayez de retrouver le texte original à partir d'un hash connu.

- 🔑 **Vérificateur de clé RSA** : validez les paires de clés RSA pour assurer leur cohérence.
```

## 📚 Technologies

- **Frontend** : [React.js](https://reactjs.org/)
  
- **Backend** : [Flask](https://flask.palletsprojects.com/)
  
  ---
  

## 🛠 Fonctionnalités prévues

| Fonction | Description |
| --- | --- |
| Factorisation | Entrer un nombre entier et obtenir ses facteurs premiers. |
| Crack de hash | Entrer un hash et essayer de retrouver son texte clair par attaque dictionnaire. |
| Vérification de clé RSA | Vérifier la validité d'une clé publique/privée RSA fournie. |

---

## 🚀 Lancer le projet en local

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/crypto-tools-web.git
cd crypto-tools-web
```

### 2. Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
flask run
```

Par défaut, Flask tourne sur `http://127.0.0.1:5000/`.

**Fichier `requirements.txt` recommandé :**

```
Flask
Werkzeug
cryptography
```

---

### 3. Frontend (React)

```bash
cd frontend
npm install
npm start
```

Par défaut, React tourne sur `http://localhost:3000/`.

---

## 🔒 Remarque de sécurité

**Attention** : le craquage de hash repose sur des attaques par dictionnaire (wordlists). Ce projet est uniquement à but éducatif et **ne doit pas être utilisé pour des activités illégales**.

---

## 🧩 À venir

- Factorisation rapide par algorithme de Pollard (rho)
  
- Bruteforce distribué pour le craquage de hash
  
- Générateur de paires de clés RSA
  

---

## 🧑‍💻 Auteur

- Mel0

---
