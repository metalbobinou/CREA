#####
# Distribution mathématique d'un ensemble en paquets de tailles équivalentes.
#####
def distributeLength(number, maxPack = 8000, threshold = 20):
    if maxPack <= 0:
        print("maxPack must be positive AND above 0");
        return []
    
    if threshold < 0 or threshold > 100:
        print("Threshold is a percentage (20% ideally) between 0 and 100")
        return []

    if number < maxPack :
        return [number]

    q,r = number // maxPack, number % maxPack

    if r == 0:
        return [maxPack] * q

    maxT = maxPack + ((maxPack * threshold) // 100)
    minT = maxPack - ((maxPack * threshold) // 100)
    
    # Si le reste est suffisamment grand, on peut s'arrêter:
    if r > maxT:
        L = [maxPack] * q
        L.append(r)
        return L 

    q2,r2 = r // q, r % q

    # Si le reste peut être distribué entre les autres paquets,
    # on peut s'arrêter:
    if maxPack + q2 + r2 < maxT:
        L = [maxPack + q2] * q
        L[-1] += r2
        return L

    # Sinon, on recommence récursivement:
    return distributeLength(number, minT, threshold)

#####
# Distribution avec comme contrainte une spécification sur les séparateurs
# (uniquement sur les ' ' et '\n' dans un texte)
#####
def distributeIndex(text, maxPack = 3750, threshold = 20):
    size = len(text)
    L = distributeLength(size, maxPack, threshold)
    L.insert(0, 0)
    n = len(L)
    for limit in range(1, n):
        L[limit] += L[limit - 1]
        while L[limit] < size and text[L[limit]] not in [' ', '\n'] :
            L[limit] += 1
    
    while L[-1] >= size:
        L.pop()
    L.append(size)
    return L

#####
# Découpe un texte pour permettre d'effectuer des requêtes Babelfy, et renvoie
# les paquets ainsi que leurs index de début et de fin.
#####
def cutByPack(text):
    indexes = distributeIndex(text)
    requests = []
    for i in range(len(indexes) - 1):
        requests.append(text[indexes[i]:indexes[i+1]])
    return requests, indexes
