#Class to work with NTC Thermistors in Python 2
#Fell free to modify, improve, hack!
#Note! Temperature range is limited to a range between 1 and 98C
#OZ1LQO 2014.05.29

import math
from scipy import interpolate




class Ntc(object):
    """A class to work with NTC Thermistors.
    Input, is B, Rn (resistance at Tn), Tn (normalized temperature).
    For the B3470 Thermistor that should be B=3470, Rn=10k, Tn=298.
    Ie. a=Ntc(3470,10,298)
    The Class can be used with measured values (B3470 only) as well as with the
    theoretical formulas for NTC Thermistor.
    All temperatures are in degrees Kelvin and all resistance values are in kilo ohms"""

    def __init__(self, B, Rn, Tn):
        """initialize the NTC with the parameters
        including results from own real life measurements of the B3470 Thermistor."""
        self.B=float(B)
        self.Rn=float(Rn)
        self.Tn=float(Tn)
              
    def __str__(self):
        """Returns the NTC's data"""
        rep="Hi, I'm an NTC Thermistor. These are my parameters:\n"
        rep+="B Value:"+str(self.B)+"\nNominal Value(kOhm):"+str(self.Rn)+"\nNominal Temperature(C):"+str(self.Tn-273)
        return rep
        


    @property
    def values(self):
        """method to return the current Thermostor parameters if needed"""
        return self.B,self.Rn,self.Tn  


    
    def RtoT_meas(self,R=10):
        """Returns the corresponding temperature from a measured Thermistor resistance
        This is ONLY accurate when using the B3470 Thermistor
        Also, only use it within the specifies interval for R, ie. 0.94k->25.5k
        If not, the method will default at R=10"""
        
        #check for valid interval
        if R>=0.94 and R<=25.5:
            self.R=float(R)
        else:
            self.R=float(10)
            
        #Define resistance vs. temperature arrays for the interpolate function
        #X should always be ascending
        res_x=[0.94, 1.04, 1.16, 1.32, 1.52, 1.74, 2.03, 2.33, 2.71, 3.16, 3.73, 4.43, 5.2,
               6.2, 7.5, 9.8, 11.28, 13.5, 16.15, 18.5, 25.5]
        temp_y=[371, 368, 363, 358, 353, 348, 343, 338, 333, 328, 323, 318, 313, 308, 303,
                298, 293, 288, 283, 278, 274]
        #define the temp function, interpolated between the two arrays. Use cubic approximation
        #use scipy.interpolate.interp1d for this
        temp=interpolate.interp1d(res_x,temp_y,kind='cubic')
        
        return temp(self.R)


    
    def TtoR_meas(self,T=298):
        """Returns the corresponding resistance from a temperature.
        This is ONLY accurate when using the B3470 Thermistor.
        Also, only use it within the specifies interval for T, ie. 274->371
        If not, the method will default at T=298"""

        #check for valid interval
        if T>=274 and T<=371:
            self.T=float(T)
        else:
            self.T=float(298)
        
        #Define temperature vs. resistance arrays for the interpolate function
        #X should always be ascending
        temp_x=[274, 278, 283, 288, 293, 298, 303, 308, 313, 318, 323, 328, 333, 338, 343,
        348, 353, 358, 363, 368, 371]
        res_y=[25.5, 18.5, 16.15, 13.5, 11.28, 9.8, 7.5, 6.2, 5.2, 4.43, 3.73, 3.16, 2.71,
               2.33, 2.03, 1.74, 1.52, 1.32, 1.16, 1.04, 0.94]
        #define the temp function, interpolated between the two arrays. Use cubic approximation
        #use scipy.interpolate.interp1d for this
        res=interpolate.interp1d(temp_x,res_y,kind='cubic')
        
        return res(self.T)



    def Rlin(self,T_hi=343,T_lo=298):
        """Calculates a suitable linearization resistor based on an input
           temperature interval. Returns resistor value for:
           R_lin_meas is based on the measured B3470 characteristic 
           NOTE! If you're using another Thermistor than B3470,
           R_lin_meas will be invalid."""

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
           presents to temperature values, one based on the measured B3470 resistor and
           one for the modeled. It needs 4 input values:
           1) Value of linearization resistor
           2) Value of series resistor
           3) Supply voltage
           4) Measured voltage at the ADC.
           Note, again, that all resistors are in kOhm's and if you're using another
           Thermistor than B3470, the Temp_meas will be invalid.
           Otherwise there may still be some differences between the measured and the
           calculated thermistor"""


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
        
    

        
    

         


if __name__=="__main__":
    print """This is an NTC Thermistor library.
You are supposed to import it and create Thermistor objects"""


    

