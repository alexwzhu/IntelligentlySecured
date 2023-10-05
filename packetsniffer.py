from scapy.all import *
import loadnotebook
a=0
def getAddress(address):
    global a
    capture = sniff(count=5)
    for p in capture:
        if (readpcap(p) == 1):
             print("Harmfull Packet!")
        elif (readpcap(p) == 0):
         print("Benign")
        a = dir(p)
        
    wrpcap("hackathon.pcap", capture)





def readpcap(pkt):
    return loadnotebook.predict(pkt)

    
getAddress("www.freerobux.com")



