

def mod_pow(base, exp, mod):
    """ Modular exponentiation, big speedup when numbers get large """
    res = 1
    for _ in range(exp):
        res *= base
        res = res % mod
    return res

def get_primes(MAX):
    """ Simple way of getting the list of first primes """
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
first_primes = list(get_primes(1000))

def egcd(a, b):
    """
    Extended Euclid's algorithm
    Returns gcd, x, y where gcd is the gcd of a, b and x*a + y*b == gcd.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = egcd(b % a, a)
        return (gcd, y - (b//a) * x, x)


# We chose two large primes
p, q = first_primes[-2:]
# n is the product of those primes
n = p * q
# Because p and q are prime, we can calculate phi(n)
phi = (p-1)*(q-1)

# Now we find e, d such that e*d % phi == 1 with d,e > 0
def get_exponents(phi):
    for e in range(2, phi):
        gcd, d, k = egcd(e, phi)
        if gcd != 1:
            continue
        if d <= 0:
            continue
        return e, d
    else:
        raise Exception("Could not find e > 0, d > 0 such that e*d % phi == 1")
e, d = get_exponents(phi)

# Now we can do encryption and decryption
message = 12345678
assert(message < n)
encrypted = mod_pow(message, e, n)
decrypted = mod_pow(encrypted, d, n)

print(f"message={message}, encrypted={encrypted}, decrypted={decrypted}")