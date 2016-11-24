import os
import var
import sys
import MySQLdb
import random
import time
import hashlib

db="";
cursor="";
fpLog="";
logName="/tmp/stayid.log";
startDateTimeStamp="1437494400";
newUidRandom=[];
days=295;
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
	for i in range(2,days):
		getEveryDayUid(i);

def getEveryDayUid(dayNum):
	global startUid;
	global uidAdd ;
	
	for regDay in range(1,dayNum):
		uids=getStayuids(dayNum,regDay);
		for uid in uids:
			 makeOneUidEverydayAction(uid,dayNum,regDay);
def getNewUids(dayNum,regDay):
	global db;
	global cursor;
	global startDateTimeStamp;
	
	uids=[];

	#get all regDay uids
	startTimeStamp=int(startDateTimeStamp) + 3600*24*int(dayNum-1)
	endTimeStamp=int(startDateTimeStamp) + 3600*24*int(dayNum);
	startTimeArray=time.localtime(startTimeStamp);
	endTimeArray=time.localtime(endTimeStamp);
	startTime=time.strftime('%Y-%m-%d %H:%M:%S',startTimeArray);
	endTime=time.strftime('%Y-%m-%d %H:%M:%S',endTimeArray);

	release="100:" + str(regDay);

	sql="select distinct(uid) from stat_log where `release` = '" + str(release) + "' and created < '" +endTime+ "' and created > '"+startTime+"'";
	cursor.execute(sql);
	data = cursor.fetchall();
	if data!=None:
		for line in data:
			uids.append(line[0]);
	
	return uids;

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
				#print uid," ",created," ",pid," ",dayNum," ",regDay;
				insertRecord(uid,created,pid,dayNum,regDay);
	
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list

#insert one record into db
def insertRecord(uid,created,pid,dayNum,regDay):
	#global var
	global db;
	global cursor;
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
	
	sql="insert into stat_log (uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,`release`,is_build,android_channel) values ('" + str(uid)  + "','" + str(sid) + "','"+ str(url) + "','" + str(pid) + "','"+ str(referrer) + "','" + str(keyword) + "','" + str(ua) + "','" + str(ip) + "','" + str(info) + "','" + str(created) + "','" +str(app_id) + "','" + str(imei) + "','" + str(model) + "','" + str(version) + "','" + str(sdk) + "','" + str(release) + "','" + str(is_build) + "','" + str(android_channel) + "')";	
	cursor.execute(sql);
	db.commit();
	recordId = int(cursor.lastrowid);
	printLog(str(recordId));
	

def main():
	init();
	do();
	#insertRecord("1239870","2016-05-03 18:00:00",14,7,1);
	close();	

if __name__ == "__main__":
	main();

