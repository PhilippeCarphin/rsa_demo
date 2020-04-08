def get_primes(MAX):
    current_primes = []
    def is_prime(i):
        if i in current_primes:
            return True
        for p in current_primes:
            if i % p == 0:
                return False
        return True

    n = 2
    while True:
        if is_prime(n):
            current_primes.append(n)
            yield n
        if len(current_primes) > MAX:
            break
        n += 1

def get_prime(N):
    return list(get_primes(N))[N-1]

p, q = list(get_primes(100))[-2:]
n = p * q

print(f'p={p}, q={q}, n={n}')

phi = (p-1)*(q-1)

print(f'phi={phi}')

e = 31
#Python program for Extended Euclidean algorithm
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = egcd(b % a, a)
		return (gcd, y - (b//a) * x, x)

gcd, d, k = egcd(e, phi)
print(f'By eucild, gcd(e, phi) = {gcd}')
print(f'by euclid extended algorithm, gcg=1={e}*{d} + {k}*{phi}')
print(f'That means that e*d % phi = {e*d % phi}')

message = 1234
encrypted = (message**e) % n

decrypted = (encrypted**d) % n

print(f"message={message}, encrypted={encrypted}, decrypted={decrypted}")