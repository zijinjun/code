import random
import sa
import grad
import ga
a=[]
lim=4
def funcval(x,y):
    res=0
    px=1
    for i in range(0,lim):
        py=1
        for j in range(0,lim):
            res=res+a[i][j]*py
            py=py*y
        px=px*x
    return res
if __name__ == '__main__':
    for i in range(0,lim):
        b=[]
        for j in range(0,lim):
            if(random.random()>0.1):
                b.append(random.randint(-100*(i+j),100*(i+j)))
            else:
                b.append(0)
        a.append(b)
    for i in range(0,lim):
        
        for j in range(0,lim):
            print(a[i][j],end=" ")
        print("")
    sa = sa.SA(funcval)
    sa.run()
    pop = ga.Population(funcval,50, 24, 0.8, 0.1, 150)
    pop.run()
    G=grad.grad(funcval,a,lim,0.5,0.95)
    G.run(0 ,0 ,100)
