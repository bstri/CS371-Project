from scapy.all import *
from get_df import *
import pandas as pd
import numpy as np
import sys
import socket 
import os
    
def fields_extraction(x):
    # print x.sprintf("{IP:%IP.src%,%IP.dst%,}"
    #     "{TCP:%TCP.sport%,%TCP.dport%,}"
    #     "{UDP:%UDP.sport%,%UDP.dport%}")
    # print x.summary()
    x.show()

pkts = sniff(prn = lambda x: fields_extraction(x), count = 50)

#"show" function 