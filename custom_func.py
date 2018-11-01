#custom Functions
import csv,pandas,numpy,datetime,scipy

#############################
# Read CSV file by giving CSV_path
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
	return rawdata
	

#############################
#Check what's the station type .
#############################
def CheckStation(rawdata):
	print('')
	print('>>[CheckStation]')
	i = len(rawdata[1])-1 # check how many row in the file

	while i > 8 :   #test item start at column 9
		#print('loop cont:',i)
		if 'tech=BT' in rawdata[1][i]:
			#rawdata = numpy.delete(rawdata,i,1)
			print('>>Station : Wifi-OTA2')
			print('>>Wipas Ver : ',rawdata[0][1])
			i = len(rawdata[1])-1
			Switch = 0
			break
		if 'tech=GPS' in rawdata[1][i]:
			print('>>Station : LIT-OTA2')
			print('>>Wipas Ver : ',rawdata[0][1])
			i = len(rawdata[1])-1
			Switch = 1
			break
		i -=1
	print('>>CheckStation Done.')
	print('>>Switch =',Switch)
	print('')
	return Switch



#############################
#Fliter unnecessary test cases
#############################
def DataFilter(switch,rawdata):
	print('>>[DataFilter]')
	if(switch == 0):
		print('>>>Wifi Data filtering...')
		Handle_Wifi(rawdata)
	else:
		print('>>>LIT-OTA2 Data filtering...')
		KeepAVG_deleNA(rawdata)
		rawdata = Handle_LIT(rawdata)
	print('>>DataFilter Done.')
	return rawdata



#############################
# Export CSV file to Desktop
#############################
def EXportCSV(a,rawdata):
	print('')
	if a == 0:
		ex_name = 'UOTA-WiFi_handled'
	else:
		ex_name = 'Cell-OTA_handled'
	print(ex_name)
	print('>>[ExportCSV]')

	#Check what time it is
	now = datetime.datetime.now()
	time = now.strftime('%Y-%m-%d-%H-%M-%S')

	#Check fianl path 
	path = './'+ex_name+'_'+time+'.csv'
	print('>>Final file path :',path)

	csvfile = open(path,'w')
	a = csv.writer(csvfile)
	a.writerows(rawdata)
	csvfile.close()
	print('>>Done.')


#############################
# FirstFilter : 
#############################
#delete the test case of upper & lower =NA and keep Avg power
def KeepAVG_deleNA(rawdata):
	print('>>[KeepAVG_deleNA]')
	i = len(rawdata[1])-1 # check how many row in the file
	#print(rawdata[2][130])
	while i > 8 :
		if rawdata[2][i] == 'NA' or rawdata[6][i] == 'NA' or rawdata[6][i] == 'C':
			#print('>>',i,rawdata[1][i])
			Rows = len(rawdata)-1
			while Rows >0:
				del rawdata[Rows][i]
				Rows -= 1
		i -= 1
	print('>>Dlete NA for upper & lower Done.')
	print('>>[After KeepAVG_deleNA] Rows:',len(rawdata),'Columns:',len(rawdata[1]))
	print()
	return rawdata



#############################
# Handle_Wifi
#############################
def Handle_Wifi(rawdata):
	print('>>>[Handle_Wifi]')
	i = len(rawdata[1])-1 # check how many row in the file
	while i > 8 :
		if 'subtc=Avg;subsubtc=Avg' not in rawdata[1][i] or 'tc=Pathloss' in rawdata[1][i]:
			print('>>',i,rawdata[1][i])
			Rows = len(rawdata)-1
			while Rows > 0:
				del rawdata[Rows][i]
				Rows -= 1
		i -= 1
	print('>>[Handle_Wifi] Done.')
	return rawdata


#############################
# Handle_LIT
#############################
def Handle_LIT(rawdata):
	print('')
	print('>>[Handle_LIT]')
	i = len(rawdata[1])-1 # check how many row in the file
	rawdata_GPS = rawdata


	#1.keep GPS data as head
	print('>>Keep GPS')
	while i > 8 :
		if 'tech=GPS' not in rawdata_GPS[1][i] :
			print('>>[GPS]',i,rawdata_GPS[1][i])
			Rows = len(rawdata_GPS)-1
			while Rows >0:
				del rawdata_GPS[Rows][i]
				Rows -= 1
		i -= 1
	print('>>[GPS]Rows:',len(rawdata_GPS),'Columns:',len(rawdata_GPS[1]))
	#print('>>[TXRX]Rows:',len(rawdataTXRX),'Columns:',len(rawdataTXRX[1]))
	print(rawdata[])



