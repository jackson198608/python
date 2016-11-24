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
logName="/tmp/updateHistory.log";
startDateTimeStamp="1437494400";
result={};
days=305;
newUids={};
uidFileName="everyDayUids";
appFileName="uidAppId";
uidApps={};
startdownSum=171692;


#init resources

def init():
	#global the commom var
	global cursor;
	global db;
	global fpLog;
	global logName;
	global days;
	global uidApps;
	global newUids;
	global uidFileName;
	global appFileName;
	
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

	#load everyUids file
	fp=open(appFileName,'r');
	uidApps=json.loads(fp.read());
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
	for i in range(1,days):
		updateHistory(i);


def updateHistory(dayNum):
	global newUids;
	global startDateTimeStamp;	
	global startdownSum;

	#get len
	todayUids=newUids[str(dayNum)];
	todayAppLen=len(todayUids);
	startdownSum=startdownSum + todayAppLen;
	todayIosLen=0;
	todayAndroidLen=0;

	#get time
	dayTimeStamp=int(startDateTimeStamp) + 3600*24*int(dayNum);
	dateArray=time.localtime(dayTimeStamp);
	created=time.strftime('%Y-%m-%d 00:00:00',dateArray);	

	#get real ios,android num
	for uid in todayUids:	
		app_id=uidApps[str(uid)];
		if app_id == 1:
			todayIosLen=todayIosLen+1;
		else:
			todayAndroidLen=todayAndroidLen+1;

	#get params
	params={};
	dataId=0;
	sql="select id,params from stat_history where created = '" +created+ "'";
	cursor.execute(sql);
	data = cursor.fetchone();
	if data!=None:
		dataId=data[0];
		params=data[1];
		params=phpserialize.loads(params);	

	#print dataId,",",params;
	#print dataId,",",dayNum;
	#print todayAppLen,",",todayIosLen,",",todayAndroidLen;
	#change params
	params['appdown']['downSum']=startdownSum;
	params['appdown']['ios_down']=todayIosLen;
	params['appdown']['android']=todayAndroidLen;
	params=phpserialize.dumps(params);

	#update record	
	updateRecord(dataId,params);

#insert one record into db
def updateRecord(dataId,params):
	#global var
	global db;
	global cursor;
	
	sql="UPDATE stat_history set params = '"+params+"' where id = " + str(dataId);
	cursor.execute(sql);
	db.commit();
	

def main():
	init();
	do();
	close();	

if __name__ == "__main__":
	main();

