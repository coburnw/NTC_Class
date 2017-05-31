#Class to work with NTC Thermistors in Python 2
#Fell free to modify, improve, hack!
#Note! Temperature range is limited to a range between 1 and 98C
#OZ1LQO 2014.05.29

import math
#from scipy import interpolate




class Ntc(object):
    """A class to work with NTC Thermistors.
    Input, is B, Rn (resistance at Tn), Tn (normalized temperature).
    For the B3470 Thermistor that should be B=3470, Rn=10k, Tn=298.
    Ie. a=Ntc(3470,10,298)
    This Class uses the theoretical formulas for a modeled NTC Thermistor.
    All temperatures are in degrees Kelvin and all resistance values are in kilo ohms"""

    def __init__(self, B, Rn, Tn):
        """initialize the NTC with the theoretical parameters"""
  
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


    def TtoR(self,T=298):
        """Returns the corresponding modeled resistance from a temperature input
           Uses the parameter values given when creating the object: B, Tn, Rn"""
        self.T=float(T)
        return self.Rn*math.exp(self.B*((1/self.T)-(1/self.Tn)))


    def RtoT(self,R=10):
        """Returns the corresponding modeled temperature from a resistance input
           Uses the parameter values given when creating the object: B, Tn, Rn"""
        #check for valid interval
        if R>=0.94 and R<=25.5:
            self.R=float(R)
        else:
            self.R=float(10)
        
        return 1/((math.log(self.R/self.Rn)/self.B)+(1/self.Tn))

    
    def Rlin(self,T_hi=343,T_lo=298):
        """Calculates a suitable linearization resistor based on an input
           temperature interval. Returns two resistor values:
           R_lin_model is
           based on a modeled Thermistor based on the input values when the object was
           instantiated. Otherwise there may still be some differences
           between the two resistors"""

        T_hi=float(T_hi)
        T_lo=float(T_lo)

        #Calculate medium temperature
        T_mid=(T_hi+T_lo)/2

        #Get corresponding resistor values for the modeled Thermistor
        R_hi=self.TtoR_calc(T_hi)
        R_mid=self.TtoR_calc(T_mid)
        R_lo=self.TtoR_calc(T_lo)
        
        #Calculate Rlin for the modeled Thermistor
        R_lin_model=(R_mid*(R_lo+R_hi)-2*R_lo*R_hi)/(R_lo+R_hi-(2*R_mid))
        

        return R_lin_model


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

        #Temperature based on the modeled Thermistor
        Temp_mod=self.RtoT_calc(R_ntc)

        return Temp_meas,Temp_mod
        
    
if __name__=="__main__":
    print """This is an NTC Thermistor library.
You are supposed to import it and create Thermistor objects"""


    

