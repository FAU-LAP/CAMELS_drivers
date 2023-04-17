import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import pyvisa
import re

rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB12::12::INSTR')
inst.timeout = 10000
inst.query('U0X')
inst.write('J0X')
inst.write("F0,1X")
inst.write('B0,2,0X')
inst.write('L0.001,0X')
inst.write('G5,2,2X')
inst.write('G13,2,2X')
inst.write("Q1,1,10,0.05,0,0X")
inst.write("T1,0,0,1X")
inst.write('N1X')
inst.write('P0X')
inst.write('H0X')
inst.write("Q1,1,7,0.05,0,0XN1XH0X")
raw_data = inst.read()
read_data = raw_data.split(',')
read_data = np.array(read_data)
volts = []
for x in read_data[::2]:
    try:
        volts.append(float(x))
    except:
        match_result = re.match(r'^(\+\d\d.\d)(\+.*)$', x)
        volts.append(float(match_result[2]))
volts = np.array(volts, dtype=float)
curs = [float(x) for x in read_data[1::2]]
plt.plot(volts,curs, 'x')
plt.plot(volts,volts/15e3)
plt.show()
inst.query('U1X')

print(inst.read())