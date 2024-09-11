import os
import sys
import time
import matplotlib.pyplot as plt


######################################
# Example feresa data plotter - shield purge
# V.E. Guiseppe 01/17/22
######################################


if(len(sys.argv)<3):
    print('usage: python3 ShieldPurgePlotter.py YYY/mm/dd-HH:MM  YYYY/mm/dd-HH:MM')
    print('where the two timestamps give the range for the analysis')
    sys.exit()

os.environ['TZ'] = 'US/Mountain'
time.tzset()

start = time.strptime(sys.argv[1], "%Y/%m/%d-%H:%M")
stop = time.strptime(sys.argv[2], "%Y/%m/%d-%H:%M")

starttime_str = time.strftime("%b %d %Y %H:%M",start) #human readable
stoptime_str = time.strftime("%b %d %Y %H:%M",stop) #human readable
starttime_sec = time.mktime(start) # in seconds
stoptime_sec = time.mktime(stop) # in seconds
starttime = time.gmtime(starttime_sec) #UTC
stoptime = time.gmtime(stoptime_sec) #UTC

print("\nGrabing shield purge data from {} to {} MT\n".format(starttime_str,stoptime_str))

#set Time window for feresa call
dayI = time.strftime("%Y/%m/%d",starttime)
timeI = time.strftime("%H:%M:%S",starttime)
dayF = time.strftime("%Y/%m/%d",stoptime)
timeF = time.strftime("%H:%M:%S",stoptime)


#get GB flow records
flowcom = "curl \"http://feresa.physics.unc.edu:5984/history_mjdscm/_design/history/_list/csv/values?startkey=%22Shield%20flow%20meter,Davis%20LN2,{}%20{}%22&endkey=%22Shield%20flow%20meter,Davis%20LN2,{}%20{}%22\">ShieldFlow.csv".format(dayI,timeI,dayF,timeF)

print(flowcom)

# Get data from feresa
os.system(flowcom)

#read in data, delete file
FlowFile = open('ShieldFlow.csv','r')
FlowLines = FlowFile.readlines()
FlowFile.close()
# os.system("rm ShieldFlow.csv")


#flow data
Flows = []
Times_sec = []
Times_hr = []
afParse0 = FlowLines[0].split("\"")
bfParse0 = afParse0[2].split("|")
t0=int(bfParse0[1].split(",")[0])
for l in range(1,len(bfParse0)):
    cfParse0 = bfParse0[l].split(",")
    Flows += [float(cfParse0[1]),] #flow data
    Times_hr += [(int(cfParse0[0])-t0)/3600/24,] #time, in d since t0
    Times_sec += [int(cfParse0[0]),] #timestamps

t0time = time.strftime("%b %d %Y %H:%M",time.localtime(t0)) #human readbale time

#save output
FlowFileOut = open('ShieldFlow.txt','w')
FlowFileOut.write("#time flow[lpm]\n")
for i in range(len(Flows)):
    FlowFileOut.write("{}\t{}\n".format(Times_sec[i],Flows[i]))
FlowFile.close()


# #plot
pltName = "ShieldPurge.pdf"
pltTitle = "Shield Purge"
pltxlabel = "Days Since {} MT".format(t0time)
plt.plot(Times_hr,Flows)
plt.xlabel(pltxlabel)
plt.ylabel('Flow Rate [lpm]')
plt.title(pltTitle)
#plt.axis([-5, 20, 0, 350])
plt.grid(True)
plt.savefig(pltName)

print("\n Date in ShieldFlow.txt\n Plot in ShieldPurge.pdf")
