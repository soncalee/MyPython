import custom_func_pandas as func
import numpy,datetime
import pandas,operator


file_path0 = '/Users/soncalee/Desktop/UOTA-WiFi-Switch-MP-VendorY-Scorpio-Audit_2018-10-22_10-32-02_v2.csv' #Wifi test
file_path1 = '/Users/soncalee/Desktop/Germanium-RedSig-OTA-POR-LithiumOTA-2-Octopus-Audit_2018-10-22_13-19-44_v2.csv' #Cell test

print('')
print('Drop the file you wanna hadle in the terminal')
print(	'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
print('')


rawdata_csv = func.loadCSV(file_path1)
print(type(rawdata_csv))
rawdata_csv.to_csv('./asdf.csv')
rawdata_array = numpy.array(rawdata_csv)




i = len(rawdata_array[1])-1 # check how many row in the file
# Delete nolimit columns
print (i)
while i > 8 :
	if rawdata_array[2][i] == 'NA' or rawdata_array[6][i] == 'NA' or rawdata_array[6][i] == 'C':
		print('>>[LIMIT]',i,rawdata_array[1][i])
		rawdata_array = numpy.delete(rawdata_array,i,1)
	i -= 1
print('>>[GPS]ROW:',len(rawdata_array),'Columns :',len(rawdata_array[1]))
#
#
#info
#delete limit2 rows
rows = len(rawdata_array)-1
print(rows)
while rows > 1:
	if 'Upper2 Limits----->'== rawdata_array[rows][0] or 'Lower2 Limits----->' == rawdata_array[rows][0] or 'Measurement Unit----->' == rawdata_array[rows][0]:
		rawdata_array = numpy.delete(rawdata_array,rows,axis =0)
		#print('row count: ',rows)
	rows -=1
	
			
raw_info=rawdata_GPS = rawdata_TX = rawdata_RX = numpy.copy(rawdata_array)

###################
#raw information
###################
i = len(raw_info[1])-1
while i > 0:
	if 'Test Start Time' != raw_info[1][i]:
		if 'Station ID' != raw_info[1][i]:
			print('>>[Info]',i,rawdata_TX[1][i])
			raw_info = numpy.delete(raw_info,i,1)
	i -= 1
print('>>[info]ROW:',len(raw_info),'Columns :',len(raw_info[1]))
print('')


#filter GPS data
i = len(rawdata_GPS[1])-1
while i >= 0 :
	if 'tech=GPS' not in rawdata_GPS[1][i]:
		print('>>[GPS]',i,rawdata_GPS[1][i])
		rawdata_GPS = numpy.delete(rawdata_GPS,i,1)
	i -= 1
print('>>[GPS]ROW:',len(rawdata_GPS),'Columns :',len(rawdata_GPS[1]))

##########
#filterTX
##########
i = len(rawdata_TX[1])-1
while i >= 0 :
	if 'TxPower' and 'Avg' not in rawdata_TX[1][i] or 'RxLevel' in rawdata_TX[1][i]:
		print('>>[Tx]',i,rawdata_TX[1][i])
		rawdata_TX = numpy.delete(rawdata_TX,i,1)
	i -= 1
print('>>[Tx]ROW:',len(rawdata_TX),'Columns :',len(rawdata_TX[1]))
#Sort TX

rawdata_TX =rawdata_TX.T
rowTx = len(rawdata_TX)-1
print('rowTx:',rowTx)
while rowTx>=0:
	if 'band=B12' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 1
	if 'band=B13' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 2
	if 'band=B17' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 3
	if 'band=B5' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 5
	if 'band=B2' in rawdata_TX[rowTx][1]:
		if 'band=B26' in rawdata_TX[rowTx][1]:
			rawdata_TX[rowTx][0] = 4
		else:	
			rawdata_TX[rowTx][0] = 6
	if 'band=B25' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 7
	if 'band=B4' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 8
	if 'band=B41' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 9
	if 'band=Band5' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 10
	if 'band=Band4' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 11
	if 'band=Band2' in rawdata_TX[rowTx][1]:
		rawdata_TX[rowTx][0] = 12
	rowTx -=1

rawdata_TX = sorted(rawdata_TX, key=operator.itemgetter(0))
#clean index
rowTx = len(rawdata_TX)-1
while rowTx>=0:
	rawdata_TX[rowTx][0] = None
	rowTx -= 1
#transpose
rawdata_TX = numpy.transpose(rawdata_TX)


##########
#filterRx
#########
i = len(rawdata_RX[1])-1
while i >= 0 :
	if 'RxLevel' and 'Avg_Prm' not in rawdata_RX[1][i]:
		print('>>[Rx]',i,rawdata_RX[1][i])
		rawdata_RX = numpy.delete(rawdata_RX,i,1)
	i -= 1
print('>>[Rx]ROW:',len(rawdata_RX),'Columns :',len(rawdata_RX[1]))

#Sort RX

rawdata_RX =rawdata_RX.T
rowTx = len(rawdata_RX)-1
print('rowRx:',rowTx)
while rowTx>=0:
	if 'band=B12' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 1
	if 'band=B13' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 2
	if 'band=B17' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 3
	if 'band=B5' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 5
	if 'band=B2' in rawdata_RX[rowTx][1]:
		if 'band=B26' in rawdata_RX[rowTx][1]:
			rawdata_RX[rowTx][0] = 4
		else:	
			rawdata_RX[rowTx][0] = 6
	if 'band=B25' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 7
	if 'band=B4' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 8
	if 'band=B41' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 9
	if 'band=Band5' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 10
	if 'band=Band4' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 11
	if 'band=Band2' in rawdata_RX[rowTx][1]:
		rawdata_RX[rowTx][0] = 12
	rowTx -=1
rawdata_RX = sorted(rawdata_RX, key=operator.itemgetter(0))

#clean index
rowTx = len(rawdata_RX)-1
while rowTx>=0:
	rawdata_RX[rowTx][0] = None
	rowTx -= 1

#transpose
rawdata_RX = numpy.transpose(rawdata_RX)

#############
#Merge
############
final_raw = numpy.concatenate((raw_info, rawdata_GPS, rawdata_TX, rawdata_RX), axis=1)
print('>>[Fianl]ROW:',len(final_raw),'Columns :',len(final_raw[1]))




############
#EX
############
now = datetime.datetime.now()
time = now.strftime('%Y-%m-%d-%H-%M-%S')


#Check fianl path 

ex_name = 'Cell-OTA_handled'
path = './'+ex_name+'_'+time+'.csv'
print('>>Final file path :',path)

#final = pandas.DataFrame(rawdata_RX)
final = pandas.DataFrame(final_raw)
final.to_csv(path,float_format='%.2f',header = 0,index = 0)



