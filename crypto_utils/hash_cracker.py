"""
Module de craquage de hachages
"""

import hashlib
import time

def crack_hash(hash_value, hash_type="md5", wordlist=None):
    """
    Tente de craquer un hash en utilisant une liste de mots (version minimale).
    
    Args:
        hash_value (str): Le hash à craquer
        hash_type (str): Type de hash (md5, sha1, sha256, etc.)
        wordlist (list): Liste de mots à essayer (optionnel)
        
    Returns:
        dict: Résultat du craquage
    """
    start_time = time.time()
    
    try:
        # Nettoyage du hash
        hash_value = hash_value.strip().lower()
        
        # Liste de mots par défaut (très limitée pour la version minimale)
        if not wordlist:
            wordlist = ["password", "123456", "admin", "welcome", "test"]
        
        # Sélectionner la fonction de hachage
        hash_func = None
        if hash_type == "md5":
            hash_func = hashlib.md5
        elif hash_type == "sha1":
            hash_func = hashlib.sha1
        elif hash_type == "sha256":
            hash_func = hashlib.sha256
        else:
            return {
                'success': False,
                'error': f"Type de hash non pris en charge: {hash_type}",
                'execution_time': time.time() - start_time
            }
        
        # Tester chaque mot
        for word in wordlist:
            word_hash = hash_func(word.encode()).hexdigest()
            if word_hash == hash_value:
                return {
                    'success': True,
                    'hash': hash_value,
                    'hash_type': hash_type,
                    'plaintext': word,
                    'attempts': wordlist.index(word) + 1,
                    'execution_time': time.time() - start_time
                }
        
        # Si aucune correspondance n'est trouvée
        return {
            'success': False,
            'hash': hash_value,
            'hash_type': hash_type,
            'message': "Aucune correspondance trouvée",
            'attempts': len(wordlist),
            'execution_time': time.time() - start_time
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }
