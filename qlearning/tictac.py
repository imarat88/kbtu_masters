import random
import time
import os
from math import hypot, pi, cos, sin, sqrt, exp
#import plot_epoch
maxiter = 500000
timesleep = 1
clear = lambda: os.system('cls')
wins = [0,0,0]

class field:
    def __init__(self, vision = 5):
        self.table = [0]*9
        self.features = []
        self.features.append(dict())
        self.features.append(dict())
        self.players = []
        self.players.append(Player(role=1))
        self.players.append(Player(role=2))
        self.actions = []
        self.gamma = 0.9
        self.alpha = 0.1
        self.tablestates = [['',''],['','']]

    def update_reward(self, k, position):

        self.getreward()


    def play2(self, k):

        finish =False
        steps = 0
        pl = k%2
        address = self.getfeatures()
        if address not in self.features[pl]:
            self.features[pl][address] = {}
        if k > 0:
            reward = self.getreward((pl-1)%2)
            if reward == 1000:
                self.features[(pl-1)%2][self.tablestates[(pl-1)%2][0]][self.actions[k - 2]] = (1 - self.alpha) * \
                                                                                  self.features[(pl-1)%2][
                                                                                      self.tablestates[(pl-1)%2][0]][
                                                                                      self.actions[
                                                                                          k - 2]] + self.alpha * (
                    reward + self.gamma * reward)

                self.features[pl][self.tablestates[pl][0]][self.actions[k - 2]] = (1 - self.alpha) * \
                                                                                  self.features[pl][
                                                                                      self.tablestates[pl][0]][
                                                                                      self.actions[
                                                                                          k - 2]] + self.alpha * (
                    reward + self.gamma * (-reward))

                return -reward
            if reward == 100:
                self.features[(pl-1)%2][self.tablestates[(pl-1)%2][0]][self.actions[k - 2]] = (1 - self.alpha) * \
                                                                                  self.features[(pl-1)%2][
                                                                                      self.tablestates[(pl-1)%2][0]][
                                                                                      self.actions[
                                                                                          k - 2]] + self.alpha * (
                    reward + self.gamma * reward)
                reward = -10
        maxval = -100000
        maxi = -1
        for i in range(9):
            if self.table[i] == 0:
                if not i in self.features[pl][address]:
                    self.features[pl][address][i] = -1
                if self.features[pl][address][i]>maxval:
                    maxi = i
                    maxval = self.features[pl][address][i]
        self.table[maxi] = pl + 1
        self.tablestates[pl][0] = self.tablestates[pl][1]
        self.tablestates[pl][1] = address
        if self.tablestates[pl][0] != '':
            self.features[pl][self.tablestates[pl][0]][self.actions[k - 2]] = (1 - self.alpha) * \
                                                                              self.features[pl][self.tablestates[pl][0]][
                                                                                  self.actions[k - 2]] + self.alpha * (
                reward + self.gamma * maxval)
        self.actions.append(maxi)
        return maxi


    def play(self):
        iterations = 0
        while True:
            iterations = iterations + 1
            if iterations == 66 or iterations == 14451:
                iterations = iterations
            self.actions = []
            self.table = [0]*9
            self.tablestates = [['', ''], ['', '']]
            for i in range(9):
                res = self.play2(i)
#                print('---------------')
#                self.print()
                if res<0:
                    wins[i%2+1] = wins[i%2+1] + 1
                    if i%2 == 0:
                        i = i
                    print('iterations', iterations,' X wins = ', wins[1], ' O Wins = ', wins[2], ' Draws = ', wins[0])
                    print('---------------')

                    break
                if i == 8:
                    wins[0] = wins[0]+1


    def getreward(self, player):
        reward = -1
        table = self.table
        combs = [[0,1,2], [0, 3, 6], [2,5,8], [6,7,8],[0,4,8], [2,4,6], [3,4,5], [1,4,7]]
        combsets = [set(a) for a in combs]
        for comb in combs:
            if table[comb[0]] == table[comb[1]] == table[comb[2]] == player+1:
                reward = 1000
                self.print()
                print(self.actions)
                return reward
        s1 = set(self.actions[player::2])
        s2 = set(self.actions[(player+1)%2::2])
        sg = set()
        for i in range(9):
            if self.table[i] == (player+1)%2+1:
                sg.add(i)
        sg.add(self.actions[len(self.actions)-1])
        for comb in combsets:
            if comb.intersection(sg) == comb:
                reward = 100
        return reward


    def print(self):
        a = [[0,0,0],[0,0,0],[0,0,0]]
        for ind, el in enumerate(self.table):
            a[ind//3][ind%3] = self.table[ind]

        for el in a:
            print(el)
        return True



    def getfeatures(self):

        address = ''.join([str(t) for t in self.table])
        return address


class Player:
    actions = [[0,1,2],[0,1,2]]

    def __init__(self, role = 1):
        self.role = role

    def put(self, k):

        game.table[k] = self.role
        return True

game = field()
game.play()