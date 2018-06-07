# Crypto Tools For CTF
<p><a target="_blank" href="https://camo.githubusercontent.com/b0224997019dec4e51d692c722ea9bee2818c837/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6d6173686170652f6170697374617475732e737667"><img src="https://camo.githubusercontent.com/b0224997019dec4e51d692c722ea9bee2818c837/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f6d6173686170652f6170697374617475732e737667" alt="license" data-canonical-src="https://img.shields.io/github/license/mashape/apistatus.svg" style="max-width:100%;"></a></p>

# cryptools


In this project, I integrate some source code collected from others great writeup, blog, project or made by myself and then do some reimplement to fit the structure.

I always use those methods to solve Crypto problem, and put new attack or method after the CTF, hoping this project will bring help for other CTF players.

It's still incomplete for now, pull requests are always welcome.

# cryptools.RSA 

Here provides some factorize formula to factor large RSA modulus amd some common RSA attacks.

I integrate some source code collected from others great writeup, blog, project or made by myself and then do some reimplement to fit the structure.

I always use those methods to solve RSA problem, and hope this project will bring help for other CTF players, pull requests are always welcome.

### Redundancy Work :

* RSAKey((n,e,d)) - Just like Crypto.PublicKey.RSA, and add some lazy function. d is option, determine is pubkey or privkey
    * encrypt(m)         - return the encryption of message
    * decrypt(c)         - return the decryption of cipher
    * load_pem(pem)      - Read Key by String
    * load_file(key.pem) - Read Key by file path
    * cal_private(e,p,q) - return the decrypt exponent

* solve_crt(remainders, modules) - solve Chinese Remainder Theoreme
* factordb(n) - API for getting well-known prime in FactorDB

### Factorization Method :

* gcd_multiple_keys(keys) - GCD for Multiple keys
* factordb(n) - Check the prime is factorize in FactorDB or not
* fermat_factorization(n) - Fermat Factorization
* wiener(n,e)       -   Wiener Attack
* boneh_durfee(n,e) -   Boneh Durfee Attack
* williams_pp1(n)   -   Williams p+1 Attack
* pollard_rho(n)    -   Pollards-Rho 
* pollard_pm1(n)    -   Pollards P-1 (Go through every primes)
* pollard_brute(n)  -   Pollards P-1 (Go through every integer)

### RSA Specific Methods :

* Partial Key Recovery for n/2 bits of the private key
* Chinese Remainder Theorem full private key recovery
Decoding despite invalid Public Exponent

### Low Public Exponent : 

* hastad_broadcast(c, N) - Hastad's Broadcast Attack
* common_modular(set1,set2) - Common Modulus, Common public Exponent [set:(N,e,c)]
* franklin_reiter(n,e,c1,c2,r,a=1) - Franklin Reiter Related Message Attack :


### Information LOSS : (TODO)

* coppersmith           - Coppersmith Attack
* coppersmith_shortpad  - Coppersmith Shortpad Attack
* partial_m()           - Known Partial bits of m, recover.
* partial_p()           - Known Partial bits of p, recover.
* partial_d()           - Known Partial bits of d, recover.
* recover_key()         - Known Partial bits of d, recover.

### Forge Signature :

* bleichenbacher_06     - Attack on (e=3) python-rsa signature.

### Others :

* noveltyprimes(n)
* smallq(n)
* smallfraction(n)
* mersenne_primes(n)


# cryptools.DSA

* Biased-K Attack

# cryptools.CBC

* Bit-flipping attack
* Padding Oracle
* POODLE Attack

