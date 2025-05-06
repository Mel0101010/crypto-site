"""
Module de factorisation de nombres
"""
import math
import time
from factordb.factordb import FactorDB

def factorize_number(number, options=None):
    """
    Factorise un nombre en ses facteurs premiers.
    
    Args:
        number (str): Le nombre à factoriser
        options (dict or str): Options de factorisation, "factor-db" pour utiliser FactorDB
        
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
        
        if options == "factor-db":
            f = FactorDB(n)
            f.connect()
            factor_data = f.get_factor_list()
            
            # Vérifier si la factorisation est complète
            if f.get_status() == "FF":  # FF = "fully factored"
                return {
                    'success': True,
                    'number': n,
                    'factors': factor_data,
                    'source': 'FactorDB',
                    'execution_time': time.time() - start_time
                }
        
        # Version par défaut: division par essai
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
            'source': 'division par essai',
            'execution_time': time.time() - start_time
        }
        
        return result
        
    except Exception as e:
        result = {
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }
        return result