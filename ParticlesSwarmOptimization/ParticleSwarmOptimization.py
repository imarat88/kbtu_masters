import random

stopSearch = 200000
S = 10
w = 0.0
wMax = 0.91
wMin = 0.4
phip = 0.149
phig = 0.149

n = 0
c = []
M = 0.0

class Particle():
    # v = []
    # x = []
    # pBest = []

    def __init__(self, dim):
        self.dim = dim
        self.x = []
        self.v = []
        self.pBest = []
        for j in range(dim):
            self.x.append((random.random()*10))
            self.v.append((random.random()*10))
        self.pBest = list(self.x)
        return



    def moveParticle(self):
        for j in range(self.dim):
            self.x[j] = self.x[j]+self.v[j]
        return

    def changeVelocity(self, gBest):
        rp = random.random()
        rg = random.random()
        for j in range(self.dim):
            self.v[j] = w * self.v[j] + phip * rp * (self.pBest[j] - self.x[j]) + phig * rg * (
            gBest[j] - self.x[j])


class ParticleSwarm():
    swarm = []
    gBest = []

    def __init__(self, dim):
        for i in range(S):
            p = Particle(dim)
            self.swarm.append(p)



    def search(self):
        global w
        self.gBest = self.swarm[0].pBest
        for k in range(1, stopSearch):
            w = wMax-((wMax-wMin)*k)/stopSearch
            for i in range(S):
                if self.lossfunction(self.swarm[i].pBest)>self.lossfunction(self.swarm[i].x):
                    self.swarm[i].pBest = self.swarm[i].x

            for i in range(S):
                lfgBest =self.lossfunction(self.gBest)
                if lfgBest>self.lossfunction(self.swarm[i].pBest):
                    self.gBest = self.swarm[i].pBest

            for i in range(S):
                self.swarm[i].moveParticle()
                self.swarm[i].changeVelocity(self.gBest)
            if lfgBest<0.00000001:
                break
        return self.gBest

    def lossfunction(self, x):
        l = 0.0
        for i in range(n):
            l = l+c[i]*x[i]
        return abs(M-l)


def main():
    global n, c, M
    with open('diaphants.txt',mode='r',encoding='utf-8') as f:
        n = int(next(f).split()[0])
        c = [float(k) for k in next(f).split()]
        M = float(next(f).split()[0])

    PSO = ParticleSwarm(n)
    optimal = PSO.search()

    for i in range(n):
        if i>0:
            print(' + ',end='')
        print(c[i],' * X',i, end='')
    print(' = ',M,'\n')
    for i in range(n):
        if i>0:
            print(' + ',end='')
        print(c[i],' * ',optimal[i], end='')
    print(' = ',M)



if __name__ == '__main__':
    main()