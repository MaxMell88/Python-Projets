import time

def measure_time(func , *args, **kwargs):

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return result, duration




"""
funkce.py

Tento modul obsahuje obecné pomocné funkce, které mohou být použity
napříč různými částmi projektu, včetně měření času a systémových informací.
"""

import time
import math
import sys

try:
    import psutil
except ImportError:
    psutil = None
    print("Upozornění: Knihovna 'psutil' není nainstalována. Funkce pro kontrolu RAM nebudou dostupné.")
    print("Pro instalaci spusťte: pip install psutil")


def measure_time(func, *args, **kwargs):
    """
    Pomocná funkce pro měření času běhu dané funkce.
    Používá time.perf_counter() pro přesnější měření.

    Args:
        func (callable): Funkce, jejíž běh se má měřit.
        *args: Pozicní argumenty předané funkci.
        **kwargs: Klíčové argumenty předané funkci.

    Returns:
        tuple: Dvojice (výsledek_funkce, doba_trvani_v_sekundach).
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return result, duration

def get_available_ram_bytes() -> int | None:
    """
    Vrátí množství dostupné RAM v bajtech.
    Vyžaduje knihovnu psutil.

    Returns:
        int | None: Dostupná RAM v bajtech, nebo None, pokud psutil není dostupné.
    """
    if psutil:
        return psutil.virtual_memory().available
    return None

def estimate_sieve_memory_bytes(limit: int) -> int:
    """
    Odhadne paměť potřebnou pro Eratosthenovo síto pro daný limit.
    Zahrnuje paměť pro boolean pole (is_prime_array) a seznam prvočísel (_primes).
    Používáme konzervativní odhad pro Python list[bool] (cca 8 bajtů na prvek)
    a pro list[int] (cca 28 bajtů na prvek).

    Args:
        limit (int): Horní limit pro síto.

    Returns:
        int: Odhadovaná paměť v bajtech.
    """
    if limit < 2:
        return 0

    # Odhad paměti pro is_prime_array (list booleans)
    # Python booleany jsou objekty, list je pole pointerů.
    # sys.getsizeof(True) je 28 bajtů, ale list[bool] je efektivnější.
    # Konzervativní odhad: ~8 bajtů na prvek pro list booleans
    sieve_array_memory = (limit + 1) * 8 # Rough estimate for list of bools

    # Odhad paměti pro _primes list (list integers)
    # Počet prvočísel do limitu (Prime-counting function approximation: pi(x) ~ x / ln(x))
    # sys.getsizeof(0) je 24 bajtů, větší inty jsou 28 bajtů.
    num_primes_approx = limit / math.log(limit) if limit > 1 else 0
    primes_list_memory = int(num_primes_approx * 28) # Rough estimate for list of ints

    return sieve_array_memory + primes_list_memory

def calculate_recommended_max_sieve_limit(available_ram_bytes: int, safety_factor: float = 0.7) -> int:
    """
    Vypočítá doporučený maximální limit pro síto na základě dostupné RAM.
    Používá bezpečnostní faktor, aby nezabíralo veškerou paměť.

    Args:
        available_ram_bytes (int): Dostupná RAM v bajtech.
        safety_factor (float): Faktor (0.0 - 1.0) pro rezervu paměti.

    Returns:
        int: Doporučený maximální limit, nebo malá hodnota pokud RAM je nízká.
    """
    if available_ram_bytes is None or available_ram_bytes <= 0:
        return 1_000_000 # Nízký výchozí limit, pokud RAM nelze zjistit

    # Využitelná paměť pro síto
    usable_ram_for_sieve = available_ram_bytes * safety_factor

    # Odhad paměti na jeden "prvočíselný slot" v síťovém poli (cca 8 bajtů)
    # Plus malý odhad na uložení prvočísel
    # Toto je velmi hrubý odhad, reálná spotřeba je složitější.
    # Pro jednoduchost budeme předpokládat, že 1 číslo v síťovém poli zabere ~8 bajtů
    # a zbytek paměti je pro seznam prvočísel.
    # Zde je to zjednodušeno na to, že limit je zhruba (použitelná RAM / 8)
    # Pro přesnější odhad by se musela řešit inverzní funkce estimate_sieve_memory_bytes.
    # Pro účely bezpečného limitu je lepší být konzervativní.
    
    # Hrubý odhad: 100M limit je ~800MB pro pole, ~1.4GB pro seznam. Celkem ~2.2GB.
    # Pokud máme 8GB RAM, 70% je 5.6GB.
    # 5.6GB / 2.2GB/100M = ~250M limit.
    # Zjednodušený odhad: limit = usable_ram_for_sieve / (průměrná_paměť_na_číslo)
    # Průměrná paměť na číslo je složitá, protože závisí na hustotě prvočísel.
    # Vezměme si, že hlavní pole je ~8 bajtů/číslo.
    
    # Pro jednoduchost a bezpečnost:
    # Zkusíme najít limit iterativně nebo použijeme velmi konzervativní lineární odhad.
    # Pokud 100M čísel zabere ~2.2GB, pak 1 bajt na číslo je příliš optimistický.
    # 2.2 GB / 100 000 000 = 22 bajtů na číslo v průměru.
    # Takže limit = usable_ram_for_sieve / 22
    
    bytes_per_number_estimate = 22 # Konzervativní odhad bajtů na číslo pro síto + seznam prvočísel
    
    if bytes_per_number_estimate == 0: # Zamezení dělení nulou
        return 1_000_000

    recommended_limit = int(usable_ram_for_sieve / bytes_per_number_estimate)
    
    # Zajistíme, že limit je alespoň 2 a není příliš velký (např. přes int max)
    return max(2, min(recommended_limit, sys.maxsize))