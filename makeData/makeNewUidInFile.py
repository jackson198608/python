import os
import var
import sys
import MySQLdb
import random
import time
import hashlib
import json

db="";
cursor="";
fpLog="";
logName="/tmp/id.log";
startDateTimeStamp="1437494400";
newUidRandom=[];
result={};
startDays=305;
endDays=335;
days=305;
startUid=2000000;
uidAdd=5000;

#init resources

def getMd5Value(value):
	md5 = hashlib.md5();
	md5.update(str(value));
	md5Value=md5.hexdigest();
	return md5Value;

def init():
	#global the commom var
	global cursor;
	global db;
	global fpLog;
	global logName;
	global newUidRandom;
	global days;
	
	#make db
	try:
		db = MySQLdb.connect(var.dbServer,var.dbUser,var.dbPasswd,var.dbName,var.dbPort,charset=var.charset);
	except:
		print "[error]connect db fail";
		sys.exit();
	cursor = db.cursor();

	#openLog
	try:
		fpLog=open(logName,'a');
	except:
		print "open log file fail";
		sys.exit();

	#make global random array
	for i in range(startDays,endDays):
		rdata=random.uniform(-0.2,0.2);
		newUidRandom.append(rdata);
	
		

def close():
	global db;
	global fpLog;
	global result;

	db.close();
	fpLog.close();

	fp=open('everyDayUids','w');
	fp.write(json.dumps(result));
	fp.close();


def printLog(message):
	global fpLog;
	fpLog.write(message);
	fpLog.write("\n");


def do():
	global days;
	for i in range(startDays,endDays):
		getEveryDayUid(i);

def getTodayNewUidNum(dayNum):
	baseNum=int(1800 * (1/(dayNum ** 0.2)) + 2724);
	baseNum = baseNum * (1 + newUidRandom[dayNum-305]);
	return baseNum;

def getEveryDayUid(dayNum):
	global startUid;
	global uidAdd ;


	todayUidNum=getTodayNewUidNum(dayNum);
	todayUids=random_int_list(startUid,startUid+uidAdd,todayUidNum);
	todayUids=list(set(todayUids));
	startUid=startUid+uidAdd+1;
	result[dayNum]=todayUids;
		
	
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list

	

def main():
	init();
	do();
	close();	

if __name__ == "__main__":
	main();

