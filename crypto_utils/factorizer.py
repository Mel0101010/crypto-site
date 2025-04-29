"""
Module de factorisation de nombres
"""

import math
import time

def factorize_number(number, options=None):
    """
    Factorise un nombre en ses facteurs premiers (version minimale).
    
    Args:
        number (str): Le nombre à factoriser
        options (dict): Options de factorisation (non utilisées dans cette version)
            
    Returns:
        dict: Résultat de la factorisation
    """
    start_time = time.time()
    
    try:
        # Convertir l'entrée en entier
        n = int(number.strip())
        if n <= 1:
            return {
                'success': False,
                'error': 'Le nombre doit être supérieur à 1',
                'execution_time': time.time() - start_time
            }
            
        # Version minimale: division par essai
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
            
        result = {
            'success': True,
            'number': int(number),
            'factors': factors,
            'execution_time': time.time() - start_time
        }
        
    except Exception as e:
        result = {
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }
        
    return result
