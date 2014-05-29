
#Linearized B3470 NTC temperature measurement using an A/D converter from abelectronics.
# http://www.abelectronics.co.uk/products/3/Raspberry-Pi/39/ADC-DAC-Pi-Raspberry-Pi-ADC-and-DAC-expansion-board
#Linearization resistor and series resistor was calculated in a spreadsheet
#R_lin=2K, R_series=2.2k. Power supply is selectable from 5V or 3.3V
#This script uses spidev and scipy which may have to be installed if not included already in the python installation.
#The script is written for Python 2.7
#OZ1LQO 2014.05.26
# Updated 2014.05.27 to use the NTC_py2 library


import spidev
import time
from scipy import interpolate

from NTC_py2 import *

def KtoC(n):
    """Converts from Kelvin to C"""
    return n-273

def CtoK(n):
    """Converts from C to Kelvin"""
    return n+273


#Setting up A/D Converter
spi = spidev.SpiDev()
spi.open(0,0)
     

def get_adc(channel):
    """This function handles reading from the ADC.
    Depending on the ADC module and adjoining libraries,
    this may have to be rewritten accordingly.
    The MCP3002 has a 3.3V rail"""
        
    # Only 2 channels 0 and 1 else return -1
    if ((channel > 1) or (channel < 0)):
        return -1
    r = spi.xfer2([1,(2+channel)<<6,0])
           
    ret = ((r[1]&0x0F) << 8) + (r[2])
    
    return ret*3.3/4096 #compensate for supply voltage and resolution for this specific ADC



# -MAIN SCRIPT PART-
#Greet the user
print """Welcome to the Rasperry PI NTC Thermistor demo!
Updated 2014.05.29 to use the newly made NTC Class/Library.
This demo shows how to use a linearized NTC Thermistor to measure the temperature.
See the calculation spreadsheet to learn about the linearization calculations.
You have to select the power supply for the sensor circuit, after that,
the script will do 10 successive measurements.
Have fun!!"""

supply=raw_input("\nWhat do you want, 1: 3.3V supply or 2: 5V ")

#select the right array based on the inputs
if supply=='1':
    Vs=3.3
else:
    Vs=5

#Setup Rlin, Rser
Rlin=2
Rs=2.2

#Create an NTC Object with standard B3470 values. Lets call it 'a'
a=Ntc(3470,10,CtoK(25))

#Let the object greet the user
print a


print "\n\nDoing a temperature measurement with the values:"
print "\nRlin=",Rlin," kOhm"
print "\nRs=",Rs," kOhm"
print "\nVs=",Vs,"Volts"



#Do 10 measurements at 1 second interval on ADC 0 based on the chosen parameters 

for i in xrange(10):
    level=get_adc(0)#Get ADC voltage
    #print "Level: ", level
    #call the temperature measurement with the values
    Ta,Tb=a.measurement(Rlin,Rs,Vs,level)
    print "\nMeasurement",i+1,"of 10"
    print "\nTemperature using measured Thermistor:","%.2f" % round(KtoC(Ta)),"C" 
    print "\nTemperature using modeled Thermistor:","%.2f" % round(KtoC(Tb)),"C\n" 
    time.sleep(1)
    





    


