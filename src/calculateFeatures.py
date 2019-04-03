from scapy.all import *
import pandas as pd
import numpy as np
import sys
import socket
import os
import urllib
from requests import get
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP=s.getsockname()[0]
print("Local IP is :%s " % (s.getsockname()[0]))
s.close()
externalIP = get('https://api.ipify.org').text
print("External IP is :%s "%(externalIP))
flows=list()

def fields_extraction(x):
    # print x.sprintf("{IP:%IP.src%,%IP.dst%,}"
    #     "{TCP:%TCP.sport%,%TCP.dport%,}"
    #     "{UDP:%UDP.sport%,%UDP.dport%}")
    # print x.summary()
    x.show()
    for f in flows:
        pass



pkts = sniff(prn = lambda x: fields_extraction(x), count = 1)
pkts.conversations()

#"show" function