import re
import os
import datetime

from ConfigParser import SafeConfigParser

import _ug_lib.ugLog
import _ug_lib.ugPN
#----------------------------

HOME = 'C:\cfast_sm_fwdl'

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
		
	def parsefile(self, inFile):
		lst_of_dict =[]
		f = open(inFile, 'r')
		for line in f:
			if row_idx == 0:
				header = line.strip().split()
			elif row_idx > 0:
				line = line.strip().split("      ")
				if "         " in line[i:]:
					line = line[0].split("         ")
					print "yes worked"
				col_idx = 0
				dict = {}
				for col in line:
					dict[header[int(col_idx)]] = col
					print "col_idx", col_idx, col
					col_idx += 1
				lst_of_dict.append(dict);
			row_idx += 1
		f.close()
		self.testcasecheck(lst_of_dict)
				
	def testcasecheck(self, lst_of_dict):
		log = _ug_lib.ugLog.Log()
		for i, row in enumerate(lst_of_dict):
			for x in lst_of_dict[i]:
				slotid = lst_of_dict[i][x]
				if slotid != 0:
					print lst_of_dict[i]
	
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
					inF = open(os.path.join(_file,file), 'r')
					for line in inF:
						if re.search('Firmware', line, re.I):
							self.fw = ",".join([bin.strip() for bin in line.split(":")[1:]])
						if re.search('Start Time', line, re.I):
							starttime = ",".join([bin.strip() for bin in line.split(" : ")[1:]])
#							print starttime
							self._log.startdate(starttime)
						if re.search('End Time', line, re.I):
							endtime = ",".join([bin.strip() for bin in line.split(" : ")[1:]])
#							print endtime
							self._log.enddate(endtime)
						if re.search('Serial Number', line, re.I):
							self._sn = ",".join([bin.strip() for bin in line.split(":")[1:]])
#							print self._sn
							break
					self.parsefile(inF)

	

SM()
