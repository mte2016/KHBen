import re
import os
import datetime

from ConfigParser import SafeConfigParser
#KHBen_1
#KHBen_1
#KHBen_1
#KHBen_1

import _ug_lib.ugLog
import _ug_lib.ugPN
#----------------------------

HOME = 'C:\Python27_1\New folder'

#-----------------------------

DEBUG = False

class SM:
	def __init__(self):
		self._sn = ""
		self.fw = ""
		self._log = _ug_lib.ugLog.Log()
		self.logfile_open()
		
	def logfile_open(self):
		parser = SafeConfigParser()
		parser.read(HOME + "/config.ini")
		self.TESTER = parser.get('TESTER', 'id')
		self.WO = parser.get('TEST', 'wo')
		self.PN = parser.get('TEST', 'pn')
		date = datetime.datetime.today().strftime("%Y%m%d")
		rootdir = HOME + '\\' + self.PN + '\LogFile' + '\\' + date
#		print rootdir
		self.FW_Get(rootdir, self.PN)
		
	def parsefile(self, f):
		lst_of_dict =[]
		header=[]
		row_idx = 0
		startparse = False
		dict = {}
		for i,line in enumerate(f):
#			look for the following line where data follows
# **************************  Port1     Port2     Port3     Port4     Port5     Port6     Port7     Port8     Port9     Port10     Port11     Port12     Port13     Port14     Port15     Port16

			if re.search(r'Port', line) is not None:
				startparse = True
			if startparse:
				if row_idx == 0:
					#	parse the following line, getting rid of space and "Port" to get a list port#: "**...","2", "3":, ...
# **************************  Port1     Port2     Port3     Port4     Port5     Port6     Port7     Port8     Port9     Port10     Port11     Port12     Port13     Port14     Port15     Port16
					header = line.strip().split().split("Port")
					for i in seq_iter(header):				
						dict[header[i]] = "0"

				elif row_idx > 0:
#Clear S.M.A.R.T. and UnFormat Fail(15)      0         1         0         0         0         0         0         0         0          0          0          0          0          0          0          0     
#    Check PreTest Fail(33)      1         2         0         2         0         0         0         0         0          0          0          0          0          0          0          0     
#    Check PreTest Fail(33)      1         2         0         2         0         0         0         0         0          0          0          0          0          0          0          0     
#    Check PreTest Fail(33)      1         2         0         2         0         0         0         0         0          0          0          0          0          0          0          0     

#					split line to list like:
#    						"Check PreTest Fail(33)","1","   2", "   0", ....
					lineItms = line.strip().split("      ")
					

#					remove any space ONLY in port value to get the following list:
#    						"Check PreTest Fail(33)","1","2", "0", ....

#					if "         " in line[i:]:
#						line = line[0].split("         ")
					for i in seq_iter(lineItms):				
						if i > 0:
							lineItms[i] = lineItms[i].split()
						
#					col_idx = 0
#					for col in line:
#						dict[header[int(col_idx)]] = col
#					#	print "col_idx", col_idx, col
#						col_idx += 1
#					lst_of_dict.append(dict);
#				row_idx += 1

#					put value into dict if not 0
					for i in seq_iter(lineItms):				
						if i > 0:
							if lineItms[i] <> "0" AND dict[i] <> "0":
								dict[i] = lineItms[0]
					


		f.close()
		self.testcasecheck(lst_of_dict)
				
	def testcasecheck(self, lst_of_dict):
		log = _ug_lib.ugLog.Log()
		#print lst_of_dict
		slotid = re.findall(r'\d+)', row)
		slotnum = []
		for i, row in enumerate(lst_of_dict):
			for x in lst_of_dict[i]:
				if slotid != '   0':
					slotid = str(x)
					TEST = lst_of_dict[i]['**************************']
					rslt = 'Fail:'
					self._log.add(self._sn, slotid, rslt, TEST)
					self._log.write(self.WO, self.PN + ".ini", self.TESTER, _ug_lib.ugPN.PN_Capacity(self.PN), self.fw)
					break


	
	def slotcheck(self, line):
		matchSlot = re.findall(r'(\d+)',line)
		slotnum = []
		if matchSlot:
			for i,x in enumerate(matchSlot[1:]):
				if x != '0':
					slotnum.append(i)
			slotnum[:] = [x+1 for x in slotnum]
		return slotnum
	
	def resultcheck(self, slotnum):
		slotid = ""
		if len(slotnum) == 0:
			slotnum.append(0)
			rslt = "Passed"
		else:
			rslt = "Fail: "
			slotid = str(slotnum).strip('{}')
		return rslt
	
	def logpass(self, rslt, slotid, matchTest):
		for i,x in enumerate(slotid):
			if rslt.startswith("Passed"):
				prereq = True
			else:
				prereq = False
				self._log.add(self._sn, str(slotid[i]), rslt, matchTest)
				self._log.write(self.WO, self.PN + ".ini", self.TESTER, _ug_lib.ugPN.PN_Capacity(self.PN), self.fw)
		return prereq

	def FW_Get(self,_file, PN):
		fw = ""
		for subdir, dirs, files in os.walk(_file):
			for file in files:
				f = os.path.splitext(file)[0]
				if f.endswith('M'):
					splitTimeExt = f.split('-')
				#	greatesthour = [x for x in splitTimeExt if 
					#if splitTimeExt == '':
				#		laterFileTime = file
				#	elif 
					inF = open(os.path.join(_file,file), 'r')
					for line in inF:
						if re.search('Firmware', line, re.I):
							self.fw = ",".join([bin.strip() for bin in line.split(":")[1:]])
						if re.search('Start Time', line, re.I):
							starttime = ",".join([bin.strip() for bin in line.split(" : ")[1:]])
							starttime = starttime.replace('/', '-')
							print starttime
							self._log.startdate(starttime)
						if re.search('End Time', line, re.I):
							endtime = ",".join([bin.strip() for bin in line.split(" : ")[1:]])
							endtime = endtime.replace('/', '-')
#							print endtime
							self._log.enddate(endtime)
						if re.search('Serial Number', line, re.I):
							self._sn = ",".join([bin.strip() for bin in line.split(":")[1:]])
#							print self._sn
							break
					self.parsefile(inF)

	

SM()
