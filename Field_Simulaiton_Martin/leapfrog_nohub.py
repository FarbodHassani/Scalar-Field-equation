import numpy as np
import array
#
def binfunc(binfac,x,y):
    if (binfac == 1):
        xbin = x
        ybin = y
        return xbin, ybin
    else:
        n1 = len(x)
        nb = np.int(n1/binfac)
        xmin = np.min(x)
        xmax = np.max(x)
        bins = np.linspace(xmin,xmax,nb)
        dig = np.digitize(x,bins)
        #y = y+1.e-99
        ybin = [np.exp(np.log(y[dig==i]).mean()) for i in range (1,len(bins))]
        xbin = 0.5*(bins[1:]+bins[:-1])
        return xbin, ybin
#
nx = 2**16 #1024 # size of data array
phi0 = 1.e-4
myseed = 444
binfac = 2**6
#
f1=open('./output.txt', 'w')
f2=open('./spectrum_pi.txt', 'w')
f3=open('./spectrum_zeta.txt', 'w')
f4=open('./spectrum_phi.txt', 'w')
#
np.random.seed(seed=myseed)
phi = phi0*np.random.randn(nx)
kernel = np.zeros(np.shape(phi))
sx = 1.e-2/4.0
sigsq = (sx*np.float(nx))**2
for ix in range(nx):
    kernel[ix]=np.exp(-0.5*np.float(ix)**2/sigsq)
phism = np.real(np.fft.ifft( np.fft.fft(phi)*kernel ))
phism = phism - np.mean(phism)
np.savetxt("real_phi.txt",phism)
spec = np.abs(np.fft.fft(phism))**2
freqs = np.fft.fftfreq(len(phism))
#f3.write(" ".join(map(str,freqs)))
#f3.write("\n")
#f3.write(" ".join(map(str,spec)))
#f3.write("\n")
xbin, ybin = binfunc(binfac,freqs,spec)
f4.write(" ".join(map(str,xbin)))
f4.write("\n")
f4.write(" ".join(map(str,ybin)))
f4.write("\n")
#
pi   = np.zeros(nx)
zeta = np.zeros(nx)
tauin = 0.0
dt    = 1.e-3
tauend = 1000.0 #100.0
cs2 = 1.e-3
al  = 1.0 #10000.0
dx  = 1.0
#
#
tau = tauin
while (tau < tauend):
    tau = tau + dt
    pi  = pi+dt*(zeta+phism)
    piplus  = np.roll(pi,1)
    piminus = np.roll(pi,-1)
    zeta = zeta + dt*(al*((piplus-piminus)/(2.0*dx))**2 - cs2*(piplus+piminus-2.0*pi)/dx**2)
    if ((np.any(np.isnan(pi)) or np.any(np.isnan(zeta)))):
        print('NaN found, aborting') # oops, pi goes nan first?
        exit()
    if (np.abs(np.int(tau)-tau)<dt):
        print tau,np.mean(pi),np.mean(zeta)
        f1.write(str(tau)+"   "+str(np.mean(pi))+"   "+str(np.mean(zeta)) + "\n")
    if (tau<650.0):
        tauwrite = 10.0
    elif (tau<660.0):
        tauwrite = 1.0
    else:
        tauwrite = 0.1
    if (np.abs(np.int(tau/tauwrite)-tau/tauwrite)<dt/tauwrite):
        spec = np.abs(np.fft.fft(pi))**2
        xbin, ybin = binfunc(binfac,freqs,spec)
        f2.write(str(tau)+" "+" ".join(map(str,ybin)))
        f2.write("\n")
        spec = np.abs(np.fft.fft(zeta))**2
        xbin, ybin = binfunc(binfac,freqs,spec)
        f3.write(str(tau)+" "+" ".join(map(str,ybin)))
        f3.write("\n")
        print('writing spectrum')
