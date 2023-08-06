"""
Program : LucidControl
Version : 0.1
last update : Feb. 18th 2019
by : andreas.westhoff@dlr.de
"""

import VoltageCtrl as LuCtrl
import time

fan01 = LuCtrl.VoltageCtrl(port='/dev/ttyACM2')
voltage = 0
channel = 0
cuvolt = fan01.get_voltage()
while voltage != 999:
    try:
        channel = int(input('Channel No [0..3] : '))
    except:
        channel = channel
    try:
        voltage = float(input('Voltage [0..10] : '))
    except:
        voltage = cuvolt[channel]
    if (isinstance(channel, int)) and (isinstance(voltage, float)):
        fan01.set_voltage(channel, voltage)
    time.sleep(0.5)
    cuvolt = fan01.get_voltage()
    print ('#################################################################')
    for ch in range(4):
        print('CHANNEL ' + str(ch) + ' : ' + str(cuvolt[ch]))
    print ('#################################################################')


for ch in range(4):
    fan01.set_voltage(ch, 0)

