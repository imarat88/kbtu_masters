import random
import time
import os
from math import hypot, pi, cos, sin, sqrt, exp
#import plot_epoch
maxiter = 100000
timesleep = 1
clear = lambda: os.system('cls')

class Q:
    def __init__(self):
        self.gamma = 0.95
        self.alpha = 0.05
        self.state = {}

    def get_wp(self, plr):
        self.plr = plr

    def run_model(self, silent=1):
        self.plr.prev_state = self.plr.curr_state[:-2] + (self.plr.dx, self.plr.dy)
        self.plr.curr_state = tuple(self.plr.get_features(self.plr.x, self.plr.y)) + (self.plr.dx, self.plr.dy)

        if not silent:
            print(self.plr.prev_state)
            print(self.plr.curr_state)

        r = self.plr.reward

        if self.plr.prev_state not in self.state:
            self.state[self.plr.prev_state] = 0

        nvec = []
        for i in self.plr.actions:
            cstate = self.plr.curr_state[:-2] + (i[0], i[1])
            if cstate not in self.state:
                self.state[cstate] = 0
            nvec.append(self.state[cstate])

        nvec = max(nvec)

        self.state[self.plr.prev_state] = self.state[self.plr.prev_state] + self.alpha * (
            -self.state[self.plr.prev_state] + r + self.gamma * nvec)


class field:
    def __init__(self, vision = 5):
        self.maxx = 10 + random.randrange(6)
        self.maxy = 10 + random.randrange(6)
        self.ballnum = 5+random.randrange(6)
        self.balls = []
        while len(self.balls)<self.ballnum:
            self.balls.append(ball(random.randrange(self.maxx), random.randrange(self.maxy)))
        self.catcher = ball(random.randrange(self.maxx), random.randrange(self.maxy),8)
        self.vision = vision
        self.features = dict()
        self.tolerances = dict()
        self.catcherstates = ['','']
        self.tolerancestate = ['','']
        self.gamma = 0.95
        self.alpha = 0.05

    def getmaxx(self):
        return self.maxx

    def getmaxy(self):
        return self.maxy

    def play(self):
        finish =False
        steps = 0
        vision = self.vision
        mingreen = 1000000000
        maxi = 0

        x = self.catcher.getx()
        y = self.catcher.gety()
        address = self.getfeatures(x, y)
        tolerance = self.gettolerance(x, y)
        if tolerance not in self.tolerances:
            self.tolerances[tolerance] = {}
        if address not in self.features:
            self.features[address] = {}
        reward = self.getreward(x,y)
        maxval = reward
        self.features[address][maxi] = maxval
        rewardtolerance = self.getrewardtolerance(x, y)
        self.tolerances[tolerance][maxi] = rewardtolerance
        self.catcherstates[1] = address
        self.tolerancestate[1] = tolerance
        while not finish:
            x = self.catcher.getx()
            y = self.catcher.gety()
            lf = []
            #address = self.getfeatures(x, y)
            #tolerance = self.gettolerance(x, y)
            self.catcherstates[0] = str(self.catcherstates[1])
            self.catcherstates[1] = str(address)
            self.tolerancestate[0] = str(self.tolerancestate[1])
            self.tolerancestate[1] = str(tolerance)
            reward = self.getreward(self.catcher.x, self.catcher.y)
            # print(reward)

            #address = str(self.getfeatures(self.catcher.x, self.catcher.y))
            if self.features[self.catcherstates[1]][maxi]!=-10000000:
                self.features[self.catcherstates[1]][maxi] = self.features[self.catcherstates[1]][maxi]+self.alpha * (
                    -self.features[self.catcherstates[1]][maxi] + reward + self.gamma * maxval)
            else:
                self.features[self.catcherstates[1]][maxi] = reward

            rewardtolerance = self.getrewardtolerance(x, y)
            #self.tolerances[tolerance][maxi] = rewardtolerance

            self.tolerances[self.tolerancestate[1]][maxi] = rewardtolerance

            if steps > maxiter:
                print(self.features[self.catcherstates[1]][maxi])
                #print(self.tolerances[self.tolerancestate[0]][maxi])

                print('====================================')
                timesleep = 0.4
                if reward == -100000:
                    reward = reward
                    time.sleep(1)
                if reward>5000:
                    timesleep = 1
                    time.sleep(timesleep)
                    reward = self.getreward(self.catcher.x, self.catcher.y)
                else:
                    time.sleep(timesleep)


            self.moveballs()

            address = self.getfeatures(x, y)
            tolerance = self.gettolerance(x, y)

            maxi = random.randrange(9)
            maxval = -1000000
            vecmax = []
            for i in reversed(range(9)):
                nextx = x+ball.actions[i][1]
                nexty = y+ball.actions[i][0]
                if address not in self.features:
                    self.features[str(address)] = {}
                if tolerance not in self.tolerances:
                    self.tolerances[str(tolerance)] = {}
                if nextx in range(self.getmaxx()) and nexty in range(self.getmaxy()):
                    if i in self.features[address]:
                        if maxval<self.features[address][i] and self.tolerances[tolerance][i]>-1:
                        #if maxval < self.features[address][i]:
                            maxval = self.features[address][i]
                            maxi = i
                            # if self.tolerances[tolerance][i] == 1:
                            #     break
                    else:
                        self.features[address][i] = -10000000
                        maxi = i
                        maxval = 5000
                        break

                        # if maxval<self.features[address][i]:
                        #     maxval = self.features[address][i]
                        #     maxi = i

            self.catcher.catchermove(maxi)
            steps = steps+1
            point = self.print(steps)
            # if point is not None:
            #     self.balls[point] = ball()



    def getrewardtolerance(self, x, y):
        reward = 0
        catcher = self.catcher
        balls = self.balls
        vision = self.vision
        red = False
        yellow = False
        green = False
        fgen = []
        mingreen = 100000000
        for b in balls:
            if x == b.getx() and y == b.gety():
                if b.fine == 0:
                    green = True
                elif b.fine == 1:
                    yellow = True
                elif b.fine == 2:
                    red = True
        if red:
            reward = -2
        elif yellow:
            reward = -1
        elif green:
            reward = 1
        return reward

    def getreward(self, x, y):
        reward = -1000
        catcher = self.catcher
        balls = self.balls
        vision = self.vision
        red = False
        yellow = False
        green = False
        fgen = []
        mingreen = 100000000
        for ind, b in enumerate(balls):
            if ((x-b.getx())**2+(y-b.gety())**2)<vision**2:
                if b.fine == 0 and mingreen>(x - b.getx()) ** 2 + (y - b.gety()) ** 2:
                    mingreen = (x - b.getx()) ** 2 + (y - b.gety()) ** 2
            if x == b.getx() and y == b.gety():
                if b.fine == 0:
                    green = True
                    balls[ind] = ball(random.randrange(self.maxx), random.randrange(self.maxy),0)
                elif b.fine == 1:
                    yellow = True
                elif b.fine == 2:
                    red = True
        if red:
            reward = -100000
        elif yellow:
            reward = -50000
        elif green:
            reward = 100000
        if not red and not yellow:
            if mingreen != 100000000:
                reward = reward+(2000 -mingreen)
        return reward


    def print(self, steps):
        b1 = None
        i1 = None
        if steps > maxiter:
            print(len(game.features))
#        clear()
        a = []
        for y in range(self.getmaxy()):
            a2 = []
            for x in range(self.getmaxx()):
                a2.append(0)
            a.append(a2)
        for ind, b in enumerate(self.balls, start=0):
            if a[b.gety()][b.getx()] == 0:
                a[b.gety()][b.getx()] = b.fine+1
            elif a[b.gety()][b.getx()]>0:
                a[b.gety()][b.getx()] = a[b.gety()][b.getx()]*10+b.fine+1
            if b.getx() == self.catcher.getx() and b.gety() == self.catcher.gety():
                if b1 is None:
                    b1 = b
                    i1 = ind
                elif b1.fine < b.fine:
                    b1 = b
                    i1 = ind

        if a[self.catcher.gety()][self.catcher.getx()] == 0:
            a[self.catcher.gety()][self.catcher.getx()] = 8
        elif a[self.catcher.gety()][self.catcher.getx()] > 0:
            a[self.catcher.gety()][self.catcher.getx()] = a[self.catcher.gety()][self.catcher.getx()]*10+8
        if steps > maxiter:
            for y in range(self.getmaxy()):
                print(a[y])
        return i1


    def getfeatures(self, x, y):
        balls = self.balls
        vision = self.vision

        fgen  = []
        mingreen = 10000000
        for b in balls:
            if ((x-b.getx())**2+(y-b.gety())**2)<vision**2:
                if b.fine == 0 and mingreen>(x - b.getx()) ** 2 + (y - b.gety()) ** 2:
                    mingreen = (x - b.getx()) ** 2 + (y - b.gety()) ** 2
                f = []
                f.append(b.fine)
                f.append(x-b.getx())
                f.append(y-b.gety())
                f.append(x-b.getx()-ball.actions[b.direction][1])
                f.append(y-b.gety()-ball.actions[b.direction][0])
                f.append(f[0]**2+f[1]**2)
                f.append(f[2]**2+f[3]**2)
                f.append(f[5]-f[4])
                fgen.append(f)
        fgen = sorted(fgen, key=lambda x: (x[0], x[6], x[7], x[5]), reverse=False)
        address = ''
        for a in fgen:
            address = address+','.join(str(x) for x in a)
        return address+'|'


    def gettolerance(self, x, y):
        balls = self.balls
        a = [[0,0,0], [0,0,0], [0,0,0]]
        for b in balls:
            if abs(x-b.getx())<=1 and abs(y-b.gety())<=1:
                if a[1+y-b.gety()][1+x-b.getx()]<b.fine:
                    a[1+y-b.gety()][1+x-b.getx()] = b.fine
        t = []
        for i in range(3):
            for j in range(3):
                t.append(a[i][j])

        address = ','.join(str(x) for x in t)
        return address


    def moveballs(self):
        for b in self.balls:
            b.move()


class ball:
    actions = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self, x, y, fine = None):
        self.x = x
        self.y = y
        self.direction = random.randrange(1,9)
        self.fine = fine
        if fine is None:

            self.fine = random.randrange(3)
        self.prevx = x
        self.prevy = y

    def getxy(self):
        return self.x, self.y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def move(self):
        while True:
            if (0 <= self.x + ball.actions[self.direction][1] < game.getmaxx()) and (0 <= self.y +
                    ball.actions[self.direction][0] < game.getmaxy()):
                self.prevx = self.x
                self.prevy = self.y
                self.y = self.y + ball.actions[self.direction][0]
                self.x = self.x + ball.actions[self.direction][1]
                break
            else:
                self.direction = random.randrange(1,9)
        return self.x, self.y

    def catchermove(self, i):
        self.prevx = self.x
        self.prevy = self.y
        if (0 <= self.x + ball.actions[i][1] < game.getmaxx()) and (0 <= self.y +
            ball.actions[i][0] < game.getmaxy()):
            self.y = self.y + ball.actions[i][0]
            self.x = self.x + ball.actions[i][1]

        return True

game = field()
game.play()