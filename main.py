import custom_func as func


file_path0 = '/Users/soncalee/Desktop/UOTA-WiFi-Switch-MP-VendorY-Scorpio-Audit_2018-10-22_10-32-02_v2.csv' #Wifi test
file_path1 = '/Users/soncalee/Desktop/Germanium-RedSig-OTA-POR-LithiumOTA-2-Octopus-Audit_2018-10-22_13-19-44_v2.csv' #Cell test

print('')
print('Drop the file you wanna hadle in the terminal')
print(	'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
print('')
'''
f_path = input(' ') 
print('>>Show File Path : ',f_path)
print('')
'''

rawdata = func.loadCSV(file_path1)
a = func.CheckStation(rawdata)
func.DataFilter(a,rawdata)

#func.EXportCSV(a,rawdata)



