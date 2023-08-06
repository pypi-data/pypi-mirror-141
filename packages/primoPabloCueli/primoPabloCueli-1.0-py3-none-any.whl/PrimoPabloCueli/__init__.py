

# Para que un numero sea primo deber ser divisible solo por si mismo y por 1

def num_primo(n):
    for i in range(2, n):
        if n % i == 0:
            print(n, "no es primo")
            return False
    print(n, "es primo")
    return True
num_primo(7)
