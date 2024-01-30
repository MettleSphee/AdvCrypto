from math import sqrt,gcd,factorial,lcm
import random

def input_xy():
    x = input("x = ")
    y = input("y = ")
    if x.isdigit() and y.isdigit():
        if x > y:
            list_xy = [y,x]
        else:
            list_xy = [x,y]
    else: #if(n.isdigit==False or n == ''):
        print("incearca din nou!")
        list_xy = input_xy()
    return list_xy

def inputN():
 n = input("Introduceti un numar neprim n mai mare ca 11 (pentru atacurile RSA,Fermat/Pollard).\nDaca nu folositi asta, scrieti 697.\nn = ")
 #print(n)
 if n.isdigit():
  n = int(n)
  if (n < 11):
   print("n este prea mic sau este incorect setat!\nIntrodu o noua valoare:")
   return inputN()
  #print(n)
  if prime_check(n)==True:
   print(f"Numarul {n} este prim! Nu se pot efectua Fermat, Pollard\'s Rho sau Pollard\'s p-1\nIntrodu o noua valoare:")
   return inputN()
  return n
 else:
  print("n nu este numar! incearca din nou!")
  return inputN()

def main_menu(n):
        #print(f"n = {n}")
        print('''====RSA Attacks====
1. Fermat
2. Pollard(p-1)
3. Pollard Rho
4. Afla m cu phi(n)
5. Afla m cu lambda(n)
6. Calculeaza valoarea phi(n)
7. Schimba valoarea lui n

======Other tools======
8. Euclid (se introduc 2 numere)
9. Exponentiere rapida
10. Shamir (polinomiala grad 2, cu 3 perechi cunoscute)
11. Elgamal aditiv (public key -> secret key -> message)
12. Elgamal multiplicativ (pub key -> sec key -> msg)

======IESIRE======
13. exit()
''')
        choice = input(">>")
        match choice:
            case "1":
                fermat_attack(n)
            case "2":
                pollard_PeeMinusOne_init(n)
            case "3":
                print_Pollard_Rho(n)
            case "4":
                RSA_Phi(n)
            case "5":
                RSA_Lambda(n)
            case "6":
                get_phi(n)
            case "7":
                main_menu(inputN())
            case "8":
                euclid(n)
            case "9":
                rapid_exp(n)
            case "10":
                shamir_2(n)
            case "11":
                additiveElgamal(n)
            case "12":
                multiplicativeElgamal(n)
            case "13":
                return
            case _:
                print("Invalid option! Try again!")
                main_menu(n)

def prime_check(n):
    x = 1
    for i in range (2, int(sqrt(n))+1):
        if n%i==0:
            x=0
            break
    if x == 1:
        return True
    else:
        return False

def pqn_check(p,q,n):
	return (p*q == n)

def fermat_attack(N):
	#input N		# N = p*q
	k = int(sqrt(N)) + 1
	print(f"incepem cu k = [sqrt({N})] + 1\n=> k = {int(sqrt(N))} + 1 = {k}")
	perfsquare = k**2 - N
	print(f"luam patratul perfect pp = {k}^2 - {N}\n=> pp = {perfsquare}\nsi acum facem pasii:\n")
	while (perfsquare != ( int( sqrt(perfsquare) ) **2 ) ) :
	    print(f"pp nu este patrat perfect\n=> k++:\n=> k = {k} + 1 = {k+1};")
	    k = k + 1
	    perfsquare = k**2 - N
	    print(f"pp = {k}^2 - {N}\n=> pp = {perfsquare}\n")
	print(f"am gasit pp patrat perfect,\nsqrt({perfsquare}) = {sqrt(perfsquare)};\n")
	p = k - int(sqrt(perfsquare))
	q = k + int(sqrt(perfsquare))
	print(f"=> p = {k} - [sqrt({perfsquare})] = {p};\n=> q = {k} + [sqrt({perfsquare})] = {q};\n")
	print(f"Final variables:\nN = {N}\nk = {k}\npp = {perfsquare}\np = {p}\nq = {q}\n")
	print(f"Final Check: {p}*{q} == {N} {pqn_check(p,q,N)}\n\n")
	main_menu(N)

#fermat_attack(697) #- seems to work so far

def pollard_PeeMinusOne_init(n):
    a = input("Incepem cu o valoare a anume? Daca nu, scrieti 0\na = ")
    #print(bytes(a,'ascii'))
    if a=='' or a==None:
        a = 0
        print("a nu este setat!")
    else:
        if a.isdigit():
            print()
        else:
            print("nu a fost introdus un numar!")
            a = 0
    pollard_PeeMinusOne(n,int(a))

def pollard_PeeMinusOne(N,a_set):   #a_set == 0 for NOT set
    def init_a(n,a):
        for i in range(2,(int(N/2) + 1)):
            if gcd(i,N)==1:
                a = i
                break
        return a
    if (a_set <= 0):
        a_set = init_a(N,a_set)
    elif (a_set >= (int(N/2) + 1)):
        print(f"a este prea mare!")
        a_set = init_a(N,a_set)
    a = a_set
    print(f"a = {a} SET\n")
    for b in range(2, (int(N/2) + 1)):
        b_factorial = factorial(b)
        ayBee= a**b_factorial
        d = gcd((ayBee - 1)%N,N)
        print(f'''b = {b}
b! = {b}! = {b_factorial}

a^b! = {a}^{b}! = {a}^{b_factorial}
=> a^b! = {ayBee}

d = gcd(a^b! - 1 mod N, N)
=> d = gcd({a}^{b}! - 1 mod {N}, {N})
=> d = {d}''')
        if (d!=1):
            p = d
            print(f"FOUND!\n")
            break
        print(f"=========NEXT STEP==========")
    q = int(N/p)
    #Final print:
    print(f"Final results:\n\nn: {N}\na: {a}\nb: {b}\nb!: {b_factorial}\na^b!: {a}^{b_factorial}\nd: gcd(a^b! - 1 (mod n), n) = {d}\np: {p}\nq: {q}\n\nFinal Check: {p}*{q} == {N} {pqn_check(p,q,N)}\n\n")
    main_menu(N)

def print_Pollard_Rho(n):
    values = Pollard_Rho(n,None,False,1,False)
    print(f'''
    n: {values[0]}
    d: {values[1]}
    x: {values[2]}
    y: {values[3]}
    c: {values[4]}
    x_init: {values[5]}
    n/d: {values[0]/values[1]}\n
    Final check: {values[0]}%{values[1]} == 0 : {(values[0]%values[1]==0)}\n
=> p = {values[1]}; q = {int(values[0]/values[1])}
    ''')
    main_menu(n)

def Pollard_Rho_Init(n,x,is_set,c,c_set):
    if is_set:
        x = int(x+1)
    else:
        x = input("Incepem cu o valoare x anume? Daca nu, scrieti 0\nx = ")
        if x=='' or x==None or x==0:
            x = False
            print("initializam cu x = 2...\n")
        else:
            if x.isdigit():
                x = int(x)
            else:
                print("x nu este un numar! initializam cu x = 2...")
                x = False
    if (x == False):
        x = 2
    #c = int(random.randrange(1,n)%(int(n/2) + 1))
    if c_set:
        c = int(c+1)
    else:
        new_c = input("vreo valoare c anume? default: 1\nc = ")
        if new_c=='' or new_c==None or new_c==0:
            c = 1
            print("c = 1...\n")
        else:
            if new_c.isdigit():
                c = int(new_c)
            else:
                print("c = 1... (wrong input)\n")
                c = 1
    return [x,c]

def Pollard_Rho(n,x,x_set,c,c_set):
    def eff(x,c):
        return int(x**2 + c)
    values = Pollard_Rho_Init(n,x,x_set,c,c_set)
    print("f(x) = x^2 + c (mod n)\n")
    step=0
    x_init = values[0]
    d = 1
    x = values[0]
    y = x
    c = values[1]
    while d==1:
        print(f"=============pasul {step}===============\n")
        print(f"x = f({x}) (mod {n})\n=> x = {x}^2 + {c} (mod n)")
        x = eff(x,c)%n
        print(f"=> x = {x}\n")
        print(f"y = f(f({y})mod n) mod n\n=> y = ({y}^2 + {c} (mod n))")
        y = eff(y,c)%n
        print(f"=> y = ({y}^2 + {c} (mod n))")
        y = eff(y,c)%n
        print(f"=> y = {y}\n")
        d = gcd(n, abs(x-y)%n)
        print(f"d = gcd(n, |x-y|)\n=> d = gcd({n}, |{x} - {y}|)\n=> d = {d}")
        step = step + 1
    if d==n:
        print("d == n, x_init++, resetam cu c = c+1 (incepem cu pasul 0)")
        result = Pollard_Rho(n,x_init,True,c+1)
    else:
        result = [n,d,x,y,c,x_init]
        #print('found result')
        #print(result)
    #print('step out')
    return result # d divide n

def gcd_step(x,y):
    print(f"{y} = {x}*{int(y/x)} + {y%x}")
    if y%x != 0:
        result = gcd_step(int(y%x),x)
    else:
        return x
    return result


def euclid(n):
    print("\n")
    [x,y] = input_xy()
    x = int(x)
    y = int(y)
    print('\n')
    print(f"gcd({x},{y}) = {gcd_step(x,y)}\n")
    main_menu(n)

def get_first_factor(n):
    for i in range (2, int(sqrt(n))+1):
        if n%i==0:
            return i

def get_phi(n):
    factors = []
    old_n = n
    while (prime_check(n)==False):
        new_factor = get_first_factor(n) #only executed if not prime
        factors.append(new_factor)
        n = n / new_factor
    n = int(n)
    #if (prime_check(n)==True): #after the while, this should always return true
        #factors.append(n)  #for better consistency, we use n as last factor
    #print(f"phi({old_n}) = ")
    printFactors = "" + (f"phi({old_n}) = ")
    for i in factors:
        printFactors = printFactors + (f"phi({i}) * ")
    printFactors = printFactors + (f"phi({n})")
    print(printFactors)
    printFactors = "= "
    for i in factors:
        printFactors = printFactors + (f"({i} - 1)")
    printFactors = printFactors + (f"({n} - 1)")
    print(printFactors)
    printFactors = "= "
    n = n - 1
    #for i in factors:
    #    print(f"{i} -> {(i-1)}")
    #    i = i - 1
    for i in range(0,len(factors)):
        factors[i] = factors[i] - 1
        printFactors = printFactors + (f"{factors[i]} * ")
    printFactors = printFactors + (f"{n}")
    for i in factors:
        n = n * i
    print(f"= {n}")
    main_menu(old_n)

def rapid_exp(nonUsedValue):
    n = input(f"ce numar? n = ")
    x = input(f"la ce putere? x = ")
    mod = input(f"modulo? mod = ")
    n = int(n)
    x = int(x)
    use_x =x
    mod = int(mod)
    i = 1
    while (i <= x):
        print(f"{n}^{i} = {(n**i)%mod} (mod {mod})")
        i = i*2
    #basic formula: (n^x)%mod = value (modulo mod), done with the print
    #now to do the final adding
    factors_list = []
    i = 1
    #I need to get the power of 2 highest that isnt larger than x
    while (i<=use_x):
        if (i*2<=use_x):
            i = i*2
        else:
            factors_list.append(i)
            use_x = use_x - i
            i = 1
    #print(factors_list) #got the factors
    printOutput = "" + f"\n=> {n}^{x} = "
    for i in factors_list:
        printOutput = printOutput + f"{n}^{i} + "
    printOutput = printOutput[:-2] + f"(mod {mod})"
    print(printOutput)
    printOutput = "= "
    result = 0
    for i in factors_list:
        result = result + ((n**i)%mod)
        printOutput = printOutput + f"{(n**i)%mod} + "
    printOutput = printOutput[:-2] + f"(mod {mod})\n= {result%mod} (mod {mod})\n"
    print(printOutput)

    main_menu(nonUsedValue)

def shamir2_solve(x1,x2,x3,f1,f2,f3,t):
    b = int(input("b = "))
    a = int(input("a = "))
    s1 = (f1 - (x1*a%t) - ((x1**2%t)*b))%t
    s2 = (f2 - (x2*a%t) - ((x2**2%t)*b))%t
    s3 = (f3 - (x3*a%t) - ((x3**2%t)*b))%t
    print(f"{s1} == {s2} == {s3}")
    if s1 == s2 == s3:
        print(f"Am gasit s! s = {s1}")
    else:
        print(f"Nu am gasit s. a sau b gresite?")
        shamir2_solve(x1,x2,x3,f1,f2,f3,t)

def shamir_2(nonUsedValue):
    print("Shamir's Secret Sharing: Polinomiala de grad 2, cu 3 perechi.\n")
    t =    int(input(f"P apartine Z t [X]. t = "))
    x1 =   int(input(f"x1 = "))
    f_x1 = int(input(f"f(x1) = "))
    x2 =   int(input(f"x2 = "))
    f_x2 = int(input(f"f(x2) = "))
    x3 =   int(input(f"x3 = "))
    f_x3 = int(input(f"f(x3) = "))
    print("\n")
    print(f"x1: s + {x1%t}a + {x1**2%t}b = {f_x1}")
    print(f"x2: s + {x2%t}a + {x2**2%t}b = {f_x2}")
    print(f"x3: s + {x3%t}a + {x3**2%t}b = {f_x3}\n")
    print(f"Rezolva sistemul, cand ai a,b scrie-le:")
    shamir2_solve(x1,x2,x3,f_x1,f_x2,f_x3,t)
    main_menu(nonUsedValue)

def additiveElgamal(nonUsedValue):
    n = int(input("modulo n = "))
    g = int(input("generator g = "))
    h = int(input("public key h = "))
    c1= int(input("c1 = "))
    c2= int(input("c2 = "))
    print(f"\nBe sure to include that:\nBecause it's ADDitive elgamal, a^b --> a*b\nConversely, a^(-1) = -a\nInclude the computation of the Euclid gcd(g,n) form before this:")
    print(f"gcd({g},{n}) = {gcd(g,n)}\n=> calculating g^(-1) mod {n}\n<Hint: use the Euclid tool for {n} and {g}>")
    found = False
    i = 1
    while (found == False):
        if (g*i%n == gcd(g,n)):
            print(f"found! i = {i}")
            found = True
        else:
            i = i + 1
    print("This program will use the first method, by finding the secret key x:\nFormula: x = g^-1 * h")
    print(f"--> x = ({i} * {h}) mod {n}")
    x = i*h%n
    print("=> x = {x}")
    print(f"And now, we find the clear message m:\nFormula: m = c2 - x*c1")
    print(f"=> m = ({c2} - {x} * {c1}) mod {n}")
    print(f"=> m = {(c2 - (x*c1))} mod {n}")
    m = (c2 - (x*c1))%n
    print(f"=> m = {m} mod {n}")
    main_menu(nonUsedValue)


def multiplicativeElgamal(nonUsedValue):
    n = int(input("modulo p = "))
    g = int(input("generator g = "))
    h = int(input("public key h = "))
    c1= int(input("c1 = "))
    c2= int(input("c2 = "))
    
    print("This program will use the first method, by finding the secret key x:\nFormula: (2^x) % p == h")
    Found = False
    i = 0
    while (Found == False):
        i = i + 1
        x = 2**i % n
        print(f"2^{i} = {x%n} (mod {n})")
        if (x == h):
            Found = True
    x = i
    print(f"=> x = {x} (secret key)")
    print(f"The formula for m becomes: m = c2 * ( c1^(-x) )\n=> m = {c2} * ( {c1}^(-{x}) )")
    print(f"Do the calculations using successive squaring (exponentiere rapida) for {c1} ^ {x} (mod {n})")
    print(f"After writing them, we obtain:\nm = {c2} * ({c1}^{x})^(-1) mod {n}")
    print(f"=> m = {c2} * {c1**x % n}^(-1)\n=> m = {c2 * ( (c1**x%n) ** (-1))}")
    print("If the value of m is not an integer (X.0) then you have to use extended euclid to calculate.")
    print(f"In this case, the result should be:\nm = {c2} * {pow(c1,-x,n)} mod {n}")
    print(f"=> m = { (c2 * pow(c1,-x,n)) % n } mod {n}")
    main_menu(nonUsedValue)

#These two are copies of former functions just because my programming right now is sloppy and I'd rather have it all done the way I can, I don't know if I'll fix it later or not
def pr_init(n,x,is_set,c,c_set):
    if is_set:
        x = int(x+1)
    else:
        x = 2
    if c_set:
        c = int(c+1)
    else:
        c = 1
    return [x,c]

def p_rho(n,x,x_set,c,c_set):
    def eff(x,c):
        return int(x**2 + c)
    values = pr_init(n,x,x_set,c,c_set)
    step=0
    x_init = values[0]
    d = 1
    x = values[0]
    y = x
    c = values[1]
    while d==1:
        x = eff(x,c)%n
        y = eff(y,c)%n
        y = eff(y,c)%n
        d = gcd(n, abs(x-y)%n)
    if d==n:
        result = p_rho(n,x_init,True,c+1)
    else:
        result = d
    return result # returns factor

def RSA_Lambda(n):    
    print(f"N = {n}")
    e = int(input("public key e = "))
    c = int(input("encrypted message c = "))
    p = p_rho(n,0,False,0,False)
    q = int(n/p)
    print(f"Do the factorisation of N, obtain:\np = {p}, q = {q}")
    L = lcm(p-1, q-1)
    print(f"Obtain lambda(n) = lcm(p-1,q-1) (do the steps bro)\nlambda({n}) = {L}")
    d = pow(e,-1,L)
    print(f"Now do the extended euclid to find out: d = e^-1 mod lambda(n)\n=> d = {e}^-1 mod {L}\n=> d = {d}")
    m = pow(c,d,n)
    print(f"All that's left to do is to calculate m = c^d mod N\n=>m = {c}^{d} mod {n}\n(use exp. rapida)\n=>m = {m} mod {n}")    
    main_menu(n)

def RSA_Phi(n):
    print(f"N = {n}")
    e = int(input("public key e = "))
    c = int(input("encrypted message c = "))
    p = p_rho(n,0,False,0,False)
    q = int(n/p)
    print(f"Do the factorisation of N, obtain:\np = {p}, q = {q}")
    phi = (p-1)*(q-1)
    print(f"phi(n) = (p-1) * (q-1)\n=> phi({n}) = {p-1} * {q-1}\n=> phi({n}) = {phi}")
    d = pow(e,-1,phi)
    print(f"Now do the extended euclid to find out: d = e^-1 mod phi(n)\n=> d = {e}^-1 mod {phi}\n=> d = {d}")
    m = pow(c,d,n)
    print(f"All that's left to do is to calculate m = c^d mod N\n=>m = {c}^{d} mod {n}\n(use exp. rapida)\n=>m = {m} mod {n}")
    main_menu(n)

main_menu(inputN())
