from math import sqrt
class grad:
    def __init__(self,func,a,lim,step,r):
        self.func=func
        self.a=a
        self.step=step
        self.r=r
        self.lim=lim
    def dfdx(self,x,y):
        res=0
        px=1
        for i in range(1,self.lim):
            py=1
            for j in range(0,self.lim):
                res=res+i*self.a[i][j]*px*py
                py=py*y
            px=px*x
        return res
    def dfdy(self,x,y):
        res=0
        px=1
        for i in range(0,self.lim):
            py=1
            for j in range(1,self.lim):
                res=res+j*self.a[i][j]*px*py
                py=py*y
            px=px*x
        return res
    def gradf(self,x,y):
        fx=self.dfdx(x,y)
        fy=self.dfdy(x,y)
        l=sqrt(fx*fx+fy*fy)
        if(l==0):
            return [0,0]
        return [fx/l,fy/l]
    def run(self,ix,iy,tms):
        x=ix
        y=iy
        l=self.step
        res=self.func(x,y)
        for i in range(0,tms):
            v=self.gradf(x,y)
            v[0]=v[0]*l
            v[1]=v[1]*l
            nx=x+v[0]
            ny=y+v[1]
            if(abs(nx)>5 or abs(ny)>5):
                if(v[0]<0):
                    k=(-5-x)/v[0]
                    v1=v
                    v1[0]=v1[0]*k
                    v1[1]=v1[1]*k
                    if(abs(y+v1[1])<=5):
                        ny=y+v1[1]
                        nx=x+v1[0]
                elif (v[0]>0):
                    k=(5-x)/v[0]
                    v1=v
                    v1[0]=v1[0]*k
                    v1[1]=v1[1]*k
                    if(abs(y+v1[1])<=5):
                        ny=y+v1[1]
                        nx=x+v1[0]
                if v[1]<0:
                    k=(-5-y)/v[1]
                    v1=v
                    v1[0]=v1[0]*k
                    v1[1]=v1[1]*k
                    if(abs(x+v1[0])<=5):
                        ny=y+v1[1]
                        nx=x+v1[0]
                elif v[1]>0:
                    k=(5-y)/v[1]
                    v1=v
                    v1[0]=v1[0]*k
                    v1[1]=v1[1]*k
                    if(abs(x+v1[0])<=5):
                        ny=y+v1[1]
                        nx=x+v1[0]
                else:
                    nx=x
                    ny=y
            print(str(x)+" "+str(y))
            res=min(res,self.func(x,y))
            x=nx
            y=ny
            l=l*self.r
        print(res)