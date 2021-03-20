from random import randrange, getrandbits

def MR_Test(n, k=128):
    # Если число 2 или 3, то сразу простое
    if n == 2 or n == 3:
        return True
    # Если 1 или чётное, то число составное
    if n <= 1 or n % 2 == 0:
        return False
    # Находим r и s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # Делаем заданное количество раундов для проверки числа
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

def generatePrimeCadidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generatePrimeNum(length):
    p = 4
    while not MR_Test(p, 128):
        p = generatePrimeCadidate(length)
    return p

def getStrongPrime(length):
    s = generatePrimeNum(length)
    t = generatePrimeNum(length)
    
    i = 1000
    r = 0
    while not MR_Test(r):
        r = 2 * i * t + 1
        i+=1
    p0 = 2 * pow(s, r-2, r) * s - 1

    j = 1000
    p = 0
    while not MR_Test(p):
        p = p0 + 2*j*r*s
        j+=1
    return [r,p]


def getSqrtQuadric(a, p):
    R1 = pow(a,(p-1)//2,p)
    S = (p-1)//2
    R2 = 1
    Z = 0

    
    b = 0
    while 1:
        if(pow(b,(p-1)//2,p) == p-1):
            break
        else: 
            b = randrange(p-1)

    P=0
    x=0
    while 1:
        P=pow(R1*R2,1,p)

        if(P == 1):
            if(S%2==0):
                S=S//2
                Z=Z//2
                R1=pow(a,S,p)
                R2=pow(b,Z,p)
            else:
                break
        else:
            p=-1
            Z=Z+(p-1)//2

            if(S%2==0):
                S=S//2
                Z=Z//2
                R1=pow(a,S,p)
                R2=pow(b,Z,p)
            else:
                break
    
    S=(S+1)//2
    Z=Z//2
    x=pow(pow(a,S)*pow(b,Z),1,p)

    return x


def getOpenKey(a, x, p):
    return pow(a,x,p)

def getU(p):
    return randrange(p-1)

def getA(gamma, p):
    print("Идёт вычисление параметра а...")
    a=3
    m=0
    while not m==1:
        m = pow(a,gamma,p)
        a+=1
    return a

def getZ(a, U, p):
    return pow(a, U, p)

def getK(U, h, x, Z, gamma):
    valForSqrt = h*h*U*U - 4*h*x*Z
    
    k = pow((h*U + getSqrtQuadric(valForSqrt, gamma))//2*h,1,gamma)

    return k

def getG(U,k,gamma):
    return pow(U-k,1,gamma)

def getS(a,g,p):
    return pow(a,g,p)

def getLeft(S, h, k, p):
    return pow(S, h * k, p) 

def getRight(y, S, a, k, p):
    return pow(y,pow(S*pow(a,k),1,p),p)

def init():
    #Получение значения гаммы
    [gamma,p] = getStrongPrime(3); 
    print("gamma = ", gamma)
    print("p = ", p)

    #Получение значение p
    # p = getStrongPrime(16)
    # print("p = ", p)

    #Выберем секретный ключ X
    x = getrandbits(3)
    print("x = ", x)

    #Выберем случайный хеш сообшения
    h = getrandbits(3)
    print("h = ", h)

    # Выбираем значение альфа
    # а - число, относящееся к некоторому простому показателю гамма по модулю p
    # то есть нужно выбрать такое a, которое в степени gamma по модулю p будет давать 1 
    a = getA(gamma,p)
    print("a = ", a)

    # Вычисляем открытый ключ
    y = getOpenKey(a, x, p)
    print("y = ", y)

    # Вычисляем значение U
    U = getU(p)
    print("U = ", U)
    
    # Вычисляем значение Z
    Z = getZ(a, U, p)
    print("Z = ", Z)

    # Вычисляем значение k
    k = getK(U, h, x, Z, gamma)
    print("k = ", k)

    # Вычисляем значение g
    g = getG(U,k,gamma)
    print("g = ", g)

    # Вычисляем значение S
    S = getS(a,g,p)
    print("S = ", S)

    print("Signature is (k,S) => ", k, S)

    # Проверка подписи...
    
    leftSideValue = getLeft(S,h,k,p)
    print("Side 1st = ", leftSideValue)

    rightSideValue = getRight(y, S, a, k, p)
    print("Side 2nd = ", rightSideValue)
    
    print("Done value = ", x * Z);
init()
