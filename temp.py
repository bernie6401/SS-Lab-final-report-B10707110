import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal

#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_yac = deque(maxlen=max_entries)
        self.axis_yfilter = deque(maxlen=max_entries)
        self.axis_yfrequency = deque(maxlen=max_entries)
        self.axis_t = deque(maxlen=max_entries)
        self.x=np.linspace(0, 100, 500)
        self.t=0
        self.c =0
        self.t1=0
        self.t2=0
        self.t3=0
        self.heart=0
        self.heart1=[]
        self.y=0
        self.sec=0
        self.fir =0
        self.fir1=0
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
        self.axis_yac.append(y-np.mean(self.axis_y))
        self.axis_yfilter = signal.lfilter([1/7, 1/7, 1/7,1/7, 1/7, 1/7,1/7], 1, self.axis_yac)
       
        self.axis_yfrequency.append(np.fft.fft(self.axis_yac))
 
       
        
    def fre(self,y):
        
   
        '''
        print(y)
        print("=: "+str(y-self.fir))
        if((y-self.fir)>3):
            
            self.fir =y
            self.t = time.time()
            #print('t: '+ str(self.t))
        if((time.time()-self.t)>=0.2 ):
            if(y-self.fir1>3):
            
                self.fir1 =y
                self.t1 = time.time()
                print('t: '+ str(self.t1))
        if(time.time()-self.t1>0.8 and self.t1>self.t):
            if(self.t1-self.t<1 and self.t1-self.t>0.4):
                print('heartbeat: '+str(1/(self.t1-self.t)*60))
                self.fir=0
                self.fir1=0
          '''
          
     

        if(self.fir<y and self.c==0):
            
            self.fir =y
            self.t = time.time()
           # print('t: '+ str(self.t))
        if((time.time()-self.t)>=0.2 and self.c==0):
            self.c=1
            self.fir =0
           # print('t1: '+ str(self.t))
        if(self.fir<y and self.c==1):
            self.fir =y
            self.t1 = time.time()

           # print('t2: '+ str(self.t1))
        if(((time.time()-self.t1)>=0.45) and ((self.t1-self.t)<=0.9) and ((self.t1-self.t)>=0.45) and (self.c==1)):
            
            self.heart = self.t1-self.t
          
            #print('heartbeat_instant: '+str((1/self.heart*60)))
            '''
            if(len(self.heart1<5)):
                self.heart1.append((1/self.heart*60))
            if((len(self.heart1>5)) and abs(np.mean(self.heart1)-self.heart)<30):
                self.heart1.append((1/self.heart*60))
            '''
            self.heart1.append((1/self.heart*60))
            print('heartbeat_av: '+str(np.mean(self.heart1)))
            
            self.c=0
            self.fir=0
        if(((self.t1-self.t)>1) and self.c==1 ):
            self.c=0
            self.t =0
            self.fir=0
            '''        
            self.heart1.append( self.t1-self.t)
            print(str(len(self.heart1)))
            
            if(len(self.heart1)>10):
                for i in range(len(self.heart1)-10,len(self.heart1),1):
                    self.t2+=self.heart1[i]
             
                print("heartbeat 10 :"+str(1/(self.t2/10)*60))
                '''            
       
            
        
            
            
        
        '''            
        if(self.fir<=y and self.c==2):
            
            self.fir =y
            self.t2 = time.time()
            #print('t: '+ str(self.t))
        if((time.time()-self.t2)>=0.4 and self.c==2):
            self.c=3
            self.fir =0
           # print('t1: '+ str(self.t))
        if(self.fir<=y and self.c==3):
            self.fir =y
            self.t3 = time.time()

          #  print('t2: '+ str(self.t1))
        if(((time.time()-self.t3)>=0.4) and ((self.t3-self.t2)<=1) and (self.c==3)):
            self.c=0
            self.fir=0
            self.heart1 = self.t3-self.t2
            print('heartbeat1: '+str((1/self.heart1*60)))
            
            print("差: "+str((1/self.heart1*60)-(1/self.heart0*60)) )
            if(abs((1/self.heart1*60)-(1/self.heart0*60))<=10):
                print("heratbeat real : "+str(((1/self.heart1*60)+(1/self.heart0*60))/2))
            
        if(((self.t3-self.t2)>=1) and self.c==3):
            self.c=2
            self.t2 =0
            self.fir=0
        
        '''
        
        
       

                
            
             
            
             
         
        
      
           
           
    
       
        

angle = np.linspace(-np.pi, np.pi, 50)
cirx = np.sin(angle)
ciry = np.cos(angle)
z = np.roots([1/7, 1/7, 1/7,1/7, 1/7, 1/7,1/7])
p = np.roots([1,0,0,0,0,0,0])
plt.figure(figsize=(8,8))
plt.plot(cirx, ciry,'k-')
plt.plot(np.real(z), np.imag(z), 'o', markersize=12)
plt.plot(np.real(p), np.imag(p),'x', markersize=12)
plt.grid()
plt.text(0.1,0.1,6)
plt.xlim((-2, 2))
plt.xlabel('Real')
plt.ylim((-2, 2))
plt.ylabel('Imag')



#initial 初始圖樣v  
fig, (ax,ax2,ax3) = plt.subplots(3,1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))


fig1, (ax4) = plt.subplots(1,1)
line4, = ax4.plot(np.random.randn(100))
plt.show(block = False)
plt.setp(line2,color = 'r')



PData= PlotData(500)
ax.set_ylim(0,500)
ax2.set_ylim(-20,20)
ax3.set_ylim(-20,20)
ax4.set_ylim(0,200)
#PData.fre=[0.0, 500.0]

# plot parameters
print ('plotting data...')
# open serial port
strPort='com6'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()

while True:
    
    for ii in range(10):

        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data)
            PData.fre (data)
        except:
            pass



    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax3.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax4.set_xlim(0, 100)
    
    
    
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(PData.axis_yac)
    line3.set_xdata(PData.axis_x)
    line3.set_ydata(PData.axis_yfilter)
    
#    line4.set_xdata(PData.x)
 #   line4.set_ydata(abs(np.fft.fft(PData.axis_yfilter)))
    if(len(abs(np.fft.fft(PData.axis_y))) == 500):
        line4.set_xdata(PData.x)					#All Frequency of Heart Data
        line4.set_ydata(abs(np.fft.fft(PData.axis_yfilter)))
            
   # print(abs(np.fft.fft(PData.axis_yfilter)))
    
 #   print('heartbeat: '+ PData.list[2]*60)
   # PData.fre(data) 
    fig.canvas.draw()
    fig.canvas.flush_events()
    fig1.canvas.draw()
    fig1.canvas.flush_events()