import random


def foo(x,y,z):
    return 6*x**3 + 9*y**2 + 90*x - 25

def fitness(x,y,z):
    ans = foo(x,y,z)

    if ans == 0:
        
        return 99999
    else:
        return abs(1/ans)
    
#generate solution 

solutions = []
for s in range(1000):
    solutions.append( (random.uniform(0,10000), #it represent X 
                       random.uniform(0,10000), #it repersent Y
                       random.uniform(0,10000))) #it represent Z 
for i in range(10000):
    rankedsolution = []
    for s in solutions:
        rankedsolution.append( (fitness(s[0],s[1],s[2]),s))
    rankedsolution.sort()
    rankedsolution.reverse()
    print(f" === Gen {i} best solution is === ")
    print(rankedsolution[0])
    
    if rankedsolution[0][0] > 999:
        break
    bestsolution = rankedsolution[:100]

    elements = []

    for s in bestsolution:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])
    
    newgen = []
    for _ in range(1000):
        e1 = random.choice(elements) * random.uniform(0.99, 1.01)
        e2 = random.choice(elements) * random.uniform(0.99, 1.01)
        e3 = random.choice(elements) * random.uniform(0.99, 1.01)

        newgen.append( (e1,e2,e3))
    
    solutions = newgen 
