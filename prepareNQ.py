#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:18:49 2018

@author: chin
"""
import mytappy as t

#batch 1
t.parseNQ('data/MIT-CS1PD/GT_DataPD_MIT-CS1PD.csv') 

t.rmNQOutlier('data/MIT-CS1PD/data_MIT-CS1PD/user*.csv')

#t.NQmean('data/MIT-CS1PD/data_MIT-CS1PD/user*.csvnooutlier')
#t.NQDesc('data/MIT-CS1PD/data_MIT-CS1PD/user*.csvnooutlier')
t.NQBins('data/MIT-CS1PD/data_MIT-CS1PD/user*.csvnooutlier')



#batch 2
t.parseNQ('data/MIT-CS2PD/GT_DataPD_MIT-CS2PD.csv')

t.rmNQOutlier('data/MIT-CS2PD/data_MIT-CS2PD/user*.csv')

#t.NQmean('data/MIT-CS2PD/data_MIT-CS2PD/user*.csvnooutlier')
#t.NQDesc('data/MIT-CS2PD/data_MIT-CS2PD/user*.csvnooutlier')
t.NQBins('data/MIT-CS2PD/data_MIT-CS2PD/user*.csvnooutlier')


#t.combineNQ(['data/MIT-CS1PD/data_MIT-CS1PD', 'data/MIT-CS2PD/data_MIT-CS2PD'], 'user*.csvnooutliermean')
t.combineNQ(['data/MIT-CS1PD/data_MIT-CS1PD', 'data/MIT-CS2PD/data_MIT-CS2PD'], 'user*.csvnooutlierBins')