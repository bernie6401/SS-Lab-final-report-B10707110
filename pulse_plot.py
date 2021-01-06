import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from scipy.fftpack import fft,ifft
from scipy import signal
from collections import deque
from scipy.io import loadmat


#Display loading
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_xf = deque()
        self.axis_yf = deque()
        self.axis_xfr = np.linspace(0,100,max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
    def add_fir(self, x, y):
        self.axis_xf.append(x)
        self.axis_yf.append(y)

t1=0
h_rate=0
t_hrv=0
input_sig=deque()
xx=deque()
hr=deque()
def fir(sig ):   #*FIR filter
    global t1
    global h_rate
    global t_hrv
    input_sig.append(sig)
    yf =signal.lfilter([1/3, 1/3, 1/3], 1, input_sig)
    xf = np.fft.fft(yf)
    xf[0] = 0   #dc=0
    xf1 = np.fft.ifft(xf)   #反傅立業
    d1=deque()

    d_1=deque()     #一段時間的數值 (heartrate)
    if(len(xf1)>100):
        if(t1 != 0) :
            for i in  range(1,100,1):
                d_1.append(xf1[len(xf1)-i])
            if(xf1[len(xf1)-1] == np.max(d_1)):
                t2=t
                if (t2-t1)**-1*60 <120:
                    hr.append((t2-t1)**-1*60)
                    h_rate=np.mean(hr)
                    print('Heartrate: ',np.mean(hr))
                    t_hrv+=1
                    xx.append(t2-t1)
                    if(t_hrv==10):
                        print('---------')
                        h=0
                        t_hrv=0
                        hrv2=round(1000*np.std(xx,ddof=1))
                        print('HRV:',hrv2,'ms')
                        xx.clear()


                t1=t2
        if(t1 == 0):
            for i in  range(1,100,1):
                d_1.append(xf1[len(xf1)-i])
            if(xf1[len(xf1)-1] == np.max(d_1)):
                t1=t
    for i in  range(1,20,1):
        d1.append(xf1[len(xf1)-i])
    d2=np.mean(d1)
    xf1[len(xf1)-1]=d2
    PData.add_fir(t,xf1[len(xf1)-1])       #*fir
    return d2






or_sig=deque()
def set_or_sig_ylim(sig):
    or_sig.append(sig)
    d1=deque()
    if(len(or_sig)>10):
        for i in  range(1,10,1):
            d1.append(or_sig[len(or_sig)-i])
    d3=np.mean(d1)
    return d3
#initial
fig, (ax,ax2,ax3) = plt.subplots(3,1,figsize=[10,10])
fig1, (ax4) =plt.subplots(1,1,figsize=[8,8])    #add window
angle = np.linspace(-np.pi, np.pi, 50)
cirx = np.sin(angle)
ciry = np.cos(angle)
plt.plot(cirx, ciry,'k-')
plt.grid()
z1=np.array([1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20,1/20])
z_=np.roots(z1)     #poles
plt.plot(np.real(z_), np.imag(z_), 'o', markersize=12)
z2=np.array([1,0,0])
z_=np.roots(z2)     #zeros
plt.plot(np.real(z_), np.imag(z_), 'x', markersize=12)
plt.text(0.15,0.15,'x20')
ax4.set_xlim(-2,2)
ax4.set_xlabel('Real')
ax4.set_ylim(-2,2)
ax4.set_ylabel('Imag')
ax.set_xlabel('time(s)')
ax2.set_xlabel('time(s)')
ax3.set_xlabel('frequent(HZ)')
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100)) #*
plt.show(block = False)
plt.setp(line2,color = 'r')



PData= PlotData(500)
ax3.set_ylim(0,100)
# plot parameters
print ('plotting data...')
# open serial port
strPort='com5'  #home pc com5 ,school com4
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()
while True:

    for ii in range(10):

        try:
            data = float(ser.readline())
            set_or_sig_ylim(data)
            t = time.time() - start
            PData.add(t, data)
            fir(data)   #*FIR filter
            ax2.set_ylim(fir(data)-2,fir(data)+2)  #change fir_y range
            ax.set_ylim(set_or_sig_ylim(data)-3,set_or_sig_ylim(data)+3)    #change original signal y range

        except:
            pass

    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax3.set_xlim(0, 100)   #*
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(PData.axis_xf)
    line2.set_ydata(PData.axis_yf)
    if (len(np.fft.fft(PData.axis_y)) == len(PData.axis_xfr)):
        line3.set_xdata(PData.axis_xfr)
        line3.set_ydata(abs(np.fft.fft(PData.axis_y)))
    fig.canvas.draw()
    fig.canvas.flush_events()
