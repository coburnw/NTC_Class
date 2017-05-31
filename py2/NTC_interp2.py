#Class to work with NTC Thermistors in Python 2
#Fell free to modify, improve, hack!
#Note! Temperature range is limited to a range between 1 and 98C
#OZ1LQO 2014.05.29

import math
from scipy import interpolate


#Define resistance vs. temperature arrays for the interpolate function
#X should always be ascending (apparently not)
# todo: investigate if ascending/decending returns the same results...

# from Vishay NTCLE413 Datasheet
B3435_const = {'resistance' : [0.85833, 0.97426, 1.1092, 1.2667, 1.4513, 1.6684, 1.9246, 2.2280,
                         2.5888, 3.0197, 3.5362, 4.1583, 4.9106, 5.8249, 6.9411, 8.3108,
                         10.000, 12.094, 14.706, 17.979, 22.108, 27.348, 34.038, 42.636,
                         53.762, 68.260, 87.285, 112.440, 145.953, 190.953 ],
         'temperature' : [105+273, 100.0+273, 95.0+273, 90.0+273, 85.0+273, 80.0+273, 75.0+273, 70.0+273,
                          65.0+273, 60.0+273, 55.0+273, 50.0+273, 45.0+273, 40.0+273, 35.0+273, 30.0+273,
                          25.0+273, 20.0+273, 15.0+273, 10.0+273, 5.0+273, 0.0+273, -5.0+273, -10.0+273,
                          -15.0+273, -20.0+273, -25.0+273, -30.0+273, -35.0+273, -40.0+273]
     }

# OZ1LQO calibrated B3470 thermister 
OZ1LQO_const = {'resistance' : [0.94, 1.04, 1.16, 1.32, 1.52, 1.74, 2.03, 2.33, 2.71, 3.16, 3.73, 4.43, 5.2,
                         6.2, 7.5, 9.8, 11.28, 13.5, 16.15, 18.5, 25.5],
         'temperature' : [371, 368, 363, 358, 353, 348, 343, 338, 333, 328, 323, 318, 313, 308, 303,
                          298, 293, 288, 283, 278, 274]
     }

thermisters = { 'B3435': B3435_const, 'OZ1LQO' : OZ1LQO_const}


class Ntc(object):
    """A class to interpolate from NTC Thermistor Temperature vs Resistance tables.
    All temperatures are in degrees Kelvin and all resistance values are in kilo ohms"""

    def __init__(self, thermister_type):
        """initialize the thermister resistance and temperature tables for the selected type
        including results from own real life measurements of the B3470 Thermistor."""

        thermister = thermisters[thermister_type]
        self.therm_res = thermister['resistance']
        self.therm_temp = thermister['temperature']
              
    def __str__(self):
        """Returns the NTC's data"""
        rep="Hi, I'm an interpolated Thermistor. These are my parameters:\n"
        #rep+="B Value:"+str(self.B)+"\nNominal Value(kOhm):"+str(self.Rn)+"\nNominal Temperature(C):"+str(self.Tn-273)
        return rep
        


    @property
    def values(self):
        """method to return the current Thermostor parameters if needed"""
        return # self.B,self.Rn,self.Tn  


    
    def RtoT(self,R=10):
        """Returns the interpolated temperature from a measured Thermistor resistance
        Also, only use it within the specifies interval for R, ie. 0.94k->25.5k
        If not, the method will default at R=10"""
        
        #check for valid interval
        if R>=0.94 and R<=25.5:
            self.R=float(R)
        else:
            self.R=float(10)
            
        #define the temp function, interpolated between the two arrays. Use cubic approximation
        #use scipy.interpolate.interp1d for this
        temp=interpolate.interp1d(self.therm_res, self.therm_temp, kind='cubic')
        
        return temp(self.R)


    
    def TtoR(self,T=298):
        """Returns the corresponding resistance from a temperature.
        Also, only use it within the specifies interval for T, ie. 274->371
        If not, the method will default at T=298"""

        #check for valid interval
        if T>=274 and T<=371:
            self.T=float(T)
        else:
            self.T=float(298)
        
        #define the temp function, interpolated between the two arrays. Use cubic approximation
        #use scipy.interpolate.interp1d for this
        res=interpolate.interp1d(self.therm_temp, self.therm_res, kind='cubic')
        
        return res(self.T)



    def Rlin(self,T_hi=343,T_lo=298):
        """Calculates a suitable linearization resistor based on an input
           temperature interval."""

        T_hi=float(T_hi)
        T_lo=float(T_lo)

        #Calculate medium temperature
        T_mid=(T_hi+T_lo)/2

        #Get corresponding resistor values for the interpolated Thermistor
        R_hi=self.TtoR(T_hi)
        R_mid=self.TtoR(T_mid)
        R_lo=self.TtoR(T_lo)
        
        #Calculate Rlin for the interpolated Thermistor
        R_lin=(R_mid*(R_lo+R_hi)-2*R_lo*R_hi)/(R_lo+R_hi-(2*R_mid))

        return R_lin


    def measurement(self, Rlin=2, Rs=2.2, Vs=5, Vadc=2):
        """This method calculates a temperature from a setup as in the schematic and
           presents to temperature values.  It needs 4 input values:
           1) Value of linearization resistor
           2) Value of series resistor
           3) Supply voltage
           4) Measured voltage at the ADC.
           Note, again, that all resistors are in kOhm's.
        """


        Rlin=float(Rlin)
        Rs=float(Rs)
        Vs=float(Vs)
        Vadc=float(Vadc)
        

        #current through the series resistor
        i_rser=(Vs-Vadc)/Rs
        #current through the linearization resistor
        i_rlin=Vadc/Rlin
        #current through the Thermistor
        i_ntc=i_rser-i_rlin
        #Thermistor resistance
        R_ntc=Vadc/i_ntc

        #Temperature based on the measured Thermistor characteristic
        Temp=self.RtoT(R_ntc)

        return Temp
        

if __name__ == "__main__":

    t_type = 'OZ1LQO'
    t_type = 'B3435'
    print 'Interpolated {} thermister'.format(t_type)
    a = Ntc(t_type)
    print ' R=27.348K(0C) = {} C'.format(a.RtoT(27.348) - 273)
    print ' R=22.108K(5C) = {} C'.format(a.RtoT(22.108) - 273)
    print ' R=10.000K(25C) = {} C'.format(a.RtoT(10.0) - 273)
    print ' R=4.1583K(50C) = {} C'.format(a.RtoT(4.1583) - 273)

    tmin = 10
    tmax = 50
    rlin_opt = a.Rlin(T_hi=273+tmax,T_lo=273+tmin)
    print ' {} to {} C range, optimal linearity resistor = {}K'.format(tmin, tmax, rlin_opt)
    rlin = 5.8
    rs = 5.8
    print ' Vadc:1.3V = {} C'.format(a.measurement(Rlin=rlin, Rs=rs, Vs=3.3, Vadc=1.3) - 273)
    print ' Vadc:1.1V = {} C'.format(a.measurement(Rlin=rlin, Rs=rs, Vs=3.3, Vadc=1.1) - 273)
    print ' Vadc:0.8V = {} C'.format(a.measurement(Rlin=rlin, Rs=rs, Vs=3.3, Vadc=0.8) - 273)



    

