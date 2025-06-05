# Import the PrimeGenerator class from its module


import math
import time

from prime_sieve.PrimeGenerator import PrimeGenerator
from funkce import measure_time
from UI.user_interface import User_interface2
# Import the measure_time function from the Funkce module




if __name__ == "__main__":
    app=User_interface2()

    app.run()