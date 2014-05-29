#This is a demo script to be used with the NTC Class.
#Although the NTC Class is pretty much self explanatory,
#this demo will run you through the full functionality of the Class.
#Run it, have the code next to you, learn whats going on!
#Comment, debug, hack, play!
#OZ1LQO 2014.05.29

from NTC_py2 import *

def KtoC(n):
    """Converts from Kelvin to C"""
    return n-273

def CtoK(n):
    """Converts from C to Kelvin"""
    return n+273

#Create an NTC Object with standard B3470 values. Lets call it 'a'
a=Ntc(3470,10,CtoK(25))

#confirm the values
print(a)

#Do some calculations to compare measured and calculated values for
#R=8K and T=300K

t_meas=a.RtoT_meas(8)
r_meas=a.TtoR_meas(CtoK(27))

t_calc=a.RtoT_calc(8)
r_calc=a.TtoR_calc(CtoK(27))

print "\nTesting NTC class with R=8k and T=27C\n"

print "\nBased on the measured Thermistor, a resistance of 8k equals:",KtoC(t_meas),"C"
print "\nBased on the calculated Thermistor, a resistance of 8k equals:",KtoC(t_calc),"C"

print "\nBased on the measured Thermistor, a temperature of 27C equals:",r_meas,"kilo ohms" 
print "\nBased on the calculated Thermistor, a temperature of 27C equals:",r_calc,"kilo ohms"
 
wait=raw_input("\nPress ENTER to continue with a demo of linearization resistors")
#Demo of linearization resistor calculation

print "\n\n--Demo of linearization resistor calculation (see schematic)--\n"

#Find the values for the default temperature range: 25C-70C
Ra,Rb=a.Rlin()
print "\nCalculating linearization resistors for the default range: 25-70C"
print "\nBased on the measured B3470 NTC, the resistor should be:",Ra
print "\nBased on the modeled B3470 NTC, the resistor should be:",Rb

#Find the values for a temperature range between 15 and 50C
Ra,Rb=a.Rlin(CtoK(50),CtoK(15))
print "\nCalculating linearization resistors for a temperature range between 15 and 50C"
print "\nBased on the measured B3470 NTC, the resistor should then be:",Ra
print "\nBased on the modeled B3470 NTC, the resistor should then be:",Rb
print "\n--Note the difference between the measured and modeled values--"


wait=raw_input("\nPress ENTER to continue with a demo of a real life measurement")

print """\n\nDoing a simulated temperature measurement with the default values:
Rlin=2k, Rs=2.2k, Vs=5V, Vadc=2V"""

#call the temperature measurement with the default values
Ta,Tb=a.measurement()

print "\nTemperature using measured Thermistor:",KtoC(Ta),"C" 
print "\nTemperature using modeled Thermistor:",KtoC(Tb),"C"


wait=raw_input("\nPress ENTER to continue with a demo using a 3.3V power supply")

print """\n\nDoing a simulated temperature measurement with the values:
Rlin=2k, Rs=2.2k, Vs=3.3V, Vadc=1.2V"""


#call the temperature measurement with the new values
Ta,Tb=a.measurement(2,2.2,3.3,1.2)

print "\nTemperature using measured Thermistor:",KtoC(Ta),"C" 
print "\nTemperature using modeled Thermistor:",KtoC(Tb),"C"



wait=raw_input("\nPress ENTER to continue with a demo using a illegal values")

print """\n\nDoing a simulated temperature measurement with the values:
Rlin=2k, Rs=2.2k, Vs=5V, Vadc=3V. The ADC voltage is impossible and the object
will return with default measurements. ALWAYS make sure you're within the
allowed ranges and that the voltages mekes sense (use the spreadsheet)"""

#call the temperature measurement with the faulty values
Ta,Tb=a.measurement(2,2.2,5,3)

print "\nTemperature using measured Thermistor:",KtoC(Ta),"C"
print "\nTemperature using modeled Thermistor:",KtoC(Tb),"C"

wait=raw_input("\n\nThanks for playing, press ENTER to exit")






