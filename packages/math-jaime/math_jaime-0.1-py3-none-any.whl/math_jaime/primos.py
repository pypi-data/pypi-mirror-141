

def printAllPrimesTillN(n):
    for i in range(1, n + 1):
        if (isPrime(i)):
            print(i, end=" ")


def isPrime(n):
    if(n==1 or n==0):
        return False
   
    #No necesitamos dividir entre todos los numeros, solo hasta la raiz cuadrada del objetivo
    for i in range(2,int(n**(1/2))+1):
        if(n%i==0):
            return False
   
    return True

printAllPrimesTillN(100)