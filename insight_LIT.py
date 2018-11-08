#
# for handle rawdata from insight
#
import custom_func_pandas as a
import numpy,datetime
import pandas,operator


file_path0 = '/Users/soncalee/Desktop/UOTA-WiFi-Switch-MP-VendorY-Scorpio-Audit_2018-10-22_10-32-02_v2.csv' #Wifi test
file_path1 = '/Users/soncalee/Desktop/cell-NA.csv' #Cell test
file_path2 = '/Users/soncalee/Desktop/cell-ota_handled_NA.csv' #Cell NA after handle
file_path3 = '/Users/soncalee/Desktop/cell-ota_handled_ROW.csv' #Cell ROW after handle

print('')
print('#This Tool is for handle the rawdata of  Wifi-OTA2 and LIT-OTA2 station.')
print('Usage : Drop the rawdata file to the Terminal window , the file after handled will create on the Desktop. ')
print('')
print('>>Drop the file you wanna hadle in the terminal')
print(	'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
print('')



'''
f_path = input(' ')
print('>>Show File Path : ',f_path)
print('')
'''

#Load CSV
rawdata_csv = a.loadCSV(file_path1)
#rawdata_csv = a.loadCSV(file_path0)
rawdata_array = numpy.array(rawdata_csv)
#first Filter
rawdata_array = a.F_Filter_insight(rawdata_array)
#delete all empty columns
rawdata_array = a.Splitsku(rawdata_array)
rawdata_array = a.SortTRX(rawdata_array)

ex_name='Cell-OTA'

#print('>>>>>',rawdata_array[4][0])

#export path

time = a.WhatTime()
EX_path = './'+ex_name+'_'+time+'.csv'
print('>>Final file path :',EX_path)

final = pandas.DataFrame(rawdata_array)
final.to_csv(EX_path,float_format='%.2f',header = 0,index = 0)
print('>>')

