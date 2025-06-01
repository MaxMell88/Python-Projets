import time
import math
# --- Pomocná funkce pro měření času ---
def measure_time(func, *args, **kwargs):

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return result, duration

def is_prime_trial_division(num: int) -> bool:

    if num <= 1:
        return False
    if num <= 3: # 2 a 3 jsou prvočísla
        return True
    if num % 2 == 0 or num % 3 == 0: # Vyloučí násobky 2 a 3
        return False
# Kontroluje dělitele ve tvaru 6k +/- 1
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

# --- Algoritmus 2: Sieve of Eratosthenes (Eratosthenovo síto)
def sieve_of_eratosthenes(limit: int) -> list[int]:
    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)
    is_prime[0] = False # 0 není prvočíslo
    is_prime[1] = False # 1 není prvočíslo

    p = 2
    while p * p <= limit:
                            # Pokud je is_prime[p] stále True, pak p je prvočíslo
        if is_prime[p]:     # Vyškrtneme všechny násobky p (začínáme od p*p, protože menší násobky už byly vyškrtnuty dřívějšími prvočísly)

            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
        p += 1                  # Posun na další číslo    

    primes = [num for num, prime_status in enumerate(is_prime) if   prime_status]
    return primes

if __name__ == "__main__": # Příklad 1: Testování jednoho velkého čísla pomocí Trial Division
    test_number_single = 15_485_863 # nalezené prvočíslo
    print(f"\nTestování prvočíselnosti jednoho čísla({test_number_single}) pomocí Trial Division:")
    is_prime_result, duration_single_td = measure_time(is_prime_trial_division, test_number_single)
    print(f"Je {test_number_single} prvočíslo? {is_prime_result}")
    print(f"Trvalo to: {duration_single_td:.6f} sekund.")

    limit_sieve = 15_485_863 

    print(f"\nNalezení VŠECH prvočísel do {limit_sieve} pomocí Eratosthenova síta:")
    primes_found_sieve, duration_sieve =measure_time(sieve_of_eratosthenes, limit_sieve)
    print(f"Nalezeno {len(primes_found_sieve)} prvočísel.")
    print(f"Trvalo to: {duration_sieve:.6f} sekund.")

    limit_small_range_td = 100_000
    print(f"\nNalezení VŠECH prvočísel do {limit_small_range_td} pomocí opakované Trial Division:")
    primes_found_td_range = []
    start_time_td_range = time.perf_counter()
    for num in range(2, limit_small_range_td + 1):
        if is_prime_trial_division(num):
            primes_found_td_range.append(num)
    end_time_td_range=time.perf_counter()
    duration_td_range = end_time_td_range - start_time_td_range
    print(f"Nalezeno {len(primes_found_td_range)} prvočísel.")
    print(f"Trvalo to: {duration_td_range:.6f} sekund.")


