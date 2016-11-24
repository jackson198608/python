import os
import var
import sys
import MySQLdb
import random
import time
import hashlib
import json

startDataId=134995727;
insertEacheTime=100;
values="";
db="";
cursor="";
fpLog="";
logName="/var/stayData5";
startDateTimeStamp="1437494400";
newUidRandom=[];
uidFileName="everyDayUids"
appFileName="uidAppId";
uidApps={};
newUids={};
days=305;
startDays=2;
endDays=304;
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
	global newUidRandom;
	global days;
	global newUids;
	global uidApps;

	#openLog
	try:
		fpLog=open(logName,'w');
	except:
		print "open log file fail";
		sys.exit();

	#make global random array
	for i in range(1,days):
		rdata=random.gauss(-0.1,0.1);
		newUidRandom.append(rdata);
		
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

	fpLog.close();

def printLog(message):
	global fpLog;
	fpLog.write(message);
	fpLog.write("\n");


def do():
	global startDays;
	global endDays;
	for i in range(startDays,endDays):
		makeDayLeaveData(i);

def makeDayLeaveData(dayNum):
	for i in range(1,dayNum):
		uids=newUids[str(i)];
		stayUids=getStayuids(dayNum,i,uids);	
		for uid in stayUids:
			 makeOneUidEverydayAction(uid,dayNum,i);	

def getStayuids(dayNum,regDay,uids):
	stayUids=[];
	#how many stay?
	x=int(dayNum)-int(regDay);
	if x < 33:
		y=31.75092747/x+6.33069234;
		y=y*(1+newUidRandom[dayNum-1]);
	else:
		y=random.randint(59,61);
		y=float(y)/10;
	uidFomerLen=len(uids);
	uidAfterLen=(float(uidFomerLen)*y)/100;
	uidAfterLen=int(uidAfterLen);

	#if more the 3,random the leave uid
	sample=range(1,uidFomerLen+1);
	randomIndex=random.sample(sample,uidAfterLen);
	for i in randomIndex:
		stayUids.append(uids[i-1]);
	
	return stayUids;

def makeOneUidEverydayAction(uid,dayNum,regDay):
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
				insertRecord(uid,created,pid,dayNum,regDay);

#insert one record into db
def insertRecord(uid,created,pid,dayNum,regDay):
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
	release="100:" + str(regDay);
	is_build="0";
	if int(uid)%2==0:
		model="iPhone7,2";
	else:
		model="HM NOTE 1LTE";
		android_channel="xiaomi'";
	valueTuple=[startDataId,uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,release,is_build,android_channel];
	
	valueTuple=map(str,valueTuple);
	record=','.join(valueTuple);
	printLog(record);
	

def main():
	global startDays;
	global endDays;
	startDays=int(sys.argv[1]);
	endDays=int(sys.argv[2]);

	init();
	do();
	#insertRecord("1239870","2016-05-03 18:00:00",14,7,1);
	close();	

if __name__ == "__main__":
	main();

