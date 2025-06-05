"""
    prime_generator.py
    Tento modul poskytuje třídu pro algoritmy prvočíselného síta.
    Je navržen tak, aby se staral pouze o logiku síta,
    bez jakékoli přímé interakce se soubory nebo správou stavu generování.
"""
import math

class PrimeGenerator2:
    """
    Třída pro algoritmy síta. Poskytuje statické metody pro generování
    základních prvočísel a pro označování složených čísel v
    segmentech.
    """
    def __init__(self):
        """
        Konstruktor třídy PrimeGenerator.
        Tato třída nyní neudržuje interní stav generování ani limit.    
        """
    pass
    @staticmethod
    def sieve_up_to_limit(limit: int) -> list[int]:
        """
        Generuje prvočísla až do daného limitu pomocí klasického
        Eratosthenova síta.
        Tato metoda je určena pro menší limity, kde se vše vejde do
        paměti.
     Pro segmentové síto se použije jen pro základní prvočísla.
        Args:
        limit (int): Horní limit pro generování prvočísel.
        Returns:
        list[int]: Seznam prvočísel až do 'limit'.
        """
        if limit < 2:
            return
        is_prime_array = [True] * (limit + 1)
        is_prime_array[0] = False
        is_prime_array[1] = False
        p = 2
        while p * p <= limit:
            if is_prime_array[p]:
                for multiple in range(p * p, limit + 1, p):
                    is_prime_array[multiple] = False
            p += 1
        return [num for num, prime_status in enumerate(is_prime_array) if prime_status]
    @staticmethod
    def mark_composites_in_segment(segment_bytearray: bytearray,segment_start_num: int, segment_end_num: int, base_primes: list[int]):
        """
        Označí složená čísla v daném segmentu reprezentovaném
        bytearray.
        Bytearray by mělo být inicializováno tak, že všechny bity jsou
        1 (potenciálně prvočísla).
        Tato metoda modifikuje 'segment_bytearray' na místě.
        Předpokládá, že 'segment_bytearray' reprezentuje čísla od
        'segment_start_num'
        do 'segment_end_num', kde každý bit odpovídá jednomu číslu.
        Bit 0 odpovídá 'segment_start_num', bit 1 odpovídá
        'segment_start_num + 1' atd.
        Args:
        segment_bytearray (bytearray): Bytearray reprezentující
        segment čísel.
        Bude modifikováno na místě.
        segment_start_num (int): Počáteční číslo, které segment
        pokrývá.
        segment_end_num (int): Koncové číslo, které segment
        pokrývá.
        base_primes (list[int]): Seznam základních prvočísel (až
        do sqrt(celkového limitu)),
        kterými se budou označovat
        násobky.
        """
        # Pokud je segment_start_num 0 nebo 1, označíme je jako složená, pokud spadají do segmentu.
        #Tato logika je duplicitní s inicializací bitmapy v PrimeSieveManager,
        # ale je dobré ji mít i zde pro robustnost, pokud by se segment_start_num lišilo.
        if segment_start_num <= 0 <= segment_end_num:
            bit_index = 0 - segment_start_num
            byte_idx = bit_index // 8
            bit_in_byte_idx = bit_index % 8
            if byte_idx < len(segment_bytearray):
                segment_bytearray[byte_idx] &= ~(1 << bit_in_byte_idx)
        if segment_start_num <= 1 <= segment_end_num:
            bit_index = 1 - segment_start_num
            byte_idx = bit_index // 8
            bit_in_byte_idx = bit_index % 8
            if byte_idx < len(segment_bytearray):
                segment_bytearray[byte_idx] &= ~(1 << bit_in_byte_idx)
         # Pro každé základní prvočíslo 'p' označíme jeho násobky v aktuálním segmentu.
        print(f"\n počítam segment :{segment_start_num}") 
        for p in base_primes:
            # Speciální případ: 2 je prvočíslo, ale jeho násobky (sudá čísla) jsou složená.
            # Pokud bychom optimalizovali a ukládali jen lichá čísla, p=2 bychom přeskočili zde.
            # Ale protože ukládáme všechna čísla (bit na číslo), 2 se chová normálně.
            # Nicméně, násobky 2 (kromě 2 samotné) jsou složené.
            # Pokud p je 2 a segment_start_num je 2, pak 2 je prvočíslo.
            # Začneme škrtat od 2*2 = 4.
            # Vypočítáme první násobek 'p', který je větší nebo roven 'segment_start_num'
            # a zároveň větší nebo roven 'p*p' (abychom neškrtali čísla, která už byla ošetřena
            # menšími prvočísly nebo jsou menší než p*p).
                start_multiple = max(p * p, (segment_start_num + p - 1) // p * p)
                    # Iterujeme přes násobky 'p' v rámci segmentu a označujeme je jako složená.
                for multiple in range(start_multiple, segment_end_num + 1,p):
                    # Vypočítáme index bitu v rámci segmentu.
                    bit_index_in_segment = multiple - segment_start_num
                    # Vypočítáme index bytu a pozici bitu v rámci bytu.
                    byte_idx = bit_index_in_segment // 8
                    bit_in_byte_idx = bit_index_in_segment % 8
                    # Zajištění, že jsme v platných mezích bytearray.
                    if byte_idx < len(segment_bytearray):
                        # Nastavíme příslušný bit na 0 (složené číslo).
                        segment_bytearray[byte_idx] &= ~(1 << bit_in_byte_idx)