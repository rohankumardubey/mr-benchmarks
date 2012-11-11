#!/usr/bin/python                                                                                                          
import os,thread
params = {}
configFile = "config.txt"
configCont = open(configFile,'r').readlines()
for i in configCont:
    if len(i)>1 and not i.strip()[0] == '#':
        iSplit = map(lambda x:x.strip(), i.split(':')[1:])
        params[i.split(':')[0]] = ':'.join(iSplit)
machs = params['Machines'].split(',')
params['MachCount']=len(machs)

machID = 0
cmd = "sync; echo 3 > /proc/sys/vm/drop_caches"
done = {}
def dropCachesThread( mach, myID, *args ):
    print "SSH'ing to machine %i" % (myID)
    os.system("ssh %s '%s'" % (mach, cmd))
    done[mach] = "done"

for mach in ( machs ):
    os.system('sleep 2')
    thread.start_new_thread(dropCachesThread, (mach, machID))
    machID = machID + 1
while (len(done.keys()) < params['MachCount']):
    os.system('sleep 60')
    print "Done with %i threads" % (len(done.keys()))
