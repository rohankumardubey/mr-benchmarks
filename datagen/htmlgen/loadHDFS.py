#!/usr/bin/python

import os,thread
params = {}
configFile = "config.txt"
configCont = open(configFile,'r').readlines()
for i in configCont:
    if len(i)>1 and not i.strip()[0] == '#':
        iSplit = map(lambda x:x.strip(), i.split(':')[1:])
        params[i.split(':')[0]] = ':'.join(iSplit)
machinesFile = "/root/persistent-hdfs/conf/slaves"
machs = open(machinesFile).readlines()
machs = map(lambda s: s.strip(),machs)
params['MachCount']=len(machs)

machID = 0
cmd = os.getenv("HADOOP_HOME") + "/bin/hadoop fs -copyFromLocal"
done = {}
def copyToHDFSThread( mach, myID, *args ):
    print "SSH'ing to machine %i" % (myID)
    print "Loading rankings data to HDFS"
    os.system("ssh %s '%s %s/Rankings.dat /data/rankings/Rankings_%s.dat'" % (mach, cmd, params['Output'], myID))
    print "Loading UserVisits data to HDFS"
    os.system("ssh %s '%s %s/UserVisits.dat /data/uservisits/UserVisits_%s.dat'" % (mach, cmd, params['Output'], myID))
    print "Machine %i done" % (myID)
    done[mach] = "done"

for mach in ( machs ):
    os.system('sleep 5')
    thread.start_new_thread(copyToHDFSThread, (mach, machID))
    machID = machID + 1
while (len(done.keys()) < params['MachCount']):
    os.system('sleep 60')
    print "Done with %i threads" % (len(done.keys()))
