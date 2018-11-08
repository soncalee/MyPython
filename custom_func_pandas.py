#custom Functions
import csv,pandas,numpy,datetime,scipy,operator
import concurrent.futures
from numba import autojit

#############################
#
# Read CSV file by giving CSV_path
# 
#############################
def loadCSV(CSV_path):
	print('>>[LoadingCSV]')
	path = CSV_path
	file = open(path,'r')
	csvR = csv.reader(file)
	rawdata = []
	for row in csvR:
		rawdata.append(row)
	print('>>Rows:',len(rawdata),'Columns:',len(rawdata[1]))
	print('>>Load CSV done.')
	# Change format to Dataframe
	rawdata1 = pandas.DataFrame(rawdata)
	print('>>Data type :',type(rawdata1))
	return rawdata1
	
################################
#
#Check  the station type .
#
################################
def CheckStation(rawdata):
	print('')
	print('>>[CheckStation]')
	i = len(rawdata[1])-1 # check how many row in the file
	while i >0  :   #test item start at column 9
		#print('loop cont:',i)
		if 'tech=BT' in rawdata[1][i]:
			print('>>Station : Wifi-OTA2')
			print('>>Wipas Ver : ',rawdata[0][1])
			#i = len(rawdata[1])-1
			Switch = 0
			break
		if 'tech=GPS' in rawdata[1][i]:
			print('>>Station : LIT-OTA2')
			print('>>Wipas Ver : ',rawdata[0][1])
			#i = len(rawdata[1])-1
			Switch = 1
			break
		i -=1

	print('>>Switch (0= WiFi, 1 =LTE )=',Switch)
	print('>>[CheckStation] Done.')
	print('')
	return Switch



#########################################
#F_Filter
#	Delte columns :
#		1. which have no limit
#		2. Measurment have no unit
#		3.Battery test item	(measurement unit = c)
#	
#	Delete rows:
#		1.Limits 2
#		2.Measurement Unit
#########################################
@autojit 
def F_Filter_insight(array):
	#with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
	print('>>F_Filter')
	numpy_array = numpy.array(array)
	i = len(numpy_array[1])-1 # check how many row in the file

	# Delete nolimit columns
	while i >= 12 :
		if numpy_array[4][i]=='NA' or numpy_array[5][i]=='NA'or numpy_array[6][i]!='dBm':
			#kepp the columns you want
			print('>>[1]i_count:',i, numpy_array[1][i])
			numpy_array = numpy.delete(numpy_array,i,1)
		i -= 1
	#
	i=11
	while 1<i < 12 :
		if numpy_array[1][i] == 'Unit Number'or numpy_array[1][i] == 'List of Failing Tests'or numpy_array[1][i] == 'Special Build Name':
			print('>>[2]i_count:',i, numpy_array[1][i])
			numpy_array = numpy.delete(numpy_array,i,1)
		i -= 1
	print('>>[Delete1]Rows:',len(numpy_array),'Columns: ',len(numpy_array[1]))
	
	#delete limit2 rows
	print('>>Delete Rows')
	rows = len(numpy_array)-1
	while rows > 1:
		if 'Display Name ----->'== numpy_array[rows][0] or 'PDCA Priority ----->' == numpy_array[rows][0]: # or 'Measurement Unit ----->' == numpy_array[rows][0]
			numpy_array = numpy.delete(numpy_array,rows,axis =0)
			print('>>Rows_count: ',rows,numpy_array[rows][0])
		rows -=1
	print('>>[Delete2]Rows:',len(numpy_array),'Columns: ',len(numpy_array[1]))
	array = numpy_array
	print('>>[F_Filter] Done')
	print('')
	return array

#########################################
#
#Data_info
#	Keep 1.Test Start Time & Station ID
#		
#########################################
def Data_info(array):
	print('>>Data_info')
	array_info = numpy.array(array)
	i = len(array_info[1])-1
	while i > 0:
		if 'Test Start Time' != array_info[1][i]:
			if 'Station ID' != array_info[1][i]:
				#print('>>[Info]',i,array_info[1][i])
				array_info = numpy.delete(array_info,i,1)
		i -= 1
	print('>>[info]ROW:',len(array_info),'Columns :',len(array_info[1]))
	print('>>[Data_info] Done')
	print('')
	array = array_info
	return array


#########################################
#
#	Keep GPS test case
#		
#########################################
def KeepGPS(array):
	print('>>KeepGPS')
	array_GPS = numpy.array(array)
	i = len(array_GPS[1])-1
	while i >= 0 :
		if 'tech=GPS' not in array_GPS[1][i]:
			#print('>>[GPS]',i,array_GPS[1][i])
			array_GPS = numpy.delete(array_GPS,i,1)
		i -= 1
	print('>>[GPS]ROW:',len(array_GPS),'Columns :',len(array_GPS[1]))
	print('>>[KeepGPS] Done.')
	return array


#########################################
#
#	Handle LTE-TX
#		
#########################################
def HandleTX(array):
	print('>>HandleTX')
	tx_array = numpy.array(array)
	i = len(tx_array[1])-1
	while i >= 0 :
		if 'TxPower' and 'Avg' not in tx_array[1][i] or 'RxLevel' in tx_array[1][i]:
			#print('>>[Tx]',i,sort_array[1][i])
			tx_array = numpy.delete(tx_array,i,1)
		i -= 1
	print('>>[HandleTX]ROW:',len(tx_array),'Columns :',len(tx_array[1]))

	#Sort test-case by frequency
	array = SortByFreq(tx_array)
	return array
	print('>>[HandleTX] Done')
	


#########################################
#
#	Handle LTE-RX
#		
#########################################
def HandleRX(array):
	rx_array = numpy.array(array)
	i = len(rx_array[1])-1
	while i >= 0 :
		if 'RxLevel' and 'Avg_Prm' not in rx_array[1][i]:
			#print('>>[Rx]',i,rx_array[1][i])
			rx_array = numpy.delete(rx_array,i,1)
		i -= 1
	print('>>[HandleRX]ROW:',len(rx_array),'Columns :',len(rx_array[1]))

	#Sort test-case by frequency
	array = SortByFreq(rx_array)
	return array
	print('>>[HandleRX] Done')

#########################################
#
#	Sort test-case By Freq from L to H
#		
#########################################
def SortByFreq(array):
	print('')
	print('>>SortByFreq')
	sort_array = numpy.array(array)
	sort_array =sort_array.T
	row_count = len(sort_array)-1
	print('row_count:',row_count)
	while row_count>=0:
		if 'band=B12' in sort_array[row_count][1]:
			sort_array[row_count][0] = 1
		if 'band=B13' in sort_array[row_count][1]:
			sort_array[row_count][0] = 2
		if 'band=B17' in sort_array[row_count][1]:
			sort_array[row_count][0] = 3
		if 'band=B5' in sort_array[row_count][1]:
			sort_array[row_count][0] = 5
		if 'band=B2' in sort_array[row_count][1]:
			if 'band=B26' in sort_array[row_count][1]:
				sort_array[row_count][0] = 4
			else:	
				sort_array[row_count][0] = 6
		if 'band=B25' in sort_array[row_count][1]:
			sort_array[row_count][0] = 7
		if 'band=B4' in sort_array[row_count][1]:
			sort_array[row_count][0] = 8
		if 'band=B41' in sort_array[row_count][1]:
			sort_array[row_count][0] = 9
		if 'band=Band5' in sort_array[row_count][1]:
			sort_array[row_count][0] = 10
		if 'band=Band4' in sort_array[row_count][1]:
			sort_array[row_count][0] = 11
		if 'band=Band2' in sort_array[row_count][1]:
			sort_array[row_count][0] = 12
		row_count -=1

	sort_array = sorted(sort_array, key=operator.itemgetter(0))
	#clean index
	row_count = len(sort_array)-1
	while row_count>=0:
		sort_array[row_count][0] = None
		row_count -= 1
	#transpose
	sort_array = numpy.transpose(sort_array)
	return sort_array
	print('>>[SortByFreq] Done')
	print('')


#########################################
#
#	Check current time
#		
#########################################
def WhatTime():
	now = datetime.datetime.now()
	time_now = now.strftime('%Y-%m-%d-%H-%M-%S')
	return time_now

################################
#
#	Handle WiFi
#
################################
def HandleWifi(array):
	print('>>Handle Wifi')
	wifi_array = numpy.array(array)

	i = len(wifi_array[1])-1 # check how many row in the file
	while i >= 0 :
		if 'subtc=Avg' and 'subsubtc=Avg' not in wifi_array[1][i] or 'tc=Pathloss' in wifi_array[1][i]:
			print('>>',i,wifi_array[1][i])
			wifi_array = numpy.delete(wifi_array,i,1)
		i -= 1

	print('>>[Handle Wifi] Done.')
	array = wifi_array
	return array

########################################################
#
#	Splitsku
#		Delete the the test case columns which = None
#
########################################################
@autojit
def Splitsku(array):
	print('>>Split')
	rawdata = numpy.array(array)
	print('>>ROW:',len(rawdata),'col:',len(rawdata[1]))
	row = len(rawdata)-1
	col = len(rawdata[1])-1
	i=2
	while row>4:
		while col>9:
			i=2
			if rawdata[row][col] =='':
				#check other section value wether None or not.
				while 0<=i<=2:
					#print('iicount:',i)
					if rawdata[row-i][col] =='':
						if i==0:
							print('[i-count]:',col,rawdata[1][col])
							rawdata = numpy.delete(rawdata,col,axis=1)							
					i-=1	
			col -=1
		row -=1
	print('>>[finish]ROW:',len(rawdata),'col:',len(rawdata[1]))
	array = rawdata
	return array

########################################################
#
#	SortTRX
#		Sorting the test case of Tx and Rx by function->freq->domain
#
########################################################
@autojit
def SortTRX(array):
	print('>>SortTRX')
	sort_array = numpy.array(array)
	sort_infor = sort_testcase = sort_array

	#find the col of the test case sarting
	index =  numpy.where(sort_array == 'Version') 
	start_col = index[1]

	#split information part and test part
	#	keep info:
	col_len = len(sort_array[1])-1
	while col_len>start_col:
		sort_infor = numpy.delete(sort_infor,col_len,axis=1)
		col_len -=1
	print('>>[raw_infor]>ROW:',len(sort_infor),'col:',len(sort_infor[1]))
	
	#	keep test case part:
	col_len = len(sort_testcase[1])-1
	while col_len>=0:
		if col_len <=start_col:
			#print('col_len : ',col_len)
			sort_testcase = numpy.delete(sort_testcase,col_len,axis=1)
		col_len -=1
	print('>>[raw_testcase]>ROW:',len(sort_testcase),'col:',len(sort_testcase[1]))
	#print('>>>>>>',sort_testcase[1][:])
	i=0
	#Sort Tx Rx 
	col_len = len(sort_testcase[1])-1
	while col_len>=0:
		# sort Tx
		if 'tcTP' in sort_testcase[1][col_len]:
			#print('>>Sorting Tx')
			if 'tUMTSbBAND5c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 1
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND8c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 2
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND4c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 3
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND2c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 4
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND1c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 5
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB12c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 6
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB17c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 7
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB13c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 8
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB18c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 9
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB26c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 10
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB5c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 11
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB19c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 12
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB20c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 13
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB8c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 14
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB4c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 15
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB66c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 16
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB3c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 17
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB2c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 18
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB25c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 19
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB1c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 20
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB7c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 21
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB39c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 22
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB40c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 23
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB41c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 24
				print('>> [sorting test case]',col_len,sort_testcase[1][col_len])

		# sort Rx
		if 'tcRL' in sort_testcase[1][col_len]:
			if 'tUMTSbBAND5c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 25
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND8c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 26
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND2c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 27
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND4c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 28
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tUMTSbBAND1c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 29
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB12c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 30
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB17c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 31
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB13c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 32
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB20c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 33
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB18c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 34
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB26c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 35
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB5c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 36
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])							
			if 'tLTEbB19c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 37
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB8c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 38
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB3c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 39
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB2c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 40
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB25c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 41
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB4c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 42
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB1c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 43
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB66c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 44
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB7c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 45
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB39c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 46
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB40c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 47
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
			if 'tLTEbB41c' in sort_testcase[1][col_len]:
				sort_testcase[0][col_len]= 48
				print('>>[sorting test case]',col_len,sort_testcase[1][col_len])
		col_len-=1

	#execute sorting
	sort_testcase = numpy.transpose(sort_testcase)
	sort_testcase = sorted(sort_testcase, key=operator.itemgetter(0))

	#clean sorting index
	row_count = len(sort_testcase)-1
	while row_count>=0:
		sort_testcase[row_count][0] = None
		row_count -= 1
	sort_testcase = numpy.transpose(sort_testcase)	
	
	
	#combine data
	sort_array = numpy.concatenate((sort_infor, sort_testcase), axis=1)
	
	print('>>[finish]ROW:',len(sort_array),'col:',len(sort_array[1]))
	array = numpy.array(sort_array)
	return array
