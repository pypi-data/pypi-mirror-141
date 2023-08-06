
#n = int(input("Introduce el valor de n:\n"))

def calcula_primos(n):
    primos = []

    if (n == 0 or n == 1):
        print("Ni 0 ni 1 son numeros primos")
    else:
        for i in range(2,n+1):
            es_primo = True

            for ii in range(2,i):
                if (i % ii == 0):
                    es_primo = False
                
            if (es_primo == True):
                primos.append(i)

    if (n>1):
        return primos

    if (n>1):
        print(calcula_primos(n))

#Los dos últimos "if" evitan el output "None" por pantalla