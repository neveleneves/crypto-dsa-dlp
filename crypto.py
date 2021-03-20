from random import randrange, getrandbits
from math import log

#Тест Миллера - Рабина
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
    while r % 2 == 0:
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

#Алгоритм Гордона по генерации сильного простого числа
def getStrongPrime(length):
    s = generatePrimeNum(length)
    t = generatePrimeNum(length)

    i = 100
    r = 0
    while not MR_Test(r):
        r = 2 * i * t + 1
        i+=1
    p0 = 2 * pow(s, r-2, r) * s - 1

    j = 100
    p = 0
    while not MR_Test(p):
        p = p0 + 2*j*r*s
        j+=1

    return [r,p]


# def getSqrtModAnother(a, p):
#     m = pow(a,1,p)
#     if m==(p-1):
#         print("Решений нет")
#         exit

#     b = 0
#     while 1:
#         if pow(b,(p-1)//2,p) == p-1:
#             break
#         b = randrange(p-1)

#     t=3
#     s=1
#     # p-1 =2^s + t
#     while 1:
#         if (p-1) % t == 0:
#             base = (p-1) // t
#             if log(base, 2) % 1 == 0:
#                 s = int(log(base, 2))
#                 base = 2
#                 break
#         t+=2
#     #################

def getSqrtMod(a, p):
    print("AAAAAAAAAAAAAAA=",a);
    R1 = pow(a,(p-1)//2,p)
    S = (p-1)//2
    R2 = 1
    Z = 0

    b = 0
    while 1:
        if pow(b,(p-1)//2,p) == p-1:
            break
        b = randrange(p-1)

    P=0
    x=0
    while 1:
        P=pow(R1*R2,1,p)
        # print(P)
        if P == 1 :
            if S%2==0:
                S=S//2
                Z=Z//2
                R1=pow(a,S,p)
                R2=pow(b,Z,p)
            else:
                break
        else:
            Z=Z+(p-1)//2

            if S%2==0:
                S=S//2
                Z=Z//2
                R1=pow(a,S,p)
                R2=pow(b,Z,p)
            else:
                break
            
    S=(S+1)//2
    Z=Z//2
    x=pow(pow(a,S,p)*pow(b,Z,p),1,p)

    print("XXXXXXXXXXXXXX=",x);
    return x


def getOpenKey(a, x, p):
    return pow(a,x,p)

def getU(p):
    return randrange(p-1)

def getA(gamma, p):
    print("Идёт вычисление параметра а...")
    a=2
    m=0
    while not m==1:
        a+=1
        m = pow(a,gamma,p)
    return a

def getZ(a, U, p):
    return pow(a, U, p)

def getK(U, h, x, Z, gamma):
    return pow((pow(h*U,1,gamma) + getSqrtMod(pow(pow(h,2,gamma)*pow(U,2,gamma),1,gamma) - pow(4*h*x*Z,1,gamma), gamma)) * inverse(2*h,gamma),1,gamma)

def getG(U,k,gamma):
    return pow(U-k,1,gamma)

def getS(a,g,p):
    return pow(a,g,p)

def getLeft(S, h, k, p, g):
    # return pow(g*h*k,1,p)
    return pow(S, h*k, p)  

def getRight(y,S,a,k,p,Z,h):
    # return pow(Z*h,1,p)
    return pow(y,pow(S*pow(a,k,p),1,p),p)

def verify_kg(k, g, U, x, Z, H, gamma):
    assert pow((k + g), 1, gamma) == pow(U,1, gamma)

    # print("pow((k * g * H), 1, gamma) = ", pow((k * g * H), 1, gamma))
    # print("pow((x * Z),1, gamma) = ", pow((x * Z),1, gamma))
    assert pow((k * g * H), 1, gamma) == pow((x * Z),1, gamma)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def inverse(element, module) -> int:
    return pow(egcd(element, module)[1], 1, module)

def init():
    countBits = 10

    #Получение значения гаммы
    [gamma,p] = getStrongPrime(countBits)

    # gamma = 187266130527359358103409790533
    # p = 1188242948802635102242772106637989280357
    print("gamma = ", gamma)
    print("p = ", p)

    #Выберем секретный ключ X
    x = randrange(1,p-1)
    # x = 12345678900987654321
    print("x = ", x)

    #Выберем случайный хеш сообшения
    h = randrange(1,p-1)
    # h = 13123123123154123152123
    print("h = ", h)

    # Выбираем значение альфа
    # а - число, относящееся к некоторому простому показателю гамма по модулю p
    # то есть нужно выбрать такое a, которое в степени gamma по модулю p будет давать 1 
    a = getA(gamma,p)
    # a = 682502200821353544223897742429626534895
    print("a = ", a)
    # print("a =============", pow(a,gamma.))

    # Вычисляем открытый ключ
    y = getOpenKey(a, x, p)
    print("y = ", y)

    # Вычисляем значение U
    U = getU(p)
    # U = getrandbits(countBits)
    # U = 13894564231549754238457865456
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

    verify_kg(k, g, U, x, Z, h, gamma)

    # Вычисляем значение S
    S = getS(a,g,p)
    print("S = ", S)

    print("Signature is (k,S) => ", k, S)

    # Проверка подписи...
    
    leftSideValue = getLeft(S, h, k, p, g)
    print("Side 1st = ", leftSideValue)

    rightSideValue = getRight(y,S,a,k,p,Z,h)
    print("Side 2nd = ", rightSideValue)


    # print("DONE 1ST = ", pow(S,k*h,p))
    # print("DONE 2ND = ",  pow(y,pow(S*pow(a,k,p),1,p),p))
init()
