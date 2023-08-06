# función en para calcular los números primos entre 1 y n

def numero_primo_hasta_n(n):
    nump = []
    i  = 1
    while i <=n:
        cont =1
        x=0
        while cont <= i:
            if i % cont == 0:
                x=x+1
            cont = cont + 1
        if x == 2:
            nump.append(i)
        
        i += 1
    return nump