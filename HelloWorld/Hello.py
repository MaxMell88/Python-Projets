import time


def NextPrime( _pole:list,_index):
    #print("next",_pole)
    _prime=_pole[_index]+2
    _i=0
    while (_i<=_index):
        if(_prime % _pole[_i]==0):
            _i=0
            _prime=_prime+2          
            
            
        if(_i>=1): 
            if((_pole[_i]*_pole[_i])>_prime):
                return _prime
        _i=_i+1        
     
    return _prime            
     


print ("Ahoj světe, pojďme vypsat pár prvočísel. Kolik jich chceš? ")

n= int(input("zadej počet:"))
zahajeni=time.time()
Prime=[]
Prime.append(2)
Prime.append(3)

print (Prime[0],Prime[1])
for i in range(n-2):
    Prime.append(0)
for i in range(n):
 
    if Prime[i]==0:
        Prime[i]=NextPrime(Prime, i-1)
ukonceni=time.time()
    
print(Prime)
print("čas zahájeni:",zahajeni)
print("čas ukončení:",ukonceni)
print("Výpočet trval :",(ukonceni-zahajeni))
print("Nejvetší nalezené prvočílo je ", Prime[n-1])
