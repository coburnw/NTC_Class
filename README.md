NTC_Class
=========
Heavily refactored:
  * split into two folders: py2 and py3 (I dont use py3, so py3 folder unchanged from Soren's original code.)
  * split into two classes: modeled and interpolated
  * Added dictionaries for holding named tables of thermister data for interpolation.
  * Added B3435 table.

among other things this eliminates the need to install the scipy
package when modeled results are acurate enough for the job at hand.

Many thanks to Soren.  My setpoint units would still be in volts without his effort.

(cw)

A Py3 toolbox to handle NTC Thermistor measurement with an ADC.
You'll find the library, a script to test all the functionality,
a spreadsheet with all my sims and calcs, and a small schematic on
how to set up a temperature sensor circuit.

See my other repository on RasPI NTC DAC handling, to get an idea on
how to use it. 

UPDATE - Just ported the library to Python 2.7 and tested it live on my 
RasPI, using an ADC from Abelectronics. Works fine.
Updated the repo with some sample code for RasPI and the ADC along with a
screenshot of a sample run :-)


Have fun!!
