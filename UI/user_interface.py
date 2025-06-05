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

from prime_sieve.PrimeGenerator import PrimeGenerator
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
            _, run_sieve_duration = measure_time(self.prime_generator._run_sive)
            print("=--- Prvočisla připravene s limitem:",self.prime_generator.get_limit(),"\n=--- Trvalo to ",run_sieve_duration,"sekund")
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
                _, run_sieve_duration = measure_time(self.prime_generator._run_sive)
                print("=--- Prvočisla připravene s limitem:",self.prime_generator.get_limit(),"\n=--- Trvalo to ",run_sieve_duration,"sekund")
                print(f"=---Nejvetší nalezené prvočíslo je:",self.prime_generator._primes[len(self.prime_generator._primes)-1])
                print(f"=--- Celekem bylo nalezono {len(self.prime_generator._primes)} prvočísel")
                print("\n"+"="*100)
                
            
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
                         
    """
    user_interface.py
    Tento modul definuje třídu UserInterface, která se stará o veškerou
    interakci s uživatelem (vstup, výstup, menu).
    Hlavní program (main.py) by měl pouze vytvořit instanci této třídy a
    zavolat její metodu run().
    Obsahuje:
    - Třídy:
    - UserInterface: Zapouzdřuje logiku uživatelského rozhraní.
    Příklady importu:
    from user_interface import UserInterface    
    """
# Importujeme potřebné moduly a třídy
from prime_sieve.prime_sieve_manager import PrimeSieveManager 
from funkce import measure_time, get_available_ram_bytes, calculate_recommended_max_sieve_limit # Pro měření času a kontrolu RAM
class User_interface2:
    """
    Třída pro správu uživatelského rozhraní aplikace pro prvočísla.
    """
    def __init__(self):
        """
        Konstruktor UserInterface.
        Inicializuje instanci PrimeSieveManager. Síto se nespouští
        automaticky.
        """
        #Nyní pracujeme s PrimeSieveManagerem
        self.sieve_manager = PrimeSieveManager()
        self._display_intro() # Zobrazíme úvodní zprávu
        self._setup_initial_generator_limit() # Nastavíme počáteční limit
    def _display_intro(self):
        """Zobrazí úvodní zprávu aplikace."""
        print("\n" + "="*50)
        print("--- Vítejte v Aplikaci pro práci s prvočísly! ---")
        print("Tato aplikace generuje prvočísla pomocí Eratosthenovasíta")
        print("a ukládá je do binárního souboru pro práci s velkými daty.")
        print("="*50 + "\n")
    def _get_integer_input(self, prompt: str, min_value: int = None,
        max_value: int = None) -> int:
        """
        Získá od uživatele platné celé číslo s volitelnou minimální a
        maximální hodnotou.
        Args:
        prompt (str): Text dotazu.
        min_value (int, optional): Minimální povolená hodnota.
        Defaults to None.
        max_value (int, optional): Maximální povolená hodnota.
        Defaults to None.
        Returns:
        int: Platné celé číslo.
        """
        while True:
            try:
                value_str = input(prompt).strip()
                value = int(value_str)
                if min_value is not None and value < min_value:
                    print(f"Vstup musí být alespoň {min_value}.")
                elif max_value is not None and value > max_value:
                    print(f"Vstup nesmí být větší než {max_value:,}.Zkuste menší číslo.")
                else:
                    return value
            except ValueError:
                print("Neplatný vstup. Zadejte prosím celé číslo.")
    def _get_yes_no_input(self, prompt: str) -> bool:
        """
        Získá od uživatele odpověď 'Y' (Ano) nebo 'N' (Ne).
        Opakuje dotaz, dokud není zadán platný vstup.
        Args:
        prompt (str): Text dotazu zobrazený uživateli.
        Returns:
        bool: True pro 'Y', False pro 'N'.
        """
        while True:
            user_input = input(f"{prompt} (Y/N): ").strip().upper()
            if user_input == 'Y':
                return True
            elif user_input == 'N':
                return False
            else:
                print("Neplatný vstup. Zadejte prosím 'Y' pro Ano nebo'N' pro Ne.")
    def _setup_initial_generator_limit(self):
        """
        Nastaví počáteční limit pro manažera prvočísel.
        Umožní uživateli zadat limit nebo použít výchozí.
        """
        print("--- Počáteční nastavení generátoru prvočísel ---")
        available_ram = get_available_ram_bytes()
        recommended_max = None
        if available_ram is not None:
            # Použijeme DEFAULT_LIMIT z PrimeSieveManageru pro výchozí     odhad
            recommended_max = calculate_recommended_max_sieve_limit(available_ram,safety_factor=0.7)
        # Doporučený limit pro síto na disku je mnohem vyšší, ale omezíme ho na rozumnou hodnotu
        # pro zamezení příliš velkých souborů pro testování.
        # Pro reálné použití by recommended_max mohl být mnohem vyšší.
            recommended_max = min(recommended_max, 10_000_000_000) # Omezíme na 10 miliard pro začátek
            print(f"Dostupná RAM: {available_ram / (1024**3):.2f} GB. Doporučený max. limit pro síto: {recommended_max:,}")
        else:
            print("Nelze zjistit dostupnou RAM. Max. limit bude omezen na 1,000,000,000.")
            recommended_max = 1_000_000_000 # Pevný fallback limit (1miliarda)
        use_default = self._get_yes_no_input(f"Chcete použít výchozí limit ({self.sieve_manager.DEFAULT_LIMIT:,})? (Y/N)")
        if use_default:
            self.sieve_manager.reset_limit_to_default()
            print(f"Limit generátoru nastaven na výchozí:{self.sieve_manager.get_limit():,}")   
        else:
            new_limit = self._get_integer_input("Zadejte horní limit pro generování prvočísel (min.2): ",  min_value=2,  max_value=recommended_max )# Nový max_value

            self.sieve_manager.set_limit(new_limit)
            print(f"Limit generátoru nastaven na: {self.sieve_manager.get_limit():,}")
            print("-" * 50)
        if self._get_yes_no_input("Chcete spustit generování prvočísel (síto) nyní? (Y/N)"):
            self._run_sieve_action()
        else:
            print("Síto nebylo spuštěno. Můžete ho spustit z hlavního menu.")
            print("\n"+"="*50)
    def _run_sieve_action(self):
        """
        Spustí generování prvočísel pomocí síta a zobrazí výsledky.
        """
        print(f"\nSpouštím generování prvočísel pro limit {self.sieve_manager.get_limit():,}...")
        try:
        # Voláme generate_primes_to_file() na instanci manažera 
            _i, duration_sieve = measure_time(self.sieve_manager.generate_primes_to_f)
            print(f"Generování síta dokončeno. Prvočísla uložena do '{self.sieve_manager._file_path}'.")
            print(f"Trvalo to: {duration_sieve:.6f} sekund.")
        except RuntimeError as e:
            print(f"Chyba při generování síta: {e}")
            print("-" * 100)
    def _change_limit_action(self):
        """
        Umožní uživateli změnit limit generátoru a nabídne opětovné
        spuštění síta.
        """
        print(f"\nAktuální limit je: {self.sieve_manager.get_limit():,}")
        available_ram = get_available_ram_bytes()
        recommended_max = None
        if available_ram is not None:
            recommended_max = calculate_recommended_max_sieve_limit(available_ram,safety_factor=0.7)
            recommended_max = min(recommended_max, 10_000_000_000) # Omezíme na 10 miliard
            print(f"Dostupná RAM: {available_ram / (1024**3):.2f} GB. \n Doporučený max. limit pro síto: {recommended_max:,}")
       
        else:
            print("Nelze zjistit dostupnou RAM. Max. limit bude omezen na 1,000,000,000.")
            recommended_max = 1_000_000_000 # Pevný fallback limit
            new_limit = self._get_integer_input("Zadejte nový limit pro generování prvočísel (min. 2): ",min_value=2,max_value=recommended_max)
            self.sieve_manager.set_limit(new_limit)
            print(f"Limit generátoru nastaven na: {self.sieve_manager.get_limit():,}")

        if self._get_yes_no_input("Chcete spustit generování prvočísel (síto) s novým limitem? (Y/N)"):
            self._run_sieve_action()
        else:
            print("Síto nebylo spuštěno s novým limitem. Můžete ho spustit z hlavního menu.")
            print("-" * 50)


    def _display_main_menu(self):
        """Zobrazí hlavní menu."""
        print("\n--- Hlavní Menu ---")
        print(f"Aktuální limit generátoru: {self.sieve_manager.get_limit():,}")
        print("1. Spustit generování prvočísel (síto)")
        print("2. Změnit limit generátoru")
        print("3. Nastavit limit na výchozí")
        print("4. Zobrazit N-té prvočíslo")
        print("5. Zkontrolovat, zda je číslo prvočíslo")
        print("6. Ukončit aplikaci")
        print("-" * 50)
    def _get_nth_prime_action(self):
        """Akce pro zobrazení N-tého prvočísla."""
        n_order = self._get_integer_input("Zadejte pořadí prvočísla (N): ", min_value=1)
        try:
            # Voláme get_nth_prime() na instanci manažera
            nth_prime_result, duration_nth_prime =  measure_time(self.sieve_manager.get_nth_prime, n_order)
            if nth_prime_result is not None:
                print(f"\n{n_order}. prvočíslo je: {nth_prime_result:,}") 
                print(f"Měření trvalo: {duration_nth_prime:.6f} sekund.")
            else:
                print(f"\nN-té prvočíslo ({n_order:,}) nebylo nalezeno v rámci limitu {self.sieve_manager.get_limit():,}.")
        except Exception as e: # Zachytíme obecnější chybu pro případ, že soubor nebyl vygenerován
            print(f"Chyba: {e}")
            print("Prosím, nejprve spusťte generování prvočísel (síto).")
            print("-" * 100)
    def _check_primality_action(self):
        """Akce pro kontrolu prvočíselnosti čísla."""
        num_to_check = self._get_integer_input("Zadejte číslo ke kontrole: ", min_value=0)
        try:
            # Voláme is_prime() na instanci manažera
            is_prime_check_result, duration_is_prime_check = measure_time(self.sieve_manager.is_prime, num_to_check)
            if num_to_check > self.sieve_manager.get_limit():
                print(f"Číslo {num_to_check:,} je mimo rozsah ({self.sieve_manager.get_limit():,}), pro který bylo síto spuštěno. Nelze ověřit.")
            else:
                print(f"Je {num_to_check:,} prvočíslo? {is_prime_check_result}")
                print(f"Měření trvalo: {duration_is_prime_check:.6f} sekund.")
        except Exception as e: # Zachytíme obecnější chybu pro případ, že soubor nebyl vygenerován
            print(f"Chyba: {e}")
            print("Prosím, nejprve spusťte generování prvočísel (síto).")
            print("-" * 50)
    def run(self):
        """
        Spustí hlavní smyčku uživatelského rozhraní aplikace.
        """
        while True:
            self._display_main_menu()
            choice = input("Vaše volba: ").strip()
            if choice == '1':
                self._run_sieve_action()
            elif choice == '2':
                self._change_limit_action()
            elif choice == '3': # Nová volba pro reset limitu
                if self._get_yes_no_input("Opravdu chcete nastavit limit na výchozí hodnotu? (Y/N)"):
                    self.sieve_manager.reset_limit_to_default()
                    print(f"Limit nastaven na výchozí:{self.sieve_manager.get_limit():,}.")
                if self._get_yes_no_input("Chcete spustit generování prvočísel (síto) s výchozím limitem? (Y/N)"):
                    self._run_sieve_action()
                else:
                    print("Síto nebylo spuštěno s výchozím limitem.")
            elif choice == '4':
                self._get_nth_prime_action()
            elif choice == '5':
                self._check_primality_action()
            elif choice == '6':
                if self._get_yes_no_input("Opravdu chcete ukončit aplikaci? (Y/N)"):
                    print("\nDěkuji za použití! Na shledanou.")
                    break
            else:
                print("Neplatná volba. Zadejte 1, 2, 3, 4, 5 nebo 6.")
            





        


                     


