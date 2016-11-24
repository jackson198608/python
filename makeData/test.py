import os
import var
import sys

db="";
cursor="";
fpLog="";
logName="/tmp/id.log";

#init resources
def init():
	#global the commom var
	global cursor;
	global db;
	global fpLog;
	global logName;
	
	#make db
	db = MySQLdb.connect(var.dbServer,var.dbUser,var.dbPasswd,var.dbName,var.dbPort,charset=var.charset);
	cursor = db.cursor();

	#openLog
	try:
		fpLog=open(logName,'a');
	except:
		print "open log file fail";
		sys.exit();
	
		

def close():
	global db;
	global fpLog;

	db.close();
	fpLog.close();

def printLog(message):
	global fpLog;
	fpLog.write(message);
	fpLog.write("\n");

def getEveryDayUid():
	return;

def makeOneUidEverydayAction(uid):
	return;

#insert one record into db
def insertRecord(uid,created,pid):
	#global var
	global db;
	global cursor;
	#define the common column
	sid="htGPF3iDJYH2D5aLO2S73emwW2eBGSRX";	
	url="";
	referrer="";
	keyword="";
	ip="103.244.252.68";
	info="";
	imei="159c4343f6d9c0d3ca43419701f6342e";
	ua="Dalvik/2.1.0 (Linux; U; Android 5.0; Nexus 5 Build/LRX21O)";
	app_id="1";
	model="";
	android_channel="";
	version="1.9.0";
	sdk="sdk";
	release="4.4.4";
	is_build="0";
	if uid%2==0:
		model="iPhone7,2";
	else:
		model="HM NOTE 1LTE";
		android_channel="xiaomi";
	
	sql="insert into stat_log (uid,sid,url,pid,referrer,keyword,ua,ip,info,created,app_id,imei,model,version,sdk,release,is_build,android_channel) values ('" + uid  + "','" + sid + "','"+ url + "','" + pid + "','"+ referrer + "','" + keyword + "','" + ua + "','" + ip + "','" + info + "','" + created + "','" +app_id + "','" + imei + "','" + model + "','" + version + "','" + sdk + "','" + release + "','" + is_build + "','" + android_channel + "')";	
	cursor.execute(sql);
	db.commit();
	recordId = int(cursor.lastrowid);
	printLog(str(recordId));
	

def main():
	init();
	insertRecord("123456","2016-05-11 22:45:53",14);
	close();	

if __name__ == "__main__":
	main();

