"""
Module d'analyse et d'extraction des paramètres des clés RSA
"""

import time
import base64
import re
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def analyze_rsa_key(key_type, key_content, options=None):
    """
    Analyse une clé RSA et extrait ses paramètres.

    Args:
        key_type (str): Type de format ('PEM', 'DER', 'modulus-exponent')
        key_content (str): Contenu de la clé
        options (dict): Options d'analyse supplémentaires

    Returns:
        dict: Résultats de l'analyse avec paramètres extraits
    """
    start_time = time.time()

    try:
        result = {
            'success': True,
            'keyType': key_type,
            'methodsUsed': ['Analyse de clé'],
        }

        # Extraction des paramètres selon le format
        if key_type == 'PEM':
            key_params = extract_from_pem(key_content)
        elif key_type == 'DER':
            key_params = extract_from_der(key_content)
        elif key_type == 'modulus-exponent':
            key_params = extract_from_modulus_exponent(key_content)
        else:
            key_params = auto_detect_and_extract(key_content)

        # Fusion des paramètres extraits dans le résultat
        result.update(key_params)

        # Analyse de sécurité de la clé
        vulnerabilities = analyze_security(result)
        if vulnerabilities:
            result['vulnerabilities'] = vulnerabilities

        result['execution_time'] = time.time() - start_time
        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }

def extract_from_pem(key_content):
    """Extrait les paramètres d'une clé au format PEM"""
    try:
        # Tentative de chargement comme clé publique
        key = serialization.load_pem_public_key(
            key_content.encode(),
            backend=default_backend()
        )
        is_private = False
    except:
        try:
            # Tentative de chargement comme clé privée
            key = serialization.load_pem_private_key(
                key_content.encode(),
                password=None,
                backend=default_backend()
            )
            is_private = True
        except:
            raise ValueError("Format PEM invalide ou non reconnu")

    # Extraction des paramètres communs
    public_numbers = key.public_numbers()
    result = {
        'modulus': str(public_numbers.n),
        'publicExponent': public_numbers.e,
        'keySize': key.key_size,
        'isPrivate': is_private
    }

    # Extraction des paramètres privés si disponibles
    if is_private:
        private_numbers = key.private_numbers()
        result.update({
            'privateExponent': str(private_numbers.d),
            'prime1': str(private_numbers.p),
            'prime2': str(private_numbers.q),
            'factorsFound': True
        })

    return result

def extract_from_der(key_content):
    """Extrait les paramètres d'une clé au format DER"""
    try:
        if isinstance(key_content, str):
            # Convertir la chaîne base64 en bytes
            binary_data = base64.b64decode(key_content)
        else:
            binary_data = key_content

        try:
            # Tentative de chargement comme clé publique
            key = serialization.load_der_public_key(
                binary_data,
                backend=default_backend()
            )
            is_private = False
        except:
            # Tentative de chargement comme clé privée
            key = serialization.load_der_private_key(
                binary_data,
                password=None,
                backend=default_backend()
            )
            is_private = True

        # Suite similaire à extract_from_pem
        public_numbers = key.public_numbers()
        result = {
            'modulus': str(public_numbers.n),
            'publicExponent': public_numbers.e,
            'keySize': key.key_size,
            'isPrivate': is_private
        }

        if is_private:
            private_numbers = key.private_numbers()
            result.update({
                'privateExponent': str(private_numbers.d),
                'prime1': str(private_numbers.p),
                'prime2': str(private_numbers.q),
                'factorsFound': True
            })

        return result

    except Exception as e:
        raise ValueError(f"Erreur lors de l'analyse du format DER: {str(e)}")

def extract_from_modulus_exponent(key_content):
    """Extrait les paramètres à partir des valeurs n et e données"""
    try:
        lines = key_content.strip().split('\n')
        modulus = None
        exponent = None

        for line in lines:
            line = line.strip()
            if line.startswith('n =') or line.startswith('modulus ='):
                modulus = re.search(r'(?:n|modulus) = (\d+)', line)
                if modulus:
                    modulus = modulus.group(1)
            elif line.startswith('e =') or line.startswith('exponent ='):
                exponent = re.search(r'(?:e|exponent) = (\d+)', line)
                if exponent:
                    exponent = exponent.group(1)

        if not modulus or not exponent:
            raise ValueError("Impossible d'extraire le module ou l'exposant")

        modulus = int(modulus)
        exponent = int(exponent)

        return {
            'modulus': str(modulus),
            'publicExponent': exponent,
            'keySize': modulus.bit_length(),
            'isPrivate': False
        }
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction n, e: {str(e)}")

def auto_detect_and_extract(key_content):
    """Détecte automatiquement le format et extrait les paramètres"""
    if '-----BEGIN' in key_content and '-----END' in key_content:
        return extract_from_pem(key_content)
    elif 'n =' in key_content or 'modulus =' in key_content:
        return extract_from_modulus_exponent(key_content)
    else:
        try:
            return extract_from_der(key_content)
        except:
            # Dernière tentative: considérer comme un module seul
            try:
                modulus = int(key_content.strip())
                return {
                    'modulus': str(modulus),
                    'publicExponent': 65537,  # e standard
                    'keySize': modulus.bit_length(),
                    'isPrivate': False,
                    'note': "Seulement le modulus a été fourni, e=65537 est supposé"
                }
            except:
                raise ValueError("Format de clé non reconnu")

def analyze_security(key_data):
    """Analyse la sécurité de la clé RSA"""
    vulnerabilities = []

    # Vérification de la taille de la clé
    if key_data.get('keySize', 0) < 2048:
        vulnerabilities.append({
            'name': 'Clé de taille insuffisante',
            'description': 'Les clés RSA devraient être d\'au moins 2048 bits selon les standards actuels.',
            'severity': 'Élevée'
        })

    # Vérification de l'exposant public
    if key_data.get('publicExponent', 0) < 65537:
        vulnerabilities.append({
            'name': 'Exposant public faible',
            'description': 'L\'exposant public devrait être au moins 65537 pour une meilleure sécurité.',
            'severity': 'Moyenne'
        })

    return vulnerabilities