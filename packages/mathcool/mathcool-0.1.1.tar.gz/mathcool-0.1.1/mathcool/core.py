# Insert your code here.
"""This code is for calculating factorial"""
def factorial(N):
    d=1
    for i in range(N+1):
        if i==1 or i==0:
            d=1
        else:
            d=i*d
    return (d)


"""This code is for calculating double factorial"""
def doublefac(n):
    if n==1 or n==0:
        return 1
    else:
        return n*doublefac(n-2)

"""This code is for plotting density of Gauss type function"""
"""photon is the number of photon,atom is the number of atoms,t is the time of evolution.Suggest the version of matplotlib is 3.2.1"""
def Gaussdensity (photon,atom,t):
    import numpy as np
    import matplotlib.pyplot as plt
    fig = plt.figure()#plot figure
#ax = Axes3D(fig)
# X Y value
    X = np.arange(0, atom+1, 1)
    Y = np.arange(0, atom+1, 1)
    X, Y = np.meshgrid(X, Y)
    def fac(h):
        if(h==0):
            return 1
        else:
         return (h*fac(h-1))#factorial,you can also the mathcool.factorial() in this repository
    z=np.zeros((atom+1,atom+1))
    m=np.zeros((atom+1,atom+1))
    for i in range(0,atom+1):
        z[:,i]=fac(atom)/fac(i)/fac(atom-i)
        m[i,:]=fac(atom)/fac(i)/fac(atom-i)
    Z=1/(2**atom)*np.sqrt(z*m)*np.cos((X+Y)*t)**photon
# plt settings
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title('hello')
    plt.xlim(0,atom)
    plt.ylim(0,atom)
    plt.pcolormesh(X,Y,Z, cmap='jet' ,shading='flat')
    plt.colorbar()

    plt.show()

"""This code is for calculating function of Hermite """
def Hermite(n1,x):
    if n1<=0:
        return 1
    elif n1==1:
        return 2*x
    else:
        return 2*x*Hermite(n1-1,x)-2*(n1-1)*Hermite(n1-2,x)

"""This code is used for calculating Binomal"""
def C(n2,m2):
    return factorial(n2)/(factorial(n2-m2)*factorial(m2))

"""This code is used for calculating Laguerre polynomial"""
def Laguerre(n2,x_):

    if n2==1:
        return -x_+1
    elif n2==2:
        return x_^2-4*x_+2
    else:
        j = 0
        for c in range (n2+1):
            j=j+(-1)**c*C(n2,x_)*factorial(n2)/factorial(c)*x_**c
        return j

















