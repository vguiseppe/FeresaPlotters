import numpy as np
import math
import os
import sys
import time
import json
import matplotlib.pyplot as plt


######################################
# Example feresa data plotter - shield purge
# V.E. Guiseppe 01/17/22
######################################


if(len(sys.argv)<4):
    print('usage: python3 RnPlotter.py YYY/mm/dd-HH:MM  YYYY/mm/dd-HH:MM name')
    print('where the two timestamps give the range for the analysis')
    sys.exit()

os.environ['TZ'] = 'US/Mountain'
time.tzset()

start = time.strptime(sys.argv[1], "%Y/%m/%d-%H:%M")
stop = time.strptime(sys.argv[2], "%Y/%m/%d-%H:%M")

dataname = sys.argv[3]

starttime_str = time.strftime("%b %d %Y %H:%M",start) #human readable
stoptime_str = time.strftime("%b %d %Y %H:%M",stop) #human readable
starttime_sec = time.mktime(start) # in seconds
stoptime_sec = time.mktime(stop) # in seconds
starttime = time.gmtime(starttime_sec) #UTC
stoptime = time.gmtime(stoptime_sec) #UTC

print("\nGrabing radon data from {} to {} MT\n".format(starttime_str,stoptime_str))

#set Time window for feresa call
dayI = time.strftime("%Y/%m/%d",starttime)
timeI = time.strftime("%H:%M:%S",starttime)
dayF = time.strftime("%Y/%m/%d",stoptime)
timeF = time.strftime("%H:%M:%S",stoptime)


#get records
com = "curl \"http://feresa.physics.unc.edu:5984/history_mjdscm/_design/history/_list/csv/values?startkey=%22DR%20Radon,Davis%20SCM%20Environmental%20Monitoring%20Processes,{}%20{}%22&endkey=%22DR%20Radon,Davis%20SCM%20Environmental%20Monitoring%20Processes,{}%20{}%22\">radon.csv".format(dayI,timeI,dayF,timeF)


# Get data from feresa
os.system(com)

#read in data, delete file
File = open('radon.csv','r')
Lines = File.readlines()
File.close()
os.system("rm radon.csv")


# data
Data = []
Times_sec = []
Times_hr = []
afParse0 = Lines[0].split("\"")
bfParse0 = afParse0[2].split("|")
t0=int(bfParse0[1].split(",")[0])
for l in range(1,len(bfParse0)):
    cfParse0 = bfParse0[l].split(",")
    Data += [float(cfParse0[1]),] # data
    Times_hr += [(int(cfParse0[0])-t0)/3600,] #time, in hr since t0
    Times_sec += [int(cfParse0[0]),] #timestamps

t0time = time.strftime("%b %d %Y %H:%M",time.localtime(t0)) #human readbale time

#save output
FileOutName = '{}_RoomRadon.txt'.format(dataname)
FileOut = open(FileOutName,'w')
FileOut.write("#time Rn[pCi/L]\n")
for i in range(len(Data)):
    FileOut.write("{}\t{}\n".format(Times_sec[i],Data[i]))
FileOut.close()


# #plot
pltName = '{}_RoomRadon.pdf'.format(dataname)
pltTitle = dataname
pltxlabel = "Hours Since {} MT".format(t0time)
plt.plot(Times_hr,Data)
plt.xlabel(pltxlabel)
plt.ylabel('Rn Conc. [pCi/L]')
plt.title(pltTitle)
#plt.axis([-5, 20, 0, 350])
plt.grid(True)
plt.savefig(pltName)

print("\n Data in {}\n Plot in {}".format(FileOutName,pltName))
