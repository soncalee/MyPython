#custom Functions
import csv

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
	return Switch



#############################
#Fliter unnecessary test cases
#############################
def DataFilter(switch,rawdata):
	print('>>[DataFilter]')
	if(switch == 0):
		print('>>>Wifi Data filtering...')
		i = len(rawdata[1])-1 # check how many row in the file
		while i > 8 :
			if 'subtc=Avg;subsubtc=Avg' not in rawdata[1][i] or 'tc=Pathloss' in rawdata[1][i]:
				print('>>',i,rawdata[1][i])
				Rows = len(rawdata)-1
				while Rows > 0:
					del rawdata[Rows][i]
					Rows -= 1
			i -= 1
	else:
		print('>>>Cell Data filtering...')
		i = len(rawdata[1])-1 # check how many row in the file
		while i > 9 :
			if 'tech=GPS' and 'subtc=Avg' not in rawdata[1][i]:
				print('>>',i,rawdata[1][i])
				Rows = len(rawdata)-1
				while Rows > 0:
					del rawdata[Rows][i]
					Rows -= 1
			i -= 1
	print('>>DataFilter Done.')
	return rawdata



#############################
# Export CSV file to Desktop
#############################
def EXportCSV(a,rawdata):
	print('')
	if a == 0:
		ex_name = 'UOTA-WiFi_handled.csv'
	else:
		ex_name = 'Cell-OTA_handled.csv'
	print(ex_name)
	print('>>[ExportCSV]')
	path = './'+ex_name
	
	csvfile = open(path,'w')
	a = csv.writer(csvfile)
	a.writerows(rawdata)
	#print(csvfile)
	csvfile.close()
	print('>>Done.')



#############################
# Split
#############################