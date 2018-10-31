
import pandas,numpy,csv
import scipy as spy




file_path0 = '/Users/soncalee/Desktop/UOTA-WiFi-Switch-MP-VendorY-Scorpio-Audit_2018-10-22_10-32-02_v2.csv' #Wifi test
file_path1 = '/Users/soncalee/Desktop/Germanium-RedSig-OTA-POR-LithiumOTA-2-Octopus-Audit_2018-10-22_13-19-44_v2.csv' #Cell test
ex_f = './Users/soncalee/Desktop/raw_filtered.csv'

#Set File Path
'''
print('')
print('Drop the file you wanna hadle in the terminal')
print(	'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
print('')
f_path = input(' ') 
print('>>Show File Path : ',f_path)
print('')
'''

#
#
#Loading CSV data
file = open(file_path1,'r')
csvR = csv.reader(file)
rawdata = []
for row in csvR:
	rawdata.append(row)

#
#
#Data information
print('>>RawData loading...')
print('>>Rows:',len(rawdata),'Columns:',len(rawdata[1]))
print('>>Wipas Ver : ',rawdata[0][1])
print('')

#
i = len(rawdata[1])-1
print('>>Test Items be selected :')
# judge what is the station type of the rawdata
# 
while i > 8 :   #test item start at column 9
	#print('loop cont:',i)
	if 'tech=BT' in rawdata[1][i]:
		#rawdata = numpy.delete(rawdata,i,1)
		print('>>Station : Wifi-OTA2')
		print('>>Execute WiFi station selecting...')
		i = len(rawdata[1])-1
		Switch = 0
		break
	if 'tech=GPS' in rawdata[1][i]:
		print('>>Station : LIT-OTA2')
		print('>>Execute LIT station selecting...')
		i = len(rawdata[1])-1
		Switch = 1
		break
	i -=1
print('')
print('>>Switch =',Switch)

#Data Filter :  Switch = 0=Wifi, Switch = 1 = Cell
if(Switch == 0):
	print('>>>Wifi Data filtering...')
	while i > 8 :
		#print(i)
		if 'subtc=Avg;subsubtc=Avg' not in rawdata[1][i] or 'tc=Pathloss' in rawdata[1][i]:
			print('>>',i,rawdata[1][i])
			Rows = len(rawdata)-1
			while Rows > 0:
				del rawdata[Rows][i]
				Rows -= 1
		i -= 1
else:
	print('>>>Cell Data filtering...')
	while i > 9 :
		if 'tech=GPS' and 'subtc=Avg' not in rawdata[1][i]:
			print('>>',i,rawdata[1][i])
			Rows = len(rawdata)-1
			while Rows > 0:
				del rawdata[Rows][i]
				Rows -= 1
		i -= 1
print('>>Rows:',len(rawdata),'Columns:',len(rawdata[1]))
print('>>')
print('>>>')

#print(rawdata)


#
#Create a new csv after filter

csvfile = open('./after.csv','w')
print(ex_filename)
#a = csv.writer(csvfile)
#a.writerows(rawdata)
#print(csvfile)
#csvfile.close()
print('>>Done.')


