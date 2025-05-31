import time
import math
# --- Pomocná funkce pro měření času ---
def measure_time(func, *args, **kwargs):
#Pomocná funkce pro měření času běhu dané funkce.  Používá time.perf_counter() pro přesnější měření.

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time    
    return result, duration
# --- Algoritmus 1: is_prime_trial_division (Zkoušení dělitelů pro
#jedno číslo) ---
# Toto je tvůj původní algoritmus pro kontrolu prvočíselnosti,
#optimalizovaný pro jedno číslo.
# Jeho složitost je O(sqrt(n)).
def is_prime_trial_division(num: int) -> bool:
#
#Testuje, zda je číslo prvočíslo, pomocí zkoušení dělitelů.
#
    if num <= 1:
        return False
    if num <= 3: # 2 a 3 jsou prvočísla
        return True
    if num % 2 == 0 or num % 3 == 0:
     # Vyloučí násobky 2 a 3
        return False
# Kontroluje dělitele ve tvaru 6k +/- 1
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
    i += 6
    return True
# --- Algoritmus 2: Sieve of Eratosthenes (Eratosthenovo síto) ---
# Tento algoritmus je mnohem efektivnější pro nalezení VŠECH prvočísel
#do určitého limitu.
# Jeho složitost je O(N log log N).
def sieve_of_eratosthenes(limit: int) -> list[int]:

#Nalezne všechna prvočísla až do zadaného limitu pomocí
#Eratosthenova síta.

 if limit < 2:

    return []
# Vytvoří boolean seznam 'is_prime', kde is_prime[i] je True,pokud je i prvočíslo
    is_prime = [True] * (limit + 1)
    is_prime[0] = False # 0 není prvočíslo
    is_prime[1] = False # 1 není prvočíslo
# Začneme od 2
    p = 2
    while p * p <= limit:
# Pokud je is_prime[p] stále True, pak p je prvočíslo
        if is_prime[p]:
# Vyškrtneme všechny násobky p (začínáme od p*p, protožemenší násobky
# už byly vyškrtnuty dřívějšími prvočísly)
         for multiple in range(p * p, limit + 1, p):

            is_prime[multiple] = False
    p += 1 # Posun na další číslo
# Shromáždíme všechna prvočísla
    primes = [num for num, prime_status in enumerate(is_prime) if prime_status]
    return primes


# --- Hlavní část pro spuštění a porovnání ---
    if __name__ == "__main__":
        print("--- Porovnání algoritmů pro prvočísla ---")
# Příklad 1: Testování jednoho velkého čísla pomocí Trial Division
# Toto je scénář, pro který je Trial Division relativně rychlá.
    test_number_single = 15_485_863 # Tvé nalezené prvočíslo
    print(f"\nTestování prvočíselnosti jednoho čísla({test_number_single}) pomocí Trial Division:")
    is_prime_result, duration_single_td =measure_time(is_prime_trial_division, test_number_single)
    print(f"Je {test_number_single} prvočíslo? {is_prime_result}")
    print(f"Trvalo to: {duration_single_td:.6f} sekund.")

# Očekávaný výsledek: velmi rychlé (zlomky milisekundy).
# Příklad 2: Nalezení VŠECH prvočísel do určitého limitu pomocí Eratosthenova síta
# Toto je scénář, pro který je Síto navrženo a je extrémně efektivní.
    limit_sieve = 15_485_863 # Tvůj limit, pro který jsi měl/a dlouhývýpočet
    print(f"\nNalezení VŠECH prvočísel do {limit_sieve} pomocí Eratosthenova síta:")
    primes_found_sieve, duration_sieve =measure_time(sieve_of_eratosthenes, limit_sieve)
    print(f"Nalezeno {len(primes_found_sieve)} prvočísel.")
    print(f"Trvalo to: {duration_sieve:.6f} sekund.")
# Očekávaný výsledek: Čas by měl být podobný tvému původnímu 137sekundám,
# protože síto efektivně dělá to, co tvůj původní kód dělalneefektivně.
# Příklad 3: Porovnání Trial Division pro rozsah (jen pro menšílimit, protože je pomalé)
# Zde uvidíš, proč se Trial Division nepoužívá pro nalezení všechprvočísel v rozsahu.
    limit_small_range_td = 100_000
    print(f"\nNalezení VŠECH prvočísel do {limit_small_range_td} pomocí opakované Trial Division:")
    primes_found_td_range = []
    start_time_td_range = time.perf_counter()
    for num in range(2, limit_small_range_td + 1):
        if is_prime_trial_division(num):
            primes_found_td_range.append(num)
    end_time_td_range = end_time_td_range - start_time_td_range
    print(f"Nalezeno {len(primes_found_td_range)} prvočísel.")
    print(f"Trvalo to: {duration_td_range:.6f} sekund.")
# Očekávaný výsledek: I pro 100 000 je to znatelně pomalejší nežSíto pro 15 milionů.
# Kód pro 15 milionů by zde trval hodiny/dny, proto honespouštíme