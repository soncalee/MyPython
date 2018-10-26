'''
This Tool for hadling raw data from PDCA
Edited by GreenHandCoder
'''
import pandas,numpy,scipy,csv

file_path0 = '/Users/soncalee/Desktop/UOTA-WiFi-Switch-MP-VendorY-Scorpio-Audit_2018-10-22_10-32-02_v2.csv' #Wifi test
file_path1 = '/Users/soncalee/Desktop/Germanium-RedSig-OTA-POR-LithiumOTA-2-Octopus-Audit_2018-10-22_13-19-44_v2.csv' #LIT test
ex_f = './Users/soncalee/Desktop/DataAterHandle/1.csv'


''' For Wifi using T to handle Ver.1
raw = pandas.read_csv('./test_wifi_turn.csv') # loading csv by pandas
dataframe = pandas.DataFrame(raw) #DataFrame = 2D array
matrix = numpy.asarray(dataframe) #to ndarray

#row_num = len(raw) #chek how many rows
#columns_num = raw.columns.size #check how many columns 

#just for check
#print(dataframe[dataframe['Serial Number'].str.contains('tc=TxPower;subtc=Avg;subsubtc=Avg')])
raw = dataframe[dataframe['Serial Number'].str.contains('TxPower')]
raw= raw.T

raw.to_csv('./raw_after_handle.csv')
print('finish')
'''

'''
i = 139
while i > 9 :   #test item start at column 9
	print('loop cont:',i)
	#if 'subsubtc=Avg' not in rawdata[1][Ncols]:
		#rawdata= scipy.delete(rawdata,Ncols,1)
		#print('count#',Ncols)
	i -= 1
'''
'''
print('Drop the file your wanna edit in here.')
f2 = input('')
print('this is your file path:',f2)
'''
#/ according SN to find related SKU 
# Sorting test item By frequency low to high

#Set File Path
print('')
print('Drop the file you wanna hadle in the terminal')
print(	'↓↓↓↓↓↓↓↓↓↓↓↓')
print('')
#f_path = input('') 
#print('>>Show File Path : ',f_path)
print('')

#Loading CSV data
file = open(file_path0,'r')
csvR = csv.reader(file)
rawdata = []
for row in csvR:
	rawdata.append(row)

#Data information
print('>>RawData loading...')
print('>>Rows:',len(rawdata),'Columns:',len(rawdata[1]))
print('>>Wipas Ver : ',rawdata[0][1])
print('')

#
i = len(rawdata[1])-1
print('>>Test Items be selected :')
while i > 9 :   #test item start at column 9
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
''''''

rawdata2 = numpy.asarray(rawdata) # as array
print(rawdata2)
#Data Filter
if(Switch == 0):
	print('>>>Wifi Data filtering...')
	while i > 9 :
		#print(i)
		if 'tc=TxPower' and 'subtc=Avg;subsubtc=Avg' in rawdata[1][i]:
			print('>>',i,rawdata[1][i])

			#rawdata = rawdata2.delete(rawdata,10, axis =1)
		i -= 1
else:
	print('>>>LIT Data filtering...')








