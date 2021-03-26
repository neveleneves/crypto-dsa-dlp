from random import randrange, getrandbits

#Тест Миллера - Рабина
def MR_Test(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r % 2 == 0:
        s += 1
        r //= 2
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

#Получение значения гаммы и p
#Алгоритм Гордона по генерации сильного простого числа
def getStrongPrime(length):
    s = generatePrimeNum(length)
    t = generatePrimeNum(length)

    i = 1
    r = 0
    while not MR_Test(r):
        r = 2 * i * t + 1
        i+=1
    p0 = 2 * pow(s, r-2, r) * s - 1

    j = 1
    p = 0
    while not MR_Test(p):
        p = p0 + 2*j*r*s
        j+=1

    return [r,p]

# Функция для нахождения квадратного корня по модулю
def getSqrtMod(a, p):
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

    return x

# Вычисляем значение открытого ключа
def getOpenKey(a, x, p):
    return pow(a,x,p)

# Выбираем значение U
def getU(p):
    return randrange(p)

# Выбираем значение альфа
def getA(gamma, p):
    print("\nИдёт вычисление параметра а...")
    b = 0
    gammaCheck = 0
    z = 0

    while 1:
        b = randrange(2, p)
        gammaCheck = (p-1)//gamma
        z = pow(b,gammaCheck,p) 

        if not z==1:
            return z

# Вычисляем значение Z
def getZ(a, U, p):
    return pow(a, U, p)

# Вычисляем параметр k
def getK(U, h, x, Z, gamma, sqrtModValue):
    return pow((pow(h*U,1,gamma) - sqrtModValue) * inverse(2*h,gamma),1,gamma)

# Вычисляем параметр g
def getG(U,k,gamma):
    return pow(U-k,1,gamma)

# Вычисляем параметр S
def getS(a,g,p):
    return pow(a,g,p)

# Вычисляем левую часть проверочного сравнения
def getLeft(S, h, k, p):
    return pow(S, h*k, p)  

# Вычисляем правую часть проверочного сравнения
def getRight(y,S,a,k,p):
    return pow(y,pow(S*pow(a,k,p),1,p),p)

# Функция для проверки квадратичного вычета
def verifyQuadResidue(x, a, p):
    if(pow(pow(x,2,p),1,p) == pow(a,1,p)):
        print("Квадратичный вычет - найден")
        print("{}^2 ≡ {} mod {}\n".format(x,pow(a,1,p),p))
    else: 
        print("{} - это квадратичный невычет, параметр U был перегенирирован".format(a,1,p))
        return 1

# Функция для отслеживания выполнения системы
def verify_kg(k, g, U, x, Z, H, gamma):
    assert pow((k + g), 1, gamma) == pow(U,1, gamma)
    assert pow((k * g * H), 1, gamma) == pow((x * Z),1, gamma)

# Расширенная функция Евклида для вычисления деления по модулю (знаменатель)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# Обратный элемент в кольце (знаменатель)
def inverse(element, module) -> int:
    return pow(egcd(element, module)[1], 1, module)

def init():
    countBits = 512

    #Получение значения гаммы и p
    [gamma,p] = getStrongPrime(countBits)

    print("gamma = ", gamma)
    print("p = ", p)

    #Выберем секретный ключ X
    x = randrange(1,p-1)
    print("x = ", x)

    # Выбираем значение альфа
    # а - число, относящееся к некоторому простому показателю гамма по модулю p
    a = getA(gamma,p)
    print("a = ", a)

    # Вычисляем открытый ключ
    y = getOpenKey(a, x, p)
    print("y = ", y)

    # Выберем случайный хеш сообшения
    h = randrange(1,p-1)
    print("h = ", h)

    # Вычисляем значение U
    U = getU(gamma)
    print("U = ", U)
    
    # Вычисляем значение Z
    Z = getZ(a, U, p)
    print("Z = ", Z)

    print("\nИдёт вычисление параметра k...")
    expression = pow(pow(pow(h,2,gamma)*pow(U,2,gamma),1,gamma) - pow(4*h*x*Z,1,gamma),1,gamma)
    sqrtModValue = getSqrtMod(expression, gamma)
    while verifyQuadResidue(sqrtModValue, expression, gamma):
        U = getU(p)
        Z = getZ(a, U, p)
        expression = pow(pow(pow(h,2,gamma)*pow(U,2,gamma),1,gamma) - pow(4*h*x*Z,1,gamma),1,gamma)
        sqrtModValue = getSqrtMod(expression, gamma)

    # Вычисляем значение k
    k = getK(U, h, x, Z, gamma, sqrtModValue)
    print("k = ", k)

    # Вычисляем значение g
    g = getG(U,k,gamma)
    print("g = ", g)

    verify_kg(k, g, U, x, Z, h, gamma)

    # Вычисляем значение S
    S = getS(a,g,p)
    print("S = ", S)
    print("\nSignature is (k,S) => ", k, S)

    # Проверка подписи...
    
    leftSideValue = getLeft(S, h, k, p)
    print("\nLeft Side = ", leftSideValue)

    rightSideValue = getRight(y,S,a,k,p)
    print("Right Side = ", rightSideValue)

    # Невозможность нахождения секретного ключа
    print("\nX*Z mod p = ", pow(x*Z,1,p))
init()
