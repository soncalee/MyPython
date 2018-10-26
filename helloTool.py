'''
This Tool for hadling raw data from PDCA
Edited by GreenHandCoder
'''
import pandas,numpy,scipy,csv
file_path = 'UOTA-WiFi-Switch-MP-VendorY-Scorpio-Audit_2018-10-22_10-32-02_v2.csv'
ex_f = './data_after_handle.csv'

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

file = open(file_path,'r')
csvR = csv.reader(file)
Title = []
rawdata = []
Testdata = []
for row in csvR:
	rawdata.append(row)
rawdata2= []
i = 139


while i > 9 :   #test item start at column 9
	#print('loop cont:',i)
	if 'tc=TxPower;subtc=Avg;subsubtc=Avg' in rawdata[1][i]:
		rawdata = scipy.delete(rawdata,i,1)
		print('Col_lable:',i,',',rawdata[1][i])
	i -=1

