import json
import sys
import random

result={};

baseMistake=0.3;

#load everyUids file
fp=open("everyDayUids","r");
newUids=json.loads(fp.read());
fp.close();

for i in newUids.keys():
	uids=newUids[i];
	for uid in uids:
		result[uid]=1;
	total=len(uids);
	myMistake=baseMistake * (1 + random.uniform(-0.2,0.2));
	androidNum=int(total*myMistake);
	androidUids=random.sample(uids,androidNum);
	for i in androidUids:
		result[i]=2;

fp=open('uidAppId','w');
fp.write(json.dumps(result));
fp.close();

