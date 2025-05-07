"""
Module de factorisation de nombres
"""
import math
import time
import random
from factordb.factordb import FactorDB

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

def factorize_using_pollard_rho(n):
    """Implémentation de l'algorithme Rho de Pollard"""
    if n % 2 == 0:
        return {
            'success': True,
            'factors': [2] + factorize_number(n // 2, "pollard-rho")['factors'],
            'source': 'Pollard Rho'
        }

    factors = []

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
        if is_prime(d):
            return d
        else:
            # Si d n'est pas premier, on le factorise récursivement
            return find_factor(d)

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

    def get_all_factors(n):
        if n == 1:
            return []

        factor = find_factor(n)
        if factor == n:
            return [factor]

        return sorted(get_all_factors(factor) + get_all_factors(n // factor))

    try:
        # Obtenir tous les facteurs
        factors = get_all_factors(n)
        if not factors:
            factors = [n]

        return {
            'success': True,
            'factors': factors,
            'source': 'Pollard Rho'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur lors de l'exécution de Pollard Rho: {str(e)}"
        }

def factorize_using_quadratic_sieve(n):
    """Version simplifiée du crible quadratique"""
    try:
        # Implémentation simplifiée du crible quadratique
        # Pour une vraie implémentation, on utiliserait une bibliothèque comme sympy

        # Vérifier si n est pair
        if n % 2 == 0:
            return {
                'success': True,
                'factors': [2] + factorize_number(n // 2, "quadratic-sieve")['factors'],
                'source': 'Crible quadratique'
            }

        # Base des facteurs premiers (B-smooth)
        B = 100
        factor_base = []
        for p in range(2, B):
            if is_prime_q(p) and legendre_symbol(n, p) == 1:
                factor_base.append(p)

        # Recherche de relations
        relations = []
        x = int(math.sqrt(n)) + 1
        while len(relations) < len(factor_base) + 10 and x < n:
            q = (x * x) % n
            if is_bsmooth(q, factor_base):
                relations.append((x, q))
            x += 1

        # Résolution du système linéaire et factorisation
        for i in range(len(relations)):
            for j in range(i+1, len(relations)):
                x1, q1 = relations[i]
                x2, q2 = relations[j]

                # Si q1*q2 est un carré parfait
                if is_perfect_square(q1 * q2):
                    # Calculer le carré parfait
                    y = int(math.sqrt(q1 * q2))

                    # Calculer les potentiels facteurs
                    a = (x1 * x2) % n
                    factor = gcd(abs(a - y), n)

                    if 1 < factor < n:
                        # Facteur trouvé
                        return {
                            'success': True,
                            'factors': sorted(factorize_number(factor, "trial-division")['factors'] +
                                              factorize_number(n // factor, "trial-division")['factors']),
                            'source': 'Crible quadratique'
                        }

        # Si pas de facteurs trouvés, retourner le nombre lui-même
        return {
            'success': True,
            'factors': [n],
            'source': 'Crible quadratique'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Erreur lors de l'exécution du crible quadratique: {str(e)}"
        }

def is_prime_q(n):
    """Test de primalité rapide"""
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

def factorize_number(number, method=None):
    """
    Factorise un nombre en ses facteurs premiers.

    Args:
        number (str): Le nombre à factoriser
        method (str): Méthode de factorisation

    Returns:
        dict: Résultat de la factorisation
    """
    start_time = time.time()
    try:
        n = int(number.strip())
        if n <= 1:
            return {
                'success': False,
                'error': 'Le nombre doit être supérieur à 1',
                'execution_time': time.time() - start_time
            }

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

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }