## Cockipit to monitoring Serial Data from 
## Arduino Connected with SparkFun LSM9DS1 and GPS NEO-6M
## Serial data contains: 
## Complementary filter result from Accelerometer, Gyroscope and Magnetometer;
## GPS Data converted to X-axis and Y-axis relative of vehicle initial position;
## Kalman Filter result with X-axis and Y-axis relative of vehicle initial position;

import serial 
import numpy  
import matplotlib.pyplot as plt 
from drawnow import *
import numpy as np

pitchFromCompFilter= []
rollFromCompFilter=[]
yawFromCompFilter=[]
gpsX= []
gpsY=[]
kalmanX= []
kalmanY=[]

arduinoData = serial.Serial('/dev/cu.usbmodem14201', 115200, timeout = None)
plt.ion()
counter=0
plt.style.use('dark_background')

def buildGraph():
    plt.subplot(2,2,1)
    plt.title('Complementary Filter from IMU', fontname="Times New Roman Bold", weight='bold')                          
    plt.ylabel('Degrees')
    plt.xlabel('Time (s)')                       
    plt.plot(pitchFromCompFilter, 'r2-', label='Roll')       
    plt.ticklabel_format(useOffset=True)           
    plt.legend(loc='upper left')                 
    plt2=plt.twinx()                                
    plt2.plot(rollFromCompFilter, 'g2-', label='Pitch') 
    plt2.ticklabel_format(useOffset=True)           
    plt2.legend(loc='upper center')
    plt2=plt.twinx()                               
    plt2.plot(yawFromCompFilter, 'y2-', label='Yaw') 
    plt2.ticklabel_format(useOffset=True)           
    plt2.legend(loc='upper right')


    plt.subplot(2,2,2)
    plt.title('GPS Data', fontname="Times New Roman Bold", weight='bold')   
    plt.ylabel('X (m)', fontsize='smaller')
    plt.xlabel('Y (m)', fontsize='smaller')                             
    plt.plot(gpsX, gpsY, 'c.-', label='Distance') 
    plt.ticklabel_format(useOffset=True)           
    plt.legend(loc='upper right')


    plt.subplot(2,1,2)
    plt.title('Kalman Filter', fontname="Times New Roman Bold", weight='bold')
    plt.plot(kalmanX, kalmanY, 'md-')

    plt.tight_layout(3.0)

while True: 
    while (arduinoData.inWaiting()==0): 
        pass 

    arduinoString = arduinoData.readline() 
    dataArray = arduinoString.split(',')   

    try:
        pitchFromCompFilter_ = float(dataArray[0])           
    except ValueError as e:
        pitchFromCompFilter_ = 0;
    except IndexError as e:
        pitchFromCompFilter_ = 0;

    try:
        rollFromCompFilter_ = float(dataArray[1])
    except ValueError as e:
        rollFromCompFilter_ = 0;
    except IndexError as e:
        rollFromCompFilter_ = 0;

    try:
        yawFromCompFilter_ = float(dataArray[2])
    except ValueError as e:
        yawFromCompFilter_ = 0;
    except IndexError as e:
        yawFromCompFilter_ = 0;

    try:
        gpsx_ = float(dataArray[3])
    except ValueError as e:
        gpsx_ = 0;
    except IndexError as e:
        gpsx_ = 0;
    try:
        gpsy_ = float(dataArray[4])
    except ValueError as e:
        gpsy_ = 0;
    except IndexError as e:
        gpsy_ = 0;
    try:
        kalmanX_ = float(dataArray[5])
    except ValueError as e:
        kalmanX_ = 0;
    except IndexError as e:
        kalmanX_ = 0;
    try:
        kalmanY_ = float(dataArray[6])
    except ValueError as e:
        kalmanY_ = 0;
    except IndexError as e:
        kalmanY_ = 0;

    print(str(pitchFromCompFilter_) + "," +  str(rollFromCompFilter_) 
    + "," + str(yawFromCompFilter_) + "," + str(gpsx_) + "," + str(gpsy_) 
    + "," + str(kalmanX_) + "," + str(kalmanY_))

    pitchFromCompFilter.append(pitchFromCompFilter_)                    
    rollFromCompFilter.append(rollFromCompFilter_)       
    yawFromCompFilter.append(yawFromCompFilter_)   

    gpsX.append(gpsx_)      
    gpsY.append(gpsy_)          

    kalmanX.append(kalmanX_)
    kalmanY.append(kalmanY_)

    drawnow(buildGraph)                     

    counter = counter + 1
    if(counter > 1000):                            
        pitchFromCompFilter.pop(0)                      
        rollFromCompFilter.pop(0)
        gpsX.pop(0)
        gpsY.pop(0)
        kalmanX.pop(0)                     
        kalmanY.pop(0)
