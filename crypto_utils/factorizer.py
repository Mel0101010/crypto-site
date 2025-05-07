"""
Module de factorisation de nombres
"""
import math
import time
import random
from factordb.factordb import FactorDB
from .factorisation_bdd import initialize_local_db, check_local_db, save_to_local_db

def factorize_using_factordb(n):
    """Factorise un nombre en utilisant FactorDB"""
    f = FactorDB(n)
    f.connect()
    factor_data = f.get_factor_list()

    # Vérifier si la factorisation est complète
    if f.get_status() == "FF":  # FF = "fully factored"
        return {
            'success': True,
            'factors': factor_data,
            'source': 'FactorDB'
        }
    return {
        'success': False,
        'error': 'Factorisation incomplète avec FactorDB',
    }

def factorize_using_trial_division(n):
    """Factorise un nombre par division d'essai"""
    factors = []

    # Vérifier facteurs 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Vérifier facteurs impairs
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i

    # Si n est un nombre premier > 2
    if n > 2:
        factors.append(n)

    return {
        'success': True,
        'factors': factors,
        'source': 'division par essai'
    }

def gcd(a, b):
    """Calcule le plus grand commun diviseur de a et b"""
    while b:
        a, b = b, a % b
    return a

def is_prime(n):
    """Test de primalité simple (pour les petits nombres)"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def factorize_using_pollard_rho(n):
    """Implémentation de l'algorithme Rho de Pollard"""
    if n % 2 == 0:
        return {
            'success': True,
            'factors': [2] + factorize_number(n // 2, "pollard-rho")['factors'],
            'source': 'Pollard Rho'
        }

    if is_prime(n):
        return {
            'success': True,
            'factors': [n],
            'source': 'Pollard Rho'
        }

    def find_factor(n):
        if n == 1:
            return 1
        if is_prime(n):
            return n

        # Fonction f(x) = (x^2 + c) mod n
        c = random.randint(1, n-1)
        def f(x):
            return (x*x + c) % n

        # Initialisation
        x = random.randint(1, n-1)
        y = x
        d = 1

        # Boucle principale
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x-y), n)

            if d == n:
                # Échec, on réessaie avec d'autres valeurs
                return find_factor(n)

        # d est un facteur trouvé
        return d

    try:
        factor = find_factor(n)
        if factor == n:
            return {
                'success': True,
                'factors': [n],
                'source': 'Pollard Rho'
            }

        # Factoriser récursivement
        factors1 = factorize_number(factor, "trial-division")['factors']
        factors2 = factorize_number(n // factor, "trial-division")['factors']

        return {
            'success': True,
            'factors': sorted(factors1 + factors2),
            'source': 'Pollard Rho'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur lors de l'exécution de Pollard Rho: {str(e)}"
        }

def is_prime_q(n):
    """Test de primalité rapide"""
    return is_prime(n)  # Simplifié pour cet exemple

def legendre_symbol(a, p):
    """Calcul du symbole de Legendre (a/p)"""
    if p < 2:
        raise ValueError("p doit être un nombre premier ≥ 2")
    if a == 0:
        return 0
    if a % p == 0:
        return 0

    result = 1
    a = a % p

    # Loi de réciprocité quadratique
    while a > 1:
        if a % 2 == 0:
            a = a // 2
            # Si p mod 8 est 3 ou 5, on inverse le signe
            if p % 8 in (3, 5):
                result = -result
        else:
            a, p = p, a
            # Si a mod 4 est 3 et p mod 4 est 3, on inverse le signe
            if a % 4 == 3 and p % 4 == 3:
                result = -result
            a = a % p

    return result

def is_bsmooth(n, primes):
    """Vérifie si n est B-smooth par rapport à la base de facteurs premiers"""
    temp = n
    for p in primes:
        while temp % p == 0:
            temp //= p
    return temp == 1

def is_perfect_square(n):
    """Vérifie si n est un carré parfait"""
    root = int(math.sqrt(n))
    return root * root == n

def factorize_using_quadratic_sieve(n):
    """Version simplifiée du crible quadratique"""
    try:
        # Vérifier si n est pair
        if n % 2 == 0:
            return {
                'success': True,
                'factors': [2] + factorize_number(n // 2, "trial-division")['factors'],
                'source': 'Crible quadratique'
            }

        # Pour les petits nombres, utiliser la division par essai
        if n < 1000000:
            result = factorize_using_trial_division(n)
            result['source'] = 'Crible quadratique (fallback)'
            return result

        # Version simplifiée - si le nombre est trop grand, on utilise juste Pollard Rho
        result = factorize_using_pollard_rho(n)
        result['source'] = 'Crible quadratique (fallback)'
        return result

    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur lors de l'exécution du crible quadratique: {str(e)}"
        }

def factorize_number(number, method=None):
    """
    Factorise un nombre en ses facteurs premiers.
    Vérifie d'abord la base locale, puis utilise la méthode spécifiée.

    Args:
        number (str): Le nombre à factoriser
        method (str): Méthode de factorisation

    Returns:
        dict: Résultat de la factorisation
    """
    start_time = time.time()
    try:
        # Conversion du nombre en entier
        if isinstance(number, str):
            n = int(number.strip())
        else:
            n = number

        if n <= 1:
            return {
                'success': False,
                'error': 'Le nombre doit être supérieur à 1',
                'execution_time': time.time() - start_time
            }

        # Initialiser la base de données si nécessaire
        if not hasattr(factorize_number, 'db_initialized'):
            initialize_local_db()
            factorize_number.db_initialized = True

        # Vérifier dans la base locale
        cached_result = check_local_db(n)
        if cached_result:
            cached_result['execution_time'] = time.time() - start_time
            return cached_result

        # Sélection de la méthode de factorisation
        if method == "factor-db":
            result = factorize_using_factordb(n)
        elif method == "pollard-rho":
            result = factorize_using_pollard_rho(n)
        elif method == "quadratic-sieve":
            result = factorize_using_quadratic_sieve(n)
        else:  # Par défaut, utilise trial-division
            result = factorize_using_trial_division(n)

        # Ajouter les informations communes
        result['number'] = n
        result['execution_time'] = time.time() - start_time

        # Sauvegarder dans la base locale si succès
        if result.get('success'):
            save_to_local_db(result)

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }