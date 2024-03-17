import time
import gmpy2

def fibonacci_with_delay(n):
    start_time = time.time()

    a, b = gmpy2.mpz(0), gmpy2.mpz(1)
    for _ in range(n):
        a, b = b, a + b

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f'O {n}-ésimo número na sequência de Fibonacci é: {a}')
    print(f'Tempo de execução: {elapsed_time:.6f} segundos')

# Exemplo de uso
n = 5000000  # Ajuste o valor de 'n' conforme necessário para aumentar a complexidade
fibonacci_with_delay(n)
