#Class to work with NTC Thermistors in Python 2
#Fell free to modify, improve, hack!
#Note! Temperature range is limited to a range between 1 and 98C
#OZ1LQO 2014.05.29

import math

class Model(object):
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


    def Rlin(self,T_hi=343,T_lo=298):
        """Calculates a suitable linearization resistor based on an input
           temperature interval."""

        T_hi=float(T_hi)
        T_lo=float(T_lo)

        #Calculate medium temperature
        T_mid=(T_hi+T_lo)/2

        #Get corresponding resistor values for the modeled Thermistor
        R_hi=self.TtoR(T_hi)
        R_mid=self.TtoR(T_mid)
        R_lo=self.TtoR(T_lo)
        
        #Calculate Rlin for the modeled Thermistor
        R_lin=(R_mid*(R_lo+R_hi)-2*R_lo*R_hi)/(R_lo+R_hi-(2*R_mid))
        
        return R_lin

    def TtoR(self,T=298):
        """Returns the corresponding modeled resistance from a temperature input
           Uses the parameter values given when creating the object: B, Tn, Rn"""
        self.T=float(T)
        return self.Rn*math.exp(self.B*((1/self.T)-(1/self.Tn)))

    def RtoT(self,R=10):
        """Returns the corresponding modeled temperature from a resistance input
           Uses the parameter values given when creating the object: B, Tn, Rn"""
        #check for gross interval
        if R < 0.1:
            self.R = 0.1
        elif R > 1e6:
            self.R = 1e6              
        else:
            self.R=float(R)
        
        return 1/((math.log(self.R/self.Rn)/self.B)+(1/self.Tn))

    
class Circuit(object):
    def __init__(self, ntc, vref, rs, rp):
        """This class calculates a temperature from a setup as in the schematic
           It needs 4 input values:
           1) ntc, ntc object (model or interp) for resistance / temperature conversion
           2) vref, Supply voltage applied to series resistor
           3) rs, Value of series resistor
           4) rp, Value of linearization resistor in paralles with the ntc device
           Note, again, that all resistors are in kOhm's.
        """
        self.ntc = ntc
        self.vref = float(vref)
        self.rs = float(rs)
        self.rlin = float(rp)
        return
    

    #def measurement(self, Rlin=2, Rs=2.2, Vs=5, Vadc=2):
    def from_volts(self, vadc):
        """This method calculates a temperature from a measured voltage
           at the thermister.
           1) Measured voltage at the ADC.
        """

        vadc=float(vadc)
        
        #current through the series resistor
        i_rser=(self.vref-vadc)/self.rs
        #current through the linearization resistor
        i_rlin=vadc/self.rlin
        #current through the Thermistor
        i_ntc=i_rser-i_rlin
        #Thermistor resistance
        try:
            r_ntc=vadc/i_ntc
        except ZeroDivisionError:
            r_ntc = 1e6

        #Finally, get temperature of the Thermistor
        degK=self.ntc.RtoT(r_ntc)

        return degK
        
    
if __name__ == "__main__":
    B = 3435
    Rn = 10 # kOhm
    Tn = 25 # degC
    print('modeled thermister: B25/85={}, Rn={}K, Tn={}degC'.format(B,Rn, Tn))
    
    ntc = Model(B=B, Rn=Rn, Tn=273+Tn)
    print(' R=27.348K(0C) = {} C'.format(ntc.RtoT(27.348) - 273))
    print(' R=22.108K(5C) = {} C'.format(ntc.RtoT(22.108) - 273))
    print(' R=10.000K(25C) = {} C'.format(ntc.RtoT(10.0) - 273))
    print(' R=4.1583K(50C) = {} C'.format(ntc.RtoT(4.1583) - 273))

    tmin = 10
    tmax = 50
    rlin_opt = ntc.Rlin(T_hi=273+tmax,T_lo=273+tmin)
    rlin = 10
    print(' {} to {} C range, optimal linearity resistor = {}K'.format(tmin, tmax, rlin_opt))
    
    vs = 1.5
    rs = 20
    temperature = Circuit(ntc, vs, rs, rlin) 
    print('Rs = {}k, rlin = {}k'.format(rs, rlin))
    for vadc in range(10, 40):
        vadc = vadc/50
        t = temperature.from_volts(vadc) - 273
        print(' Vadc:{}V = {} C'.format(vadc, t))

