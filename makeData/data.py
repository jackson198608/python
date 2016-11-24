#encoding=utf-8
import os
import var 
import hashlib    
import MySQLdb
import sys
import json
import zlib
import threading

reload(sys)
sys.setdefaultencoding('utf-8');

def get():
	#beging doing 
	for i in range(0,var.threadNum):
		t=threading.Thread(target=tGetByRange);
		t.start();
		var.taskThreads.append(t);
	for d in var.taskThreads:
		d.join();
	for d in var.backupThread:
		d.join();


def tGetByRange():
	
	proccessLen=var.proccessLen;
	#connect to the DB server		
	try:
		db = MySQLdb.connect(var.dbServer,var.dbUser,var.dbPasswd,var.dbName,var.dbPort,charset=var.charset);
	except:
		print "[error]connect db fail";
		return False;

	cursor = db.cursor();

	#if task is not zero,loop!
	while 1:
		#if this is the last loop
		var.dataGetKeysMutex.acquire();
		taskList=[];
		for i in range(0,proccessLen):
			try:
				taskList.append(var.dataGetKeys[0]);
				del var.dataGetKeys[0];
			except:
				print "[error]out of range now,doing the last";
				var.saveResultDict();
				sys.exit();
		var.dataGetKeysMutex.release();
		#doing id by id 
		for tid in taskList:
			result=getByTid(tid,db,cursor);
			if result:
				#lock the common var
				var.resultDickMutex.acquire();
				var.resultDict[str(tid)]=1;
				var.resultDickMutex.release();
			else:
				#lock the common var
				var.resultDickMutex.acquire();
				var.resultDict[str(tid)]=9;
				var.resultDickMutex.release();
		print "over tid:",tid;
	#free the resources
	cursor.close();
	db.close();

def getByTid(tid,db,cursor):
    #---------------------------
	#get nessary data from DB
	#---------------------------
	authorid=1;
	title="";
	content="";
	repliesByAuthor="";
	repliesByOther="";
	forumName="";
	fid=1;

	#get title
	sql="select subject,authorid,fid from pre_forum_thread where tid = " + str(tid);
	cursor.execute(sql);
	data = cursor.fetchone();
	if data==None:
		print "[error]has on title";
		return False;
	title=data[0];
	authorid=data[1];
	fid=data[2];

	#get forumName
	sql="select name from pre_forum_forum where fid= " + str(fid);
	cursor.execute(sql);
	data = cursor.fetchone();
	if data==None:
		print "[error]has on title";
		return False;
	forumName=data[0];

	#get basic content
	sql="select message from pre_forum_post where tid = " + str(tid) + " and first=1";
	cursor.execute(sql);
	data = cursor.fetchone();
	if data==None:
		print "[error]has on content tid:", tid;
		return False;

	content=forumName + ' ' + data[0];

	#get replies list and full contents in situation
	sql="select message,authorid from pre_forum_post where tid = " + str(tid) + " and first=0 order by dateline asc limit 0,100";
	cursor.execute(sql);
	data = cursor.fetchall();
	
	#find the situation to add for getting the full contents
	if data!=None:
		lastIsReplies=0;
		for line in data:
			if not lastIsReplies:
				if line[1]!=authorid:
					lastIsReplies=1;
				else:
					content = content + "||" + line[0];
					continue;
			if line[1]==authorid:
				repliesByAuthor=repliesByAuthor + "||" +  line[0];
			else:
				repliesByOther=repliesByOther + "||" +  line[0];


	#print log for result
	#print "[title]\n",title;
	#print "[content]\n",content;
	#print "[repliesByAuthor]\n",repliesByAuthor;
	#print "[repliesByOther]\n",repliesByOther;


	#save file
	if not saveDataFile(title,content,repliesByAuthor,repliesByOther,tid):
		return False;
	return True;
	
def saveDataFile(title,content,repliesByAuthor,repliesByOther,tid):
	dataDirPath=var.handleDataDir + makeMd5SubPath(tid);
	dataFilePath=dataDirPath + var.dataFileName;

	#make dataFilePath;
	try:
		if not os.path.exists(dataDirPath):
			os.makedirs(dataDirPath);
	except:
		print "[error]create dir file fail";
		return False;

	dataDict={};
	dataDict["title"]=title;
	dataDict["content"]=content;
	dataDict["repliesByAuthor"]=repliesByAuthor;
	dataDict["repliesByOther"]=repliesByOther;
	
	#write dict to file in json format
	try:
		fp=open(dataFilePath,'w');
		dataJson=json.dumps(dataDict);
		dataCompressJson=zlib.compress(dataJson);
		fp.write(dataCompressJson);
		fp.close();
	except:
		print "[error]write file failed";
		return False;

	return True;


def makeMd5SubPath(dataId):
	#caculate the md5 of the data id#do not forgot to change the data id to string object
	md5 = hashlib.md5();   
	md5.update(str(dataId));
	md5Value=md5.hexdigest();
	
	#make the path var from md5 value
	md5SubPath='/'+md5Value[0:2] + '/' + md5Value[2:4] + '/' + md5Value[4:6] + '/' + md5Value[6:] + '/';

	#get the result
	if md5SubPath:
		#print "threadid: ",threading.current_thread().name;
		#print md5SubPath;
		return md5SubPath;
	else: 
		return False;


def main():
	var.confInit();
	var.taskInit();
	#md5Path=makeMd5SubPath(1);
	#print md5Path;
	try:
		db = MySQLdb.connect(var.dbServer,var.dbUser,var.dbPasswd,var.dbName,var.dbPort,charset=var.charset);
	except:
		print "[error]connect db fail";
		return False;


	getByTid(90366,db);
	db.close();

if __name__ == "__main__":
	main();
