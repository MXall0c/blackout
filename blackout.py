#! /bin/python
import requests, os

def retrieve(files):
    badlist = 1
    for file in files:
        if 'list' in file:
            print file
            f = open(file, 'r')
            for blacklist in f:
                print blacklist
                r = requests.get(blacklist.strip())
                open("{}.bl".format(badlist), 'wb').write(r.content)
                badlist +=1

def cleanup(files):
    #remove downloaded files
    for file in files:
        if '.bl' in file:
            print "Deleting {}".format(file)
            os.remove(file)

def cleananduniqe(files):
    #Go through files, remove IPs, comments and dupes
    badsites = set()
    for file in files:
        if '.bl' in file:
            print file
            f = open(file, 'r')
            for line in f:
                line = line.strip()
                if line.find('#') == 0 or line.find('<') == 0:
                    #skip all comment lines and html
                    continue
                if '#' in line:
                    #chop off trailing comments
                    x = line.split('#')
                    line = x[0]  
                line = line.split()
                if len(line) == 1:
                    #just an url
                    badsites.add(line[0])
                if len(line) > 1:
                    #url with leading ip
                    if '127.0.0.1' in line[0] or '0.0.0.0' in line[0] or '::1' in line[0]:
                        badsites.add(line[1])
                        #print line[1]
                    else:
                        #debug the weird garbage
                        print line
    print "{} unique bad sites.".format(len(badsites))
    open("blackout.txt", 'w').write('\n'.join(badsites))


retrieve(os.listdir('.'))
cleananduniqe(os.listdir('.'))
#print '\n'.join(badsites)
#cleanup(os.listdir('.'))
