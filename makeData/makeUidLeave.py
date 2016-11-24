import os
import var
import sys
import MySQLdb
import random
import time
import hashlib
import json

insertEacheTime=100;
values="";
db="";
cursor="";
fpLog="";
logName="/tmp/stayid_new.log";
startDateTimeStamp="1437494400";
newUidRandom=[];
uidFileName="everyDayUids"
newUids={};
days=295;
startDays=2;
endDays=15;
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
	for i in range(1,days):
		rdata=random.gauss(-0.1,0.1);
		newUidRandom.append(rdata);
	
		
	#load everyUids file
	fp=open(uidFileName,'r');
	newUids=json.loads(fp.read());
	fp.close();


def close():
	global db;
	global fpLog;

	db.close();
	fpLog.close();

def printLog(message):
	global fpLog;
	fpLog.write(message);
	fpLog.write("\n");


def do():
	global days;
	global startDays;
	global endDays;
	for i in range(startDays,endDays+1):
		makeDayLeaveData(i);

def makeDayLeaveData(dayNum):
	for i in range(1,dayNum):
		print dayNum,":",i;
		uids=newUids[str(i)];
		stayUids=getStayuids(dayNum,i,uids);	
		for uid in stayUids:
			 makeOneUidEverydayAction(uid,dayNum,i);	
def getStayuids(dayNum,regDay,uids):
	stayUids=[];
	#how many stay?
	x=int(dayNum)-int(regDay);
	y=31.75092747/x+6.33069234;
	y=y*(1+newUidRandom[dayNum-1]);
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
	global db;
	global cursor;
	global values;
	global insertEacheTime;
	#define the common column
	sid=getMd5Value("htGPF3iDJYH2D5aLO2S73emwW2eBGSRX" + str(uid));
	url="";
	referrer="";
	keyword="";
	ip="103.244.252.68";
	info="";
	imei=getMd5Value("159c4343f6d9c0d3ca43419701f6342f" + str(uid));
	ua="Dalvik/2.1.0 (Linux; U; Android 5.0; Nexus 5 Build/LRX21O)";
	app_id="1";
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
		android_channel="xiaomi";
	#sql="insert into stat_log (uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,`release`,is_build,android_channel) values ('" + str(uid)  + "','" + str(sid) + "','"+ str(url) + "','" + str(pid) + "','"+ str(referrer) + "','" + str(keyword) + "','" + str(ua) + "','" + str(ip) + "','" + str(info) + "','" + str(created) + "','" +str(app_id) + "','" + str(imei) + "','" + str(model) + "','" + str(version) + "','" + str(sdk) + "','" + str(release) + "','" + str(is_build) + "','" + str(android_channel) + "')";	
	valueTuple=(uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,release,is_build,android_channel);
	valueTuple=map(str,valueTuple);
	values.append(valueTuple);

	if (len(values)> insertEacheTime):
		cursor.executemany("""insert into stat_log (uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,`release`,is_build,android_channel) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",values);
		values=[];
		db.commit();
		printLog(len(values));
	

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

