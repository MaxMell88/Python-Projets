# Import the PrimeGenerator class from its module


import math
import time

from prime_sieve.PrimeGenerator import PrimeGenerator

test=PrimeGenerator()
# Import the measure_time function from the Funkce module
from funkce import measure_time
from UI.user_interface import User_interface

app=User_interface()



if __name__ == "__main__":
    app.run()  