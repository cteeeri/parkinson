#!/usr/bin/env python3
# -*- coding: cp1252 -*-
"""
Created on Fri Jan 26 10:03:44 2018

@author: chin
"""

import constants


def clean(inStr):
    import re
    import numpy as np
    
    mystr = inStr.strip(' \t\r\n\0')
    mystr = mystr.replace('\x00', '')
    rowpattern = r'^(\w{10})\s+(\d{6})\s+(\d{2}:\d{2}:\d{2}\.\d{3})\s+([RLS]{1})\s+(\d{4}\.\d{1})\s+([RLS]{1}[RLS]{1})\s+(\d{4}\.\d{1})\s+(\d{4}\.\d{1})'
    r = re.search(rowpattern, mystr, re.I)

    
    returnStr = constants.discard
    
    if r:
        res = np.empty(8).tolist()
        for i in range(1,9):
            res[i-1] = r.group(i)
        
        # 
        res[4] = res[4].lstrip("0")
        
        # 
        res[6] = res[6].lstrip("0")
        
        # 
        res[7] = res[7].lstrip("0")
        
        cleanStr = ""
        for k in res:
            cleanStr += k + " " 
    
        returnStr = cleanStr + "\n"
    
    return returnStr
    