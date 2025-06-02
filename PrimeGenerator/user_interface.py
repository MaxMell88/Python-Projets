"""
Třída pro správu uživatelského rozhraní aplikace

User_interface.py
Tento modul definuje třídu User_interface, která se stará o veškerou
interakci s uživatelem (vstup, výstup, menu).

Obsahuje:
- Třídy:
- User_interface: Zapouzdřuje logiku uživatelského rozhraní.
Příklady importu:

from User_interface import User_interface
"""
# Importujeme potřebné moduly a třídy které máme k dispozici 

import keyboard

from PrimeGenerator import PrimeGenerator
from funkce import measure_time

class User_interface:
    def __init__(self):
        self.prime_generator=PrimeGenerator()
        self.display_intro()
        self.setup_generator_limit()


    def display_intro(self):
        print("\n"+"="*100)
        print("=-- Vítejte v aplikaci pro práci s prvočísly  "
              "\n=-- Tato aplikace generuje prvočísla pomocí Eratosthenova síta" \
              "\n=-- a umožnuje s nimi provádět různe oparace ")
        print("\n"+"="*100)

    def _get_integer_input(self, prompt: str, min_value: int = None) ->int:
        while True:
            try:
                value_str=input(prompt).strip()
                value =int(value_str)
                if min_value is not None and value < min_value:
                    print(f"Vstup musí být vetší než{min_value}.")
                else:
                    return value
            except ValueError:
                print(f"Chyba vstupu, zadejte cele číslo vetší než {min_value}")

    def _get_yes_no_input (self, prompt: str)   ->bool:
        while True:
            user_input=input(f"{prompt}=---> (Y/N): ").strip().upper()
            if user_input=="Y":
                return True
            if user_input =="N":
                return False
            else:
                print(f"=--- zadejte platny vstup (Y/N:)")

    def setup_generator_limit(self):
        
        print(f"=--- Počateční nastavení generatoru prvočísel:",self.prime_generator.ACT_LIMIT)
        
        use_default= self._get_yes_no_input("=--- Chete použít výchozí limit? ")
        if use_default:
            self.prime_generator.set_limit(self.prime_generator.DEF_LIMIT)
        else:
            new_limit=self._get_integer_input(f"=--- Zasdejte horní limit pro generovaní prvočísel:\n")
            self.prime_generator.set_limit(new_limit)
        #spustime sito hned?
        if self._get_yes_no_input(f"=---Chcete spustit generovaní prvočísel s limitem - {self.prime_generator.ACT_LIMIT}"):
            _, run_sief_duration = measure_time(self.prime_generator._run_sive)
            print("=--- Prvočisla připravene s limitem:",self.prime_generator.get_limit(),"\n=--- Trvalo to ",run_sief_duration,"sekund")
            print(f"=---Nejvetší nalezené prvočíslo je:",self.prime_generator._primes[len(self.prime_generator._primes)-1])
            print(f"=--- Celekem bylo nalezono {len(self.prime_generator._primes)} prvočísel")
            print("\n"+"="*100)
        else:
            print(f"=--- Nastavení generatoru: \n=--- Hormní limit prvočísel je: {self.prime_generator.ACT_LIMIT}")
            if self.prime_generator._is_sieve_run:
                print(f"=--- Sito nebylo spuštěné")
                print("\n"+"="*100)
            else:        
                print(f"=--- Sito již bylo spuštěné, s limitem {self.prime_generator.ACT_LIMIT}")
                print("\n"+"="*100)

    def display_main_menu(self):
        print("\n=--- Hlavní Menu ---")
        print(f"=--- Aktuální limit generátoru:{self.prime_generator.get_limit()}")
        print("=--- 1. Spustit generování prvočísel (síto)")
        print("=--- 2. Změnit limit generátoru")
        print("=--- 3. Nastavit limit na výchozí")
        print("=--- 4. Zobrazit N-té prvočíslo")
        print("=--- 5. Zkontrolovat, zda je číslo prvočíslo")
        print("=--- 6. Ukončit aplikaci")
        print("="*100)
    def get_nth_prime_action(self):
        #ziskaní Nteho P v sezanmu
       
        _NinP=self._get_integer_input("=--- Zadejte pořadí prvočisla N:",min_value=1)
        #Test na vyýtup
        try:
            _nth_NinP_result, _nth_NinP_duration = measure_time(self.prime_generator.get_nth_prime, _NinP)
            if _nth_NinP_result is not None:
                print(f"=--- {_NinP} prvočíslo v pořadí je {_nth_NinP_result}")
                print(f"=--- trvalo to {_nth_NinP_duration:.6f} s")
            else:
                print(f"=--- Limit sita {self.prime_generator.get_limit()} neni dostatečný po nalezni {_NinP} prvočísla v seznamu. Zvěčte limit")
        except RuntimeError as e:
                print("Prosím, nejprve spusťte generování prvočísel")
                print("-" * 50)

    def _check_primality_acton(self):
        try:
            num_to_check=self._get_integer_input("=--- Zadejte čilso ke kontrole:", min_value=0)
            #je n prvočíslo?
            _is_n_prime, duration_is_n_prime=measure_time(self.prime_generator._is_prime,num_to_check)
            if num_to_check> self.prime_generator.get_limit():
                print(f"=--- {num_to_check} je vetší než {self.prime_generator.get_limit()} limit sita které bylo spuštěné.")
                print(f"=--- Je potřba spustit sito s vyšším limitem")
            else:
                print(f"=--- {num_to_check} Je prvočíslo?:{_is_n_prime}")
                print(f"=--- Akce trvala: {duration_is_n_prime} sekud")
        except RuntimeError as e:
                print(f"=--- Chyba {e}\n=--- Spuisťe generator prvočísle (síto)")

    def run(self):
        while True:
            self.display_main_menu()
            choise=self._get_integer_input("=--- Vaše volba?:\n")
            if choise==1:
                self.prime_generator._run_sive()
            
            elif choise == 2:
                self.setup_generator_limit()

            elif choise == 3:
                self.prime_generator.set_limit(self.prime_generator.DEF_LIMIT)
                print(f"=--- Limit přenastaven na výchozi honotu {self.prime_generator.DEF_LIMIT} (1000,000 prvočísel)")

            elif choise == 4:
                self.get_nth_prime_action()

            elif choise == 5:
                self._check_primality_acton()

            elif choise == 6:
                break
            else:
                print("=--- Neplatna volba. Běželo sito?:",{self.prime_generator._is_sieve_run})
                         

            





        


                     


