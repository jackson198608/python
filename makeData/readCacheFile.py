import json
#read uid file
'''
fp=open("everyDayUids","r");
newUids=json.loads(fp.read());
fp.close();
print newUids['308'];
'''

#read appid file
fp=open("uidAppId","r");
newAppIds=json.loads(fp.read());
fp.close();

print   newAppIds['2015085'];


