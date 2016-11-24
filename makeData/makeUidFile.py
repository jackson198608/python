import os
import var
import sys
import MySQLdb
import random
import time
import json
import hashlib

db="";
cursor="";
saveFileName="everyDayUids"
startDateTimeStamp="1437494400";

result={};
days=295;

db = MySQLdb.connect(var.dbServer,var.dbUser,var.dbPasswd,var.dbName,var.dbPort,charset=var.charset);
cursor = db.cursor();

for i in range(1,days):
	uids=[];
	release="100:" + str(i);
	startTimeStamp=int(startDateTimeStamp) + 3600*24*int(i)
	endTimeStamp=int(startDateTimeStamp) + 3600*24*int(i+1);
	startTimeArray=time.localtime(startTimeStamp);
	endTimeArray=time.localtime(endTimeStamp);
	startTime=time.strftime('%Y-%m-%d %H:%M:%S',startTimeArray);
	endTime=time.strftime('%Y-%m-%d %H:%M:%S',endTimeArray);

	sql="select distinct(uid) from stat_log where `release` = '" + str(release) + "' and created < '" +endTime+ "' and created > '"+startTime+"'";
	print sql;
	cursor.execute(sql);
	data = cursor.fetchall();
	if data!=None:
		for line in data:
			uids.append(line[0]);
	result[i]=uids;


fp=open(saveFileName,'w');
fp.write(json.dumps(result));
fp.close();

