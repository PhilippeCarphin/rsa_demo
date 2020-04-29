#
# RSA encryption is mostly based on these three things:
# 1. Factoring a large number is way hard
# 2. a^(k*phi(n)) % n == 1 (this is known as Fermat's little theorem)
#    therefore a^(k*phi(n)+1) % n == a
#    and phi(n) gives how many numbers between 1 and n-1 share no
#    factors with n.
# 3. Calculating phi(n) is hard unless you know the factors of n, in which case it is very easy.
#    This is because phi(p) is obviously p-1 if p is a prime number.  With that
#    in mind, one can see why phi(pq) = (p-1)(q-1).
# (Sidenote about modular arithmetic: a*b % n == (a%n)*(b%n) % n and (a+b) % n ==
# (a%n) + (b%n)
# Ex: 13*5 % 6 == 65 % 6 == 5 % 6
#              == (13%6) * (5%6)
#              == 1%6 * 5*6
#              == 5%6
#
#
# The idea is to take p,q, two large primes
# then calculate n = pq
#
# Because we know the prime factors, we know
# that phi = (p-1)(q-1)
#
# All we have left to do is to find two things that when multiplied together make k*phi(n) + 1.
# Then we will have a^(k*phi(n) + 1) % n == a^(k*phi(n))*a % n == a % n (because
# a^(k*phi(n)) % n == 1%n.
#
# We start by trying to find e such that GCD(phi,e) = 1.  The idea is that
#
# By Euler's extended algorithm, we know that
# for any a,b, there exist x,y such that x*a + y*b = gcd(a,b)
# Therefore if gcd(e, phi) = 1, the algorithm will give us x,y such that
# x*e + y*phi = 1 (therefore x*e = y*phi + 1) so we now have two numbers x, e that multiply together
# to give something that is one above a multiple of phi (or x*e % phi == 1).
#
# Lets rename x to d, so we have e*d % phi == 1

# HERE IS HOW IT WORKS
# ====================
#
# This is where we use that theorem that A^(phi(n)) % n == 1 for any 0<A<n
#
# Let m < n be our message.
#
# m^e % n is the encrypted message, lets call it w (upside down m)
#
# To decrypt the encrypted message w, and we raise it to the power 'd'
# w^d % n  == (m^e)^d
#          == m^(ed)
#          == m^(y*phi + 1)
#          == m^(y*phi) * m 
#          ==     1     * m
#          == m


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
# We chose e, if it is coprime with phi, then egcd() will
# give us a d.  We could stop there but if d < 0, then
# that complicates things.  So we try different values of e
# until we get d > 0.
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

#
# SUMMARY
# 
# Private elements
# - Primes p,q
# - Phi = (p-1)(q-1)
# - d (decryption key)

# Public elements
# - n ( = p*q)
# - e Encryption key

# I calculated all these things, now if I want you to send
# me a message that no one else can read, I send you 'n' and 'e'
print(f'p={p}, q={q}, n={n}, phi={phi}, e={e}, d={d}')

# You have your message
message = 12345678
assert(message < n)

# You encrypt it with the encryption key and send me the encrypted message
encrypted = mod_pow(message, e, n)

# Because I know the 'd', I can decrypt the message but 
decrypted = mod_pow(encrypted, d, n)

print(f"message={message}, encrypted={encrypted}, decrypted={decrypted}")

# In the new die hard movie, they have to fill a bottle up to 4L using 3L and 5L jugs.
# We know that the problem is solvable becasue 3,5 are coprime, which means that
# their GCD = 1.  Therefore, there exists x,y such that x*3 + y*5 == 1 (2*5 - 3*3 = 1)
# if we want 4, then 4 = 8*5 -12*3
#                      = 6*5 + 2*5 - 10*3 - 2*3
#                      = 2*3*5 + 2*5 - 2*5*3 - 2*3
#                      = 2*5 - 2*3
