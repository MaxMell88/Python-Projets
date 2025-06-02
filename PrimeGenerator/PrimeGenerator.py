import math
import time


class PrimeGenerator:
    DEF_LIMIT = 15485863 # Výchozi honota pro 1000,000te prvočíslo 
    ACT_LIMIT=DEF_LIMIT
    


    def __init__(self, limit: int):


        self.limit= limit           #limit vyhledávání
        self._primes = []           #pole prvočisel
        self._is_sieve_run=False    #Flag_ bylo již spoštěno?



    def _run_sive(self):
        
        _is_prime_array = [True] * (self.limit + 1)
        _is_prime_array[0]=False
        _is_prime_array[1]=False

        p=2

        while p*p <= self.limit:
            if _is_prime_array[p]:
                for multiple in range(p * p , self.limit + 1, p):
                    _is_prime_array[multiple]=False

            p+=1



        self._primes = [num for num, prime_status in enumerate(_is_prime_array)  if prime_status] # přepis prvočisel do interního seznamu

        self._is_sieve_run=True
        return self._primes
    
    def get_nth_prime(self, n : int):

        if not self._is_sieve_run:
            self._run_sive()
        if len(self._primes) -1 > n:
             return False
        else:
             return self._primes[n-1]


    def _is_prime(self, _test_num ) -> bool:
           if _test_num in self._primes :
               return True
           else:
               return False
           

    def get_primes (self) -> list[int]:
        return self._primes
    
    def set_limit(self,  _newlmit) ->bool:
        
            self.ACT_LIMIT=_newlmit
        
          
    def get_limit(self) -> int:

        return self.ACT_LIMIT
    
    
        
        


