import math
import time


class PrimeGenerator:
    def __init__(self, limit: int):

        if not isinstance(limit, int) or limit <2:
            raise ValueError("Limit musí byt celé čislo větší než 2")

        self.limit= limit           #limit vyhledávání
        self._primes = []           #pole prvočisel
        self._is_sieve_run=False    #Flag_ bylo již spoštěno?



    def _run_sive(self):
        if self._is_sieve_run:
            print("Sito již běželo")
            return
        print("Start pro limit", self.limit)
        _is_prime_array= [True] * (self.limit + 1)
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
        print("Sito dokončeno! Nalezeno:",len(self._primes),"prvočisel \n nejvetší nalezene prvočíslo je:", self._primes[(len(self._primes)-1)])
        return self._primes
    
    def get_nth_prime(self, n : int):

        if not self._is_sieve_run:
            self._run_sive()

        if n<=0:
            raise ValueError("index musí byt větší než 0")
        if n- 1 < len(self._primes):

            return self._primes[n-1]
        else:
            print("Limit neni dostatečně velky proé nalezeni Nteho prvočisla")
            return None

    def _is_prime(self, num : int) -> bool:
        if not self._is_sieve_run:
            self._run_sive()
        if num <0 or num > self.limit:
            return False    

def measure_time(func, *args, **kwargs):

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return result, duration
