# ejercicio #2

def v_primo(n):
        primo = []
        for n in range(1,n):
                if n > 1:
                        c=0
                        i=2
                        while i<n and c==0: 
                                r=n%i
                                if r==0:
                                        c+=1
                                i+=1
                        if c ==0:
                               primo.append(i)    
        return primo
