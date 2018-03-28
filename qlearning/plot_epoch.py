import matplotlib.pyplot as plt

class epoch_graph:
    def __init__(self):
        self.it=0
        self.iter=[]
        self.number=[]
        self.iter_aver=[]

    def plt_append(self,iter):
        self.it=self.it+1
        self.iter.append(iter)
        self.number.append(self.it)
        if len(self.iter)>100:
            self.iter_aver.append(sum(self.iter[-100:])/100)
        else:
            self.iter_aver.append(sum(self.iter)/len(self.iter))

    def plt_virt_game(self,W,QModel):
        wr=W(5,QModel)
        wr.P.eps=0.0
        iter=wr.play(1,0)
        self.plt_append(iter)

    def plot_graph(self):
        plt.plot(self.number,self.iter_aver)
        plt.xlabel('n_epoch')
        plt.ylabel('aver. score')
        plt.show()