import os
import var
import sys
import MySQLdb
import random
import time
import hashlib
import json

startDataId=134714104;
db="";
cursor="";
fpLog="";
logName="/var/newData";
uidFileName="everyDayUids";
appFileName="uidAppId";
newUids={};
uidApps={};
startDateTimeStamp="1437494400";
startDays=305;
endDays=335;
startUid=200000;
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
	global appFileName;
	global uidFileName;
	global newUids;
	global uidApps;
	
	#openLog
	try:
		fpLog=open(logName,'w');
	except:
		print "open log file fail";
		sys.exit();

	#load everyUids file
	fp=open(uidFileName,'r');
	newUids=json.loads(fp.read());
	fp.close();

	#load uidapp file
	fp=open(appFileName,'r');
	uidApps=json.loads(fp.read());
	fp.close();

		
def close():
	global db;
	global fpLog;

	fpLog.close();

def printLog(message):
	global fpLog;
	fpLog.write(message);
	fpLog.write("\n");


def do():
	global startDays;
	global endDays;
	for i in range(startDays,endDays):
		getEveryDayUid(i);


def getEveryDayUid(dayNum):
	global newUids;

	for uid in newUids[str(dayNum)]:
		makeOneUidEverydayAction(uid,dayNum);


def makeOneUidEverydayAction(uid,dayNum):
		dayTimeStamp=int(startDateTimeStamp) + 3600*24*int(dayNum);

		p14Times=random.randint(3,5);
		p15Times=random.randint(3,5);
		p16Times=random.randint(1,4);
		p17Times=random.randint(1,4);
		p22Times=random.randint(1,5);

		pidTImes={14:p14Times,15:p15Times,16:p16Times,17:p17Times,22:p22Times};

		for pid,pidTimes in pidTImes.items():
			for i in range(1,pidTimes):
				#user use the app in 8 AM ~ 21 PM
				todayHmsTimeStamp=random.randint(8*3600,21*3600);
				dateArray=time.localtime(dayTimeStamp + todayHmsTimeStamp);
				created=time.strftime('%Y-%m-%d %H:%M:%S',dateArray);
		
				#insert record
				#print uid," ",created," ",pid," ",dayNum;
				insertRecord(uid,created,pid,dayNum);
	

#insert one record into db
def insertRecord(uid,created,pid,dayNum):
	#global var
	global startDataId;
	global uidApps;
	startDataId=startDataId+1;
	#define the common column
	sid=getMd5Value("htGPF3iDJYH2D5aLO2S73emwW2eBGSRX" + str(uid));
	url="";
	referrer="";
	keyword="";
	ip="103.244.252.68";
	info="";
	imei=getMd5Value("159c4343f6d9c0d3ca43419701f6342f" + str(uid));
	ua="";
	app_id=uidApps[str(uid)];
	model="";
	android_channel="";
	version="1.9.0";
	sdk="19";
	release="100:" + str(dayNum);
	is_build="0";
	if int(uid)%2==0:
		model="iPhone7";
	else:
		model="HM NOTE 1LTE";
		android_channel="xiaomi";
	valueTuple=[startDataId,uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,release,is_build,android_channel];
	
	valueTuple=map(str,valueTuple);
	record=','.join(valueTuple);
	printLog(record);
	

def main():
	init();
	do();
	close();	

if __name__ == "__main__":
	main();

