"""
Module pour le crackage de hash
Implémente différentes méthodes pour tenter de retrouver un texte original à partir de son hash
"""

import time
import hashlib
import itertools
import os
from pathlib import Path

def crack_hash(hash_value, hash_type, wordlist=None, mode="bruteforce", charset_name="alphanumeric", max_length=6):
    """
    Tente de retrouver le texte original à partir d'un hash.

    Args:
        hash_value (str): Le hash à cracker
        hash_type (str): Type de hash (md5, sha1, sha256, sha512)
        wordlist (str): Nom du dictionnaire à utiliser en mode dictionary
        mode (str): Mode d'attaque ("dictionary" ou "bruteforce")
        charset_name (str): Jeu de caractères pour le mode bruteforce
        max_length (int): Longueur maximale pour la force brute

    Returns:
        dict: Résultats du crackage avec succès ou échec
    """
    start_time = time.time()

    # Validation des entrées
    if not hash_value:
        return {
            'success': False,
            'error': "Aucun hash fourni",
            'execution_time': time.time() - start_time
        }

    # Normaliser le hash (enlever les espaces et convertir en minuscules)
    hash_value = hash_value.strip().lower()

    # Obtenir la fonction de hash correspondante
    hash_func = get_hash_function(hash_type)
    if not hash_func:
        return {
            'success': False,
            'error': f"Type de hash non supporté: {hash_type}",
            'execution_time': time.time() - start_time
        }

    # Exécuter la méthode de crackage appropriée
    if mode == "dictionary":
        return dictionary_attack(hash_value, hash_func, wordlist, start_time, hash_type)
    elif mode == "bruteforce":
        return bruteforce_attack(hash_value, hash_func, charset_name, max_length, start_time, hash_type)
    else:
        return {
            'success': False,
            'error': f"Mode d'attaque non supporté: {mode}",
            'execution_time': time.time() - start_time
        }

def get_hash_function(hash_type):
    """
    Retourne la fonction de hachage correspondant au type spécifié.

    Args:
        hash_type (str): Type de hash (md5, sha1, sha256, sha512)

    Returns:
        function: La fonction de hachage correspondante ou None si non supportée
    """
    hash_functions = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }

    return hash_functions.get(hash_type.lower())

def dictionary_attack(hash_value, hash_func, wordlist, start_time, hash_type):
    """
    Tente de cracker un hash en utilisant une attaque par dictionnaire.

    Args:
        hash_value (str): Le hash à cracker
        hash_func (function): La fonction de hash à utiliser
        wordlist (str): Le dictionnaire à utiliser
        start_time (float): Heure de début pour calculer le temps d'exécution
        hash_type (str): Type de hash pour le rapport

    Returns:
        dict: Résultat de l'attaque
    """
    # Chemins vers les dictionnaires
    base_dir = Path(__file__).parent.parent / "dictionaries"
    dictionaries = {
        'common': base_dir / "common_passwords.txt",
        'french': base_dir / "french.txt",
        'english': base_dir / "english.txt"
    }

    # Récupérer le chemin du dictionnaire
    dict_path = dictionaries.get(wordlist, dictionaries['common'])

    # Vérifier si le fichier existe
    if not dict_path.exists():
        return {
            'success': False,
            'error': f"Dictionnaire non trouvé: {dict_path}",
            'execution_time': time.time() - start_time
        }

    # Compteur de tentatives
    attempts = 0

    try:
        # Lire le dictionnaire et tester chaque mot
        with open(dict_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                attempts += 1

                # Nettoyer le mot
                word = line.strip()

                # Calculer le hash du mot
                word_hash = hash_func(word.encode()).hexdigest()

                # Vérifier si le hash correspond
                if word_hash == hash_value:
                    return {
                        'success': True,
                        'found': True,
                        'hash': hash_value,
                        'original': word,
                        'type': hash_type,
                        'mode': 'dictionary',
                        'attempts': attempts,
                        'execution_time': time.time() - start_time
                    }

        # Si aucune correspondance n'est trouvée
        return {
            'success': True,
            'found': False,
            'hash': hash_value,
            'type': hash_type,
            'mode': 'dictionary',
            'attempts': attempts,
            'execution_time': time.time() - start_time
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur lors de l'attaque par dictionnaire: {str(e)}",
            'execution_time': time.time() - start_time
        }

def bruteforce_attack(hash_value, hash_func, charset_name, max_length, start_time, hash_type):
    """
    Tente de cracker un hash en utilisant une attaque par force brute.

    Args:
        hash_value (str): Le hash à cracker
        hash_func (function): La fonction de hash à utiliser
        charset_name (str): Le nom du jeu de caractères à utiliser
        max_length (int): La longueur maximale à essayer
        start_time (float): Heure de début pour calculer le temps d'exécution
        hash_type (str): Type de hash pour le rapport

    Returns:
        dict: Résultat de l'attaque
    """
    # Définir les jeux de caractères selon l'option choisie
    charsets = {
        "numeric": "0123456789",
        "alpha": "abcdefghijklmnopqrstuvwxyz",
        "alphanumeric": "abcdefghijklmnopqrstuvwxyz0123456789",
        "full": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/"
    }

    # Récupérer le jeu de caractères sélectionné
    charset = charsets.get(charset_name, charsets["alphanumeric"])

    # Vérifier que max_length est raisonnable
    if max_length > 10:
        max_length = 10  # Limiter pour éviter des temps d'exécution excessifs

    # Compteur de tentatives
    attempts = 0

    try:
        # Générer et tester toutes les combinaisons
        for length in range(1, max_length + 1):
            for combination in itertools.product(charset, repeat=length):
                attempts += 1
                word = ''.join(combination)
                word_hash = hash_func(word.encode()).hexdigest()

                if word_hash == hash_value:
                    return {
                        'success': True,
                        'found': True,
                        'hash': hash_value,
                        'original': word,
                        'type': hash_type,
                        'mode': 'bruteforce',
                        'attempts': attempts,
                        'execution_time': time.time() - start_time
                    }

                # Option pour limiter le nombre total de tentatives
                if attempts >= 10000000:  # 10 millions de tentatives max
                    return {
                        'success': True,
                        'found': False,
                        'hash': hash_value,
                        'type': hash_type,
                        'mode': 'bruteforce',
                        'attempts': attempts,
                        'message': "Limite de tentatives atteinte sans trouver de correspondance",
                        'execution_time': time.time() - start_time
                    }

        # Si aucune correspondance n'est trouvée après avoir essayé toutes les combinaisons
        return {
            'success': True,
            'found': False,
            'hash': hash_value,
            'type': hash_type,
            'mode': 'bruteforce',
            'attempts': attempts,
            'message': "Aucune correspondance trouvée en mode bruteforce",
            'execution_time': time.time() - start_time
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur lors de l'attaque par force brute: {str(e)}",
            'execution_time': time.time() - start_time
        }

def hash_string(text, hash_type):
    """
    Utilitaire pour hacher une chaîne avec l'algorithme spécifié.

    Args:
        text (str): Texte à hacher
        hash_type (str): Type de hash (md5, sha1, sha256, sha512)

    Returns:
        str: Hash généré ou None en cas d'erreur
    """
    hash_func = get_hash_function(hash_type)
    if not hash_func:
        return None

    return hash_func(text.encode()).hexdigest()