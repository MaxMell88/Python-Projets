"""
prime_sieve_manager.py
Tento modul poskytuje třídu pro správu generování prvočísel
pomocí segmentovaného síta a jejich ukládání do binárního souboru
(bitmapy).
Obsahuje logiku pro práci se soubory a orchestraci síta.

"""
import math 
import os 
from prime_sieve.PrimeGenerator2 import PrimeGenerator2

from typing import BinaryIO

class PrimeSieveManager:
    DEFAULT_FILE_NAME="primes_bitmap.bin"                                   #výchozí název spouboru 
    DEFAULT_LIMIT= 1_000_000_000                                            #výchozí limit
    SEGMENT_SIZE_NUMBERS=10_000_000                                             #velokost segmentu RAM cca 1.25 MB
    f:BinaryIO
    def __init__(self, file_path:  str =None, limit: int = None ):
        # Pokud není zadána cesta, použijeme výchozí název souboru
        # a umístíme ho do podsložky '_data' pro lepší organizaci.
        if file_path is None:
            self._file_path=os.path.join("D:\\PrimeGen_data",self.DEFAULT_FILE_NAME)
        else:
            self._file_path=file_path
        # pokud není definovyný jiný limit použijeme výchozí    
        if limit is None:
            self._limit=self.DEFAULT_LIMIT
        else:
            self._limit=limit
        
        #Vytvoření instance PrimeGenerator
        self._prime_generator_algo=PrimeGenerator2()
        
        # pomocné proměnne
        self._sqrt_limit=int(math.sqrt(self._limit))                           #limit sita(druhá mocnina základů)
        self._base_primes=[]                                                   #list naplněný prvočísly pro uložení do souboru
        
        #výpočet velikostí bin souboru 
        self._total_bits=self._limit+1
        self._total_bytes= math.ceil(self._total_bits / 8)                     #velikost souboru v Bajtech

        os.makedirs(os.path.dirname(self._file_path) or ".", exist_ok=True)    #zajištění existence složky pro bin

    def _get_bit(self, num: int) -> int:
        """
        Přečte bit pro dané číslo ze souboru.
        Vrací 1, pokud je potenciálně prvočíslo, 0, pokud je složené.
        """
        if not (0 <= num <= self._limit):
            return 0 # Mimo rozsah, považujeme za složené
        byte_idx = num // 8
        bit_in_byte_idx = num % 8
        try:
            with open(self._file_path, 'r+b') as f:
                f.seek(byte_idx)
            byte_val = f.read(1)
            if not byte_val: # End of file or error reading
                return 0
            byte_val = byte_val[0] # Přečteme jeden byte
            return (byte_val >> bit_in_byte_idx) & 1
        except IOError as e:
                print(f"Chyba při čtení bitu pro číslo {num} ze souboru:{e}")
                return 0 # Při chybě předpokládáme složené
    
    def _set_bit(self, num: int, value: int):
        if not (0<= num < self._limit):                                        #Kontrtola rozsahu pro num v limit
            return
        byte_index          = num // 8                                                   #pozice Byte
        bit_in_byte_index   = num % 8                                                     #pozice bite
        try:
            with open(self._file_path, 'r+b') as f:
                f.seek(byte_index)
                current_byte=f.read(1)
                if not current_byte:
                    return                                              #chyba čtení
                current_byte=current_byte[0]
                if value == 0:
                    new_byte= current_byte & ~(1 << bit_in_byte_index)
                else:
                    new_byte= current_byte |(1 << bit_in_byte_index)
                    f.seek(byte_index)
                    f.write(bytes([new_byte]))
        except IOError as e:
            print(f"chyba pro nastavení bitu {num} v souboru {e}")                    
      
    def _initialize_bitmap_file(self):                                        #vytvoři a upravi soubor pro prvočísla (binarní sito)
        try:
            with open(self._file_path, "wb") as f:
                for _i in range(self._total_bytes):
                    f.write(b"\xFF")

                #nutno předělat a předat správu do user interface 
                print(f"Soubor s bitmapou '{self._file_path}' \n inicializován na velikost: {self._total_bytes / (1024*1024):.2f} MB.")
                if 0 <= self._limit:
                    self._set_bit(0,0)

                 #možná zbytečná podmínka    
                if 1<=self._limit:
                    self._set_bit(1,0)                                        # nastaví bit pro jedna na 0 ne prvočíslo

                if 2<= self._limit:
                    self._set_bit(2,1)                                         #nastavi 2 na prvočíslo (1)
        
        # zachycení výjímky 
        except IOError as e: 
            raise RuntimeError(f"Chyba{e} při načítání  {self._file_path}")
            
    # generujme prvočilsa do souboru f po limit 

    def generate_primes_to_f(self):
        # Krok 1: Inicializujeme soubor s bitmapou
        print(f"Spouštím generování prvočísel až do {self._limit:,} do souboru: {self._file_path}")

        self._initialize_bitmap_file()
        # Krok 2: Vygenerujeme základní prvočísla (až do sqrt(limit)) Používáme statickou metodu z PrimeGeneratoru
        self._base_primes=self._prime_generator_algo.sieve_up_to_limit(self._sqrt_limit)
        print(f"základní prvočílsa vygenrovaná až po {self._sqrt_limit}")
        print(f"Seznam obsahuje: {len(self._base_primes)} prvočísel")
        #Krok 3 Zpracuijem segmenty a označime složená čisla v souboru 
        # Začiname od 0 protože mark_composites umí zpracovat čísla 0 1 2 
        current_segment_start_num=0
        
        while current_segment_start_num<=self._limit:
            current_segment_end_num= min(current_segment_start_num + self.SEGMENT_SIZE_NUMBERS - 1, self._limit)
        
            # Vypočítáme rozsah bytů, které tento segment pokrývá
            # Segment začíná od bitu 'current_segment_start_num
            segment_start_byte_idx = current_segment_start_num // 8
            segment_end_byte_idx   = current_segment_end_num //8
            # Potřebujeme přečíst byty, které tyto bity obsahují
            # Pokud koncový bit spadá do dalšího bytu, musíme přečísti ten
            # # Zajištěníže segment_end_byte_idx nepřekročí celkový počet bytů v souboru
            segment_end_byte_idx = min(segment_end_byte_idx, self._total_bytes - 1)

            # Přečteme segment do paměti jako bytearray

            segment_bytearray = bytearray()
            try:
                with open(self._file_path, 'r+b') as f:
                    f.seek(segment_start_byte_idx)
                    bytes_to_read = segment_end_byte_idx - segment_start_byte_idx +1
                    segment_bytearray.extend(f.read(bytes_to_read))
        
            except IOError as e: 
                print(f"Chyba při čtení segmentu ze souboru ({current_segment_start_num:,}-{current_segment_end_num:,}): {e}")
                current_segment_start_num += self.SEGMENT_SIZE_NUMBERS                 
                continue         # Přeskočit na další segment při chybě
        # Zavoláme PrimeGenerator pro označení složených čísel v tomto segmentu.
        # Důležité: 'mark_composites_in_segment' potřebuje vědět, jaká čísla
        # skutečně reprezentuje 'segment_bytearray'.
        # První číslo reprezentované 'segment_bytearray' je'segment_start_byte_idx * 8'.
        # Poslední číslo je '(segment_end_byte_idx + 1) * 8 - 1'.
            actual_segment_start_num_for_sieve =segment_start_byte_idx * 8 
            actual_segment_end_num_for_sieve = min((segment_end_byte_idx + 1) * 8 - 1, self._limit)

            self._prime_generator_algo.mark_composites_in_segment (
            segment_bytearray,actual_segment_start_num_for_sieve,
            actual_segment_end_num_for_sieve,self._base_primes 
            )
        # Zapíšeme modifikovaný segment zpět do souboru
            print(f"\n Zapisují... do {self._file_path}")
            try:
                with open(self._file_path, 'r+b') as f:
                    f.seek(segment_start_byte_idx)
                    f.write(segment_bytearray)
                    print("....hotovo")
            except IOError as e:
                print(f"Chyba při zápisu segmentu do souboru ({current_segment_start_num:,}-{current_segment_end_num:,}): {e}")
            print(f"Zpracován segment: {current_segment_start_num:,} až {current_segment_end_num:,}")
            current_segment_start_num += self.SEGMENT_SIZE_NUMBERS
        print(f"Generování prvočísel do souboru '{self._file_path}'dokončeno.")

    def get_limit(self) -> int:
        """
        Vrátí aktuální limit, pro který je manažer nastaven.
        """
        return self._limit
    def set_limit(self, new_limit: int):
        
        """
        Nastaví nový limit pro generování prvočísel.
        Tím se resetuje stav manažera a bude nutné znovu spustit generování.
        Args:
            new_limit (int): Nový horní limit. Předpokládá se, že je to celé číslo >= 2.
        """
        if new_limit != self._limit:
            self._limit = new_limit
            self._sqrt_limit = int(math.sqrt(self._limit))
            self._base_primes = []
            self._total_bits = self._limit + 1
            self._total_bytes = math.ceil(self._total_bits / 8)
            # Soubor bude inicializován při dalším volání generate_primes_to_file()
    def reset_limit_to_default(self):
        """
        Nastaví limit manažera na výchozí hodnotu (DEFAULT_LIMIT).
        """
        self.set_limit(self.DEFAULT_LIMIT)

    def is_prime(self, num: int) -> bool:    
        """
        Zkontroluje, zda je číslo prvočíslo, čtením z bitmapy.
        Args:
        num (int): Číslo ke kontrole.
        Returns:
        bool: True, pokud je číslo prvočíslo, jinak False.
        """
        if num < 2:
            return False
        if num > self._limit:
            return False 
        # Mimo rozsah generovaného síta
        # Pro čísla <= sqrt_limit můžeme pro rychlost zkontrolovat _base_primes.
        # Předpokládá se, že generate_primes_to_file() bylo spuštěno.
        if num <= self._sqrt_limit:
            return num in self._base_primes
        # Pro větší čísla čteme z binárního souboru.
        return self._get_bit(num) == 1
    def get_nth_prime(self, n: int) -> int | None:
        """
            Najde N-té prvočíslo iterací přes bitmapu.
            Tato metoda může být pomalá pro velmi velké N, protože
            vyžaduje lineární procházení.
            """
             #stvělý postřeh!!!
        """ Args:
            n (int): Pořadí hledaného prvočísla (např. 1 pro první, 2 pro druhé).
            Returns:
            int | None: N-té prvočíslo, nebo None, pokud N-té
            prvočíslo není nalezeno
            v rámci aktuálního limitu.
            """
        for p in self._base_primes:
            prime_count += 1
            if prime_count == n:
                return p
        # Pokud N-té prvočíslo nebylo mezi základními, pokračujeme v hledání v souboru.
        # Začneme hledat od čísla, které je hned po posledním základním prvočísle,
        # nebo od 3, pokud základní prvočísla nejsou.
        start_search_num = self._base_primes[-1] + 1  if self._base_primes else 3

        if start_search_num % 2 == 0 and start_search_num > 2: 
            # Zajistíme, že začínáme od lichého čísla, pokud > 2
            start_search_num += 1
            # Iterujeme přes soubor v segmentech, abychom spočítali prvočísla.
            # Začínáme od čísla, které je násobkem 8 a je menší nebo rovno start_search_num,
            # abychom správně zarovnali čtení bytů.
        current_segment_start_num = (start_search_num // 8) * 8
        while current_segment_start_num <= self._limit:
            current_segment_end_num = min(current_segment_start_num + self.SEGMENT_SIZE_NUMBERS - 1, self._limit)
            # Vypočítáme rozsah bytů k přečtení pro tento segment
            segment_start_byte_idx = current_segment_start_num // 8
            segment_end_byte_idx = math.ceil((current_segment_end_num+ 1) / 8) - 1
            segment_end_byte_idx = min(segment_end_byte_idx,
            self._total_bytes - 1)
            segment_bytearray = bytearray()
            try: 
                with open(self._file_path, 'rb') as f:
                    f.seek(segment_start_byte_idx)
                    bytes_to_read = segment_end_byte_idx - segment_start_byte_idx + 1 
                    segment_bytearray.extend(f.read(bytes_to_read))
            except IOError as e:
                print(f"Chyba při čtení segmentu pro get_nth_prime: {e}")
                current_segment_start_num += self.SEGMENT_SIZE_NUMBERS
                continue
            # Iterujeme přes čísla v tomto segmentu (reprezentovaná bity v bytearray)
            actual_segment_start_num_in_bytearray = segment_start_byte_idx * 8

            for i in range(len(segment_bytearray) * 8):                         # Projdeme všechny bity v bytearray
                num_in_segment = actual_segment_start_num_in_bytearray + i
                if num_in_segment > self._limit: # Zastavíme, pokud překročíme celkový limit
                    return None
                if num_in_segment < start_search_num: # Přeskočíme čísla před naším startem hledání
                    continue
                byte_idx = i // 8
                bit_in_byte_idx = i % 8
                # Zkontrolujeme, zda je bit nastaven (tj. číslo je prvočíslo)
                if (segment_bytearray[byte_idx] >> bit_in_byte_idx) & 1:
                    prime_count += 1
                    if prime_count == n:
                        return num_in_segment
            current_segment_start_num += self.SEGMENT_SIZE_NUMBERS
        return None # N-té prvočíslo nebylo nalezeno v rámci limitu
