import time


def NextPrime( _pole:list,_index):
    print("next",_pole)
    _prime=_pole[_index]+2
    for _i in range(_index):
        if(_prime % _pole[_index]==0):
            _prime=_prime+2          
            _i=0

        if(_i>=1): 
            if(_prime / _pole[_i] < _pole[_i]): return _prime
    return _prime            
     



print ("Ahoj světe, pojďme vypsat pár prvočísel. Kolik jich chceš? ")

n= int(input("zadej počet:"))
Prime=[]
Prime.append(2)
Prime.append(3)

print (Prime[0],Prime[1])
for i in range(n):
    Prime.append(0)
for i in range(n):
 
    if Prime[i]==0:
        Prime[i]=NextPrime(Prime, i-1)
    
print(Prime)
