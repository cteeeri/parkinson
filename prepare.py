#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 09:14:43 2018

@author: chin
"""

import mytappy as t

j = t.agg_struct('data/ArchivedUsers', 'User_*.txt', 'data/TappyData', '*_*.txt', 'data/datapools.json')
t.cleanUpData('data/TappyData', '*_*.txt')
t.user2DF(j, 'data/ArchivedUsers/Users.csv')

t.keystrokeDataForDF(j, 'data/TappyData/cleanup')
t.combine('dfData','df.csv','data/ArchivedUsers','Users.csv' , 'data/TappyData/cleanup', '*.csvbins' )



#### develop
#j = t.agg_struct('fordevelop_data/ArchivedUsers', 'User_*.txt', 'fordevelop_data/TappyData', '*_*.txt', 'fordevelop_data/fordevelop_datapools.json')
#t.cleanUpData('fordevelop_data/TappyData', '*_*.txt')
#t.user2DF(j, 'fordevelop_data/ArchivedUsers/Users.csv')
#
#t.keystrokeDataForDF(j, 'fordevelop_data/TappyData/cleanup')
#t.combine('dfData','df.csv','fordevelop_data/ArchivedUsers','Users.csv' , 'fordevelop_data/TappyData/cleanup', '*.csvbins' )

