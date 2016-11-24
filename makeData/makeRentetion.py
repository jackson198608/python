import os
import var
import sys
import MySQLdb
import random
import time
import hashlib
import json
import phpserialize

db="";
cursor="";
fpLog="";
logName="/tmp/retetion.log";
startDateTimeStamp="1437494400";
result={};
days=305;
newUids={};
uidFileName="everyDayUids";

#init resources

def init():
	#global the commom var
	global cursor;
	global db;
	global fpLog;
	global logName;
	global days;
	global newUids;
	global uidFileName;
	
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

	#load everyUids file
	fp=open(uidFileName,'r');
	newUids=json.loads(fp.read());
	fp.close();


def close():
	global db;
	global fpLog;
	global result;

	db.close();
	fpLog.close();



def printLog(message):
	global fpLog;
	fpLog.write(message);
	fpLog.write("\n");


def do():
	global days;
	for i in range(220,305):
		getEveryDayRentention(i);


def getEveryDayRentention(dayNum):
	global newUids;
	params={"newuser":0,"1_day":0,"2_day":0,"3_day":0,"4_day":0,"5_day":0,"6_day":0,"7_day":0,"14_day":0,"30_day":0};
	newUidLen=len(newUids[str(dayNum)]);
	params["newuser"]=newUidLen;
	for i in [1,2,3,4,5,6,7,14,30]:	
		countDay=dayNum+i;

		#more than time
		if(countDay>days-1):
			break;

		#get time range
		startTimeStamp=int(startDateTimeStamp) + 3600*24*int(countDay)
		endTimeStamp=int(startDateTimeStamp) + 3600*24*int(countDay+1);
		startTimeArray=time.localtime(startTimeStamp);
		endTimeArray=time.localtime(endTimeStamp);
		startTime=time.strftime('%Y-%m-%d %H:%M:%S',startTimeArray);
		endTime=time.strftime('%Y-%m-%d %H:%M:%S',endTimeArray);

		
		release="100:" + str(dayNum);

		sql="select count(distinct(uid)) from stat_log where `release` = '" + str(release) + "' and created < '" +endTime+ "' and created > '"+startTime+"'";
		cursor.execute(sql);
		data = cursor.fetchone();
		
		stayLen=0;
		if data!=None:
			stayLen=data[0];

		#print dayNum,":",countDay,",",newUidLen,":",stayLen;
		key=str(i)+"_day";
		params[key]=stayLen;

	#change params
	params=phpserialize.dumps(params);

	#insert record	
	insertRecord(params,dayNum);

#insert one record into db
def insertRecord(params,dayNum):
	#global var
	global db;
	global cursor;
	global startDateTimeStamp;

	dayTimeStamp=int(startDateTimeStamp) + 3600*24*int(dayNum);
	dateArray=time.localtime(dayTimeStamp);
	created=time.strftime('%Y-%m-%d %H:%M:%S',dateArray);
	
	sql="insert into stat_user_retention(type,params,created) values (1,'"+str(params)+"','" + str(created)+"')";
	print sql;
	cursor.execute(sql);
	db.commit();
	recordId = int(cursor.lastrowid);
	printLog(str(recordId));

def main():
	init();
	do();
	close();	

if __name__ == "__main__":
	main();

