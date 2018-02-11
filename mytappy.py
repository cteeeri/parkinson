# -*- coding: utf-8 -*-
"""
Spyder Editor

mytappy.py
"""

import json
import numpy as np
import pandas as pd
import os, glob
from decimal import Decimal

def agg_struct(userf_path, userf_pattern, dataf_path, dataf_pattern, outputfile):
    '''
    agg_data() will gather all files related and put out a json 
    with key as the 10 character user id and a list of keystroke data 
    of the user
    '''
    
#    import os, glob
#    import json
    
    users = os.path.join(userf_path, userf_pattern)   
    usersdata = os.path.join(dataf_path, dataf_pattern)   
    files_pool = {}
    
    for f in glob.glob(users):  
        #print(f)
        if f not in files_pool:
            # use filename with full path as key
            files_pool[f] = [] 
        
    for g in glob.glob(usersdata):
        g_base_10chr = os.path.basename(g)[0:-9]
        #print(g)
        userFullPathKey = users.replace('*', g_base_10chr)
        if userFullPathKey in files_pool:
            #print(userFullPathKey)
            v = files_pool[userFullPathKey]
            if g not in v:
                v.append(g)
                files_pool[userFullPathKey] = v   
            v = None
    
    _removeUserNoData(files_pool)
    
    with open(outputfile, 'w') as out:
        json.dump(files_pool, out)
    print ("All data structure gathered in {}".format(outputfile))
    
    return outputfile

def _removeUserNoData(jsonf):
    # filter through and delete those user without tappy data
    users_w_empty_data = []
    for k, v in jsonf.items():
    #    print(k, v)
        if not v:
            #print("{} has no keystroke data.".format(k))
            users_w_empty_data.append(k)
      
    # remove from files_pool
    for user in users_w_empty_data:
        del jsonf[user]
        #print("{} removed".format(user))
    
def info(injson):
    '''
    [Total files, nonPD, PD, PD_takeMed, pd_noMed] 
    '''
#    import json
    parkinson_count = 0
    nonParkinson_count = 0
    pd_take_medicine = 0
    
    with open(injson, 'r') as rf:
        jsonloaded = json.load(rf)
    
    len_injson = len(jsonloaded)
    
    for k in jsonloaded:
        with open(k) as file:
            content = file.readlines()
            if  content[2] == "Parkinsons: True\n":
                parkinson_count += 1
                if content[8] == 'Levadopa: True\n':
                    pd_take_medicine += 1
                elif content[9] == 'DA: True\n':
                    pd_take_medicine += 1
                elif content[10] == 'MAOB: True\n':
                    pd_take_medicine += 1
                elif content[11] == 'Other: True\n':
                    pd_take_medicine += 1
            elif content[2] == "Parkinsons: False\n":
                nonParkinson_count += 1
    pd_noMed = parkinson_count-pd_take_medicine                
    print("total users {}, nonPD {}, PD {} (PD_takeMed {}, noMed {})".format(len_injson, nonParkinson_count, parkinson_count, pd_take_medicine, pd_noMed))            
    return [len_injson, nonParkinson_count, parkinson_count, pd_take_medicine, pd_noMed]  


def _findStat(df, target):
    '''
    Return a result for the target feature
    '''
#    import pandas as pd
#    import numpy as np
#    from decimal import Decimal
    
    directions = [['RR', 'RL','RS'],['LR','LL','LS'],['SR','SL','SS']]
    #df.info()

    #df['logHold'] = np.log(df['Hold'].values)
    rr = df[(df['Direction']== directions[0][0])][target]

    Q1 = rr.quantile(0.25)
    Q2 = rr.quantile(0.5)
    Q3 = rr.quantile(0.75)
    
    iqr = Q3 - Q1
    
    low_threshold = int(Decimal(Q1 - 1.5*iqr))
    hi_threshold = int(Decimal(Q3 + 1.5*iqr))
    
#    a = pd.Series([62,47,55,74,31,77,85,63,42,32,71,57])
#    print(a.mean())
#    print(a.var())
    avg = int(Decimal(rr.mean()))
    variance = int(Decimal(rr.var()))
    
    return (avg, variance, Q1, Q2, Q3, low_threshold, hi_threshold)
    
def user2DF(injson, path):
    '''
    Put all users together as a dataframe and save as csv
    '''
    
    with open(injson, 'r') as rf:
        jsonf = json.load(rf)
    col_names = ['Birth','Gender','Parkinson','Tremors', 'DiagnosisYr',
                 'Sidedness','UPDRS','Impact','Levadopa','DA',
                 'MAOB','OtherMed','UserKey']
    userdata = np.empty(13).tolist()
    df = pd.DataFrame()
    for k, v in jsonf.items():
        with open(k,'r') as rf:
            userdata[12] = k[-14:-4]
            for i,line in enumerate(rf):
                try:
                    label, justtext = line.strip().split(": ")
                    userdata[i] = justtext.strip() 
                except ValueError:
                    userdata[i] = '------'    
            row = dict(list(zip(col_names, userdata)))  
            
        df = df.append(row, ignore_index=True)

    new_dir = os.path.dirname(path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)    
    
    savepath = os.path.join(new_dir, os.path.basename(path))
    
    df.to_csv(savepath, index=False)
    print("Successfully transformed ArchivedUsers data to 1 csv file with 13 columns, see {}".format(path))
    
    return df
    

def readInJson(injson):
    with open(injson, 'r') as rf:
        jsonf = json.load(rf)
    return jsonf

def rmOutlier(df):
    directions = ['RR','RL','RS','LR','LL','LS','SR','SL','SS']
    for d in directions:
        for t in ['Hold','Flight']:
            q3 = df[df.Direction==d][t].quantile(0.75)
            q1 = df[df.Direction==d][t].quantile(0.25)
            iqr = q3 - q1   
            low_thresh = q1 - 1.5*iqr
            hi_thresh = q3 + 1.5*iqr
            
            # drop in place
            if t == 'Hold':
                df.drop(df[(df.Direction == d) & (df.Hold > hi_thresh)].index, inplace=True)
                df.drop(df[(df.Direction == d) & (df.Hold < low_thresh)].index, inplace=True)
            if t == 'Flight':
                df.drop(df[(df.Direction == d) & (df.Flight > hi_thresh)].index, inplace=True)
                df.drop(df[(df.Direction == d) & (df.Flight < low_thresh)].index, inplace=True)
            
    return df

def findmeanvar(df):
    user = df.iloc[0,0]
    htmean = df['Hold'].mean()   
    ftmean = df['Flight'].mean()
    data = {'UserKey':[user], 'HTmean':[htmean], 'FTmean':[ftmean]}
    
    df = pd.DataFrame(data)
    
    return df


def findDescribe(df):
    import operator
    from functools import reduce
#    UserKey, HoldTimeMS Direction FlighttimeMS
#    print("finddescribe", df.head())
    df.drop('Direction', axis=1,inplace=True)
    
    dfdesc = df.describe()
    dfdesc.loc['var',:]= df.var()
    dfdesc.drop('count', axis=0, inplace=True)
    
    v = dfdesc.values.tolist()
    colnames = ['HTmean', 'FTmean','HTstd', 'FTstd','HTmin', 'FTmin','HT25', 'FT25','HT50', 'FT50','HT75', 'FT75','HTmax', 'FTmax','HTvar', 'FTvar']
    r = reduce(operator.concat, v)
    
    m = map(lambda x,y: {x:y}, colnames, r)
    mm = list(m)
    dd = dict()
    for i in mm:
        dd[list(i.keys())[0]] = [list(i.values())[0]]
    
    loadeddf = pd.DataFrame(dd)
    
    loadeddf.loc[:,'UserKey'] = df.iloc[0,0]
    
#    print("loadeddf ", loadeddf)
    
    return loadeddf
  
def locateBin (inTime):    
    binRange = range(1,11)

    if (inTime) < 100: return 1 
    if (inTime) > 1000: return 10 
        
    significant = int(str(inTime)[0])

    return binRange[significant]

def findBins(df):
#         UserKey   Hold Direction  Flight
#0     WY25WHLA9D  109.4        LL   312.5
#1     WY25WHLA9D   93.8        LL   296.9
#2     WY25WHLA9D  125.0        LS   566.4
#3     WY25WHLA9D  140.6        SL   589.8
#4     WY25WHLA9D  140.6        LR   531.3
#5     WY25WHLA9D  125.0        RL   558.6
#6     WY25WHLA9D  140.6        RL   418.0
#7     WY25WHLA9D   97.7        LL   265.6
#8     WY25WHLA9D  140.6        LL   293.0
#9     WY25WHLA9D  140.6        LR   359.4
#10    WY25WHLA9D  125.0        RL   437.5
#11    WY25WHLA9D  109.4        LR   671.9
#12    WY25WHLA9D  109.4        RL   484.4
#13    WY25WHLA9D  140.6        SR   515.6
#14    WY25WHLA9D  109.4        RL   500.0
#15    WY25WHLA9D  125.0        RR   312.5
#16    WY25WHLA9D   93.8        RL   375.0
#17    WY25WHLA9D   93.8        SR   359.4
#18    WY25WHLA9D   93.8        RR   265.6
#19    WY25WHLA9D  109.4        RL   265.6
#20    WY25WHLA9D  140.6        LR   421.9
#21    WY25WHLA9D   93.8        RL   437.5
#22    WY25WHLA9D  109.4        LR   609.4
#23    WY25WHLA9D  125.0        RL   468.8
#24    WY25WHLA9D  140.6        SR   500.0
#25    WY25WHLA9D  109.4        RL   531.3
#26    WY25WHLA9D  109.4        LR   656.3
#27    WY25WHLA9D  125.0        RR   265.6
#28    WY25WHLA9D  109.4        RL   312.5
#29    WY25WHLA9D  171.9        LS   578.1
#1480  WY25WHLA9D  125.0        LL   437.5
#1481  WY25WHLA9D   93.8        LL   578.1
#1482  WY25WHLA9D   78.1        LL   328.1
#1483  WY25WHLA9D  109.4        LL   546.9
#1484  WY25WHLA9D   93.8        LL   625.0
#1485  WY25WHLA9D   78.1        LR   234.4
#1486  WY25WHLA9D  109.4        RR   234.4
#1487  WY25WHLA9D   78.1        RL   265.6
#1488  WY25WHLA9D   93.8        LL   234.4
#1489  WY25WHLA9D   93.8        RR   265.6
#1490  WY25WHLA9D   46.9        RR   328.1
#1491  WY25WHLA9D   93.8        RR   203.1
#1492  WY25WHLA9D   78.1        LL   453.1
#1493  WY25WHLA9D  109.4        LL   578.1
#1494  WY25WHLA9D  156.3        LR   250.0
#1495  WY25WHLA9D  109.4        RL   125.0
#1496  WY25WHLA9D   78.1        LR   234.4
#1497  WY25WHLA9D  109.4        RR   234.4
#1498  WY25WHLA9D   78.1        LL   546.9
#1499  WY25WHLA9D   62.5        LL   406.3
#1500  WY25WHLA9D   93.8        LL   562.5
#1501  WY25WHLA9D   62.5        SL   640.6
#1502  WY25WHLA9D   93.8        LL   609.4
#1503  WY25WHLA9D   78.1        LR   265.6
#1504  WY25WHLA9D  125.0        RR   281.3
#1505  WY25WHLA9D   62.5        RL   312.5
#1506  WY25WHLA9D   62.5        LL   250.0
#1507  WY25WHLA9D   78.1        LR   375.0
#1508  WY25WHLA9D   62.5        RR   109.4
#1509  WY25WHLA9D  101.6        RR   625.0
#    print(df)
    
    df.loc[:, 'HTbins'] = df['Hold'].apply(locateBin)
    df.loc[:, 'FTbins'] = df['Flight'].apply(locateBin)
    
    
    fli = df.FTbins.value_counts(sort=False, normalize=True)
    fltbin = ['FTbin1', 'FTbin2', 'FTbin3', 'FTbin4', 'FTbin5', 'FTbin6', 'FTbin7', 'FTbin8', 'FTbin9', 'FTbin10']
    flidd = dict()
    for idx, i in enumerate(fltbin,1):
        if idx not in fli.index.tolist():
            flidd[i] = [0.]
        else:
            flidd[i] = [fli[idx]] 
    f = pd.DataFrame(flidd)
    
    hold = df.HTbins.value_counts(sort=False, normalize=True)
    holdbin = ['HTbin1', 'HTbin2', 'HTbin3', 'HTbin4', 'HTbin5', 'HTbin6', 'HTbin7', 'HTbin8', 'HTbin9', 'HTbin10']
    holddd = dict()
    for idx, i in enumerate(holdbin,1):
        if idx not in hold.index.tolist():
            holddd[i] = [0.]
        else:
            holddd[i] = [hold[idx]] 
    h = pd.DataFrame(holddd)
    
    newdf = pd.concat([f,h], axis=1) 

    userkey = df.iloc[0,0] 
    newdf.loc[:,'UserKey'] = userkey
    
    newdf.loc[:,'HTVar'] = df['Hold'].var()
    newdf.loc[:,'FTVar'] = df['Flight'].var()
    
    newdf.loc[:,'HTmean'] = df['Hold'].mean()
    newdf.loc[:,'FTmean'] = df['Flight'].mean()    
    
    
#    df.to_csv(, index=False)
    return newdf

def keystrokeDataForDF(injson, outpath):
    jsonf = readInJson(injson)
    #col_names = ['UserKey', 'Date','Timestamp','Hand','Hold', 'Direction','Latency', 'Flight']
    header = 'UserKey Date Timestamp Hand Hold Direction Latency Flight'
    
    if not os.path.exists(outpath):
        #os.makedirs(outpath)
        print("There are no cleaned up keystroke data to work with! Check your directory.")
        return 
    
    for k, v in jsonf.items():
        newK = os.path.basename(k)[-14:-4] + '.csv'
        tmpfile = os.path.join(outpath, newK)
        
        with open(tmpfile, 'w+') as wf:
            wf.write(header+"\n")
            for each_v in v:
                # below will combine all keystroke data file 
                new_v = os.path.basename(each_v)+'.csv'
                
                with open(os.path.join(outpath, new_v), 'r') as rf:
                    wf.write(rf.read())
#                    wf.write("\n")

        # After sets of keystroke data file are combined, let's use pd to extract feature we need
        df = pd.read_csv(tmpfile, sep = '\s+') #, header = None), names=col_names)
        df.drop('Date', axis=1, inplace=True )
        df.drop('Timestamp', axis=1, inplace=True )
        df.drop('Hand', axis=1, inplace=True )
        df.drop('Latency', axis=1, inplace=True )


        df = rmOutlier(df)
#        print("rm ",b4-len(df))

        
        
#        df = findmeanvar(df)        
#        df = findDescribe(df)
        df = findBins(df)
        
        
        
        
#        df.to_csv(tmpfile+'mean', index=False)
#        df.to_csv(tmpfile+'desc', index=False) 
        df.to_csv(tmpfile+'bins', index=False) 
        
    print("Keystrokes features are computed and ready for further merging with User.csv.")       
    
    return
    




def cleanUpData(targetDir, fpattern):    
    import os, glob
    from funcs import clean
    import constants
    
    new_dir = os.path.join(targetDir, "cleanup/discard")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    target = os.path.join(targetDir, fpattern)            
    for g in glob.glob(target):
        txtcsv = os.path.basename(g)+ '.csv'
        with open(g, 'r') as rawf:
            cleanpath = os.path.join(targetDir+'/cleanup', txtcsv)
            with open(cleanpath, 'w') as wf:
                for i, n in enumerate(rawf):
                    c = clean(n)
                    if (constants.discard == c):
                        dstr = "{} {}\n".format(i, n)
                        discardpath = os.path.join(targetDir+'/cleanup/discard', txtcsv+'.discard')
                        with open(discardpath, 'a') as dsf:
                            dsf.write(dstr)
                    else :
                        wf.write(c)  
    print("Clean up done. See {}".format(new_dir))
    return

def combine(targetDir, targetfile,  userDir, userfile, dataDir, dpattern):
    import os, glob
    import shutil
    
    usercsv = os.path.join(userDir,userfile)
    target = os.path.join(targetDir,targetfile)
    datacsv = os.path.join(dataDir,dpattern)
    
    try:
        shutil.copy(usercsv, target)
    except:
        print("shutil error out")
    
    u = pd.read_csv(target)
#    print(u)
    da=[] # contains all keystroke dataframes
    for g in glob.glob(datacsv):        
        ddf = pd.read_csv(g)
        da.append(ddf)

    allda = pd.concat(da)
    combineddf = pd.merge(u, allda, on='UserKey')
#    print(combineddf)
    combineddf.to_csv(target, index=False)
    
    
    return combineddf

def processNQData(UserKey, Parkinson, oricsv):
    last_rel = 0.0
    holdtime = 0.0
    flighttime = 0.0
    
    savedpath = os.path.dirname(oricsv)
    savedname = 'user' + UserKey + '.csv'
    savedfile = os.path.join(savedpath, savedname)
    if Parkinson == 'True':
        pks = 1
    else:
        pks = 0  
#    print("processNQData {} {}".format(Parkinson, pks))
    
    with open(savedfile, 'a+') as wf:
#        wf.write('UserKey, Parkinson, Hold, Flight\n')
        with open(oricsv, 'r') as rf:
            for i, r in enumerate(rf):
                
                    
                line = r.strip().split(",")
    #            print(line)
                ht = float(line[1])
                rel = float(line[2])
                press = float(line[3])
                
                if i == 0 and rel>0.0:
                    last_rel = rel
                elif i > 0:
                    
                    if (rel>press and press>0.0):
                        holdtime = ht
                        flighttime = press - last_rel
                        last_rel = rel
                    else:
                        if rel > last_rel:
                            last_rel = rel
                        continue # press, release time messed up
    #            print(i, "   ", holdtime, "     ",flighttime)
                if (holdtime>0.0 and flighttime > 0.0):
                        
                    record = "{},{},{},{}\n".format(UserKey, pks, holdtime*1000, flighttime*1000)
#                    print(record)
                    wf.write(record)
         
    return

def parseNQ(inFile):
    basepath = os.path.dirname(inFile)
    basename = os.path.basename(inFile)
    mitname = '/data_' + basename[-13:-4]
#    print("{} {} {}".format(basepath, basename, mitname))
    with open(inFile, 'r') as rfh:
        for r in rfh:
            
            row = r.strip().split(',')
            if row[0].startswith('pID'):
                continue
            for i, content in enumerate(row):
#                print("{} {}".format(i, content))
                if i==0:
                    UserKey = content
                if i==1:
                    Parkinson = content  
#                    print(Parkinson)
                if (i==7 or i==8):  
                    oricsv = os.path.join(basepath+mitname, content)
#                    print('processNQData(oricsv) {}'.format(oricsv))
                    if oricsv != "": 
                        processNQData(UserKey, Parkinson, oricsv)

                             
            
    
    return

def NQmean(path):
    
    dirname = os.path.dirname(path)
    
    header = 'UserKey,Parkinson,HTmean,FTmean\n'
    
    for f in glob.glob(path):
        fname = os.path.basename(f)+"mean"
        wpath = os.path.join(dirname, fname)
#        print(wpath)
#        col_names = ['UserKey', 'Parkinson', 'Hold','Flight']
        df = pd.read_csv(f)
#        print(df.head())
        user = df.iloc[0,0]
#        print(user)
        pks = df.iloc[0,1]
#        print(pks)
        HTmean = df['Hold'].mean()
        FTmean = df['Flight'].mean()

#        print("=",user, pks, HTmean, FTmean)
        wstr = "{},{},{},{}\n".format(user, pks, HTmean, FTmean)
#        print(wstr)
        with open(wpath, 'w') as wf:
            wf.write(header)
            wf.write(wstr)
        
    return

def NQDesc(path):
    from functools import reduce
    import operator
    
    for g in glob.glob(path):

        df = pd.read_csv(g)
        
        dfdesc = df[['Hold', 'Flight']].describe()
        dfdesc.loc['var',:]= df[['Hold', 'Flight']].var()
        dfdesc.drop('count', axis=0, inplace=True)

    
        v = dfdesc.values.tolist()
        colnames = ['HTmean', 'FTmean','HTstd', 'FTstd','HTmin', 'FTmin','HT25', 'FT25','HT50', 'FT50','HT75', 'FT75','HTmax', 'FTmax','HTvar', 'FTvar']
        r = reduce(operator.concat, v)
    
        m = map(lambda x,y: {x:y}, colnames, r)
        mm = list(m)
        
        dd = dict()
        for i in mm:
            dd[list(i.keys())[0]] = [list(i.values())[0]]
        
        loadeddf = pd.DataFrame(dd)
    
        loadeddf.loc[:,'UserKey'] = df.iloc[0,0]
        loadeddf.loc[:,'Parkinson'] = df.iloc[0,1]
        
        print(loadeddf.head())
        loadeddf.to_csv(g+'Desc', index=False)

    return

def NQBins(path):
    fltbin = ['FTbin1', 'FTbin2', 'FTbin3', 'FTbin4', 'FTbin5', 'FTbin6', 'FTbin7', 'FTbin8', 'FTbin9', 'FTbin10']
    holdbin = ['HTbin1', 'HTbin2', 'HTbin3', 'HTbin4', 'HTbin5', 'HTbin6', 'HTbin7', 'HTbin8', 'HTbin9', 'HTbin10']
  
    for g in glob.glob(path):

        df = pd.read_csv(g)  
#UserKey,Parkinson,Hold,Flight
#11,1,171.3,299.4999999999997
#11,1,143.2,146.70000000000005        
        df.loc[:, 'HTbins'] = df['Hold'].apply(locateBin)
        df.loc[:, 'FTbins'] = df['Flight'].apply(locateBin)
        
        
        fli = df.FTbins.value_counts(sort=False, normalize=True)
        flidd = dict()
        for idx, i in enumerate(fltbin,1):
            if idx not in fli.index.tolist():
                flidd[i] = [0.]
            else:
                flidd[i] = [fli[idx]] 
        f = pd.DataFrame(flidd)        

        hold = df.HTbins.value_counts(sort=False, normalize=True)
        holddd = dict()
        for idx, i in enumerate(holdbin,1):
            if idx not in hold.index.tolist():
                holddd[i] = [0.]
            else:
                holddd[i] = [hold[idx]] 
        h = pd.DataFrame(holddd)
        
        newdf = pd.concat([f,h], axis=1) 
    
        userkey = df.iloc[0,0] 
        newdf.loc[:,'UserKey'] = userkey
        
        newdf.loc[:,'HTVar'] = df['Hold'].var()
        newdf.loc[:,'FTVar'] = df['Flight'].var()
        
        newdf.loc[:,'HTmean'] = df['Hold'].mean()
        newdf.loc[:,'FTmean'] = df['Flight'].mean() 
    
        newdf.loc[:,'UserKey'] = df.iloc[0,0]
        newdf.loc[:,'Parkinson'] = df.iloc[0,1]
    
        newdf.to_csv(g+'Bins', index=False)
    return



def rmNQOutlier(path):
    dirname = os.path.dirname(path)
    
#    header = 'UserKey,Parkinson,HTmean,FTmean\n'
    
    for f in glob.glob(path):
        fname = os.path.basename(f)+"nooutlier"
        wpath = os.path.join(dirname, fname)
#        print(wpath)
        col_names = ['UserKey', 'Parkinson', 'Hold','Flight']
        df = pd.read_csv(f, names=col_names)
        
        for t in ['Hold','Flight']:
            q3 = df[t].quantile(0.75)
            q1 = df[t].quantile(0.25)
            iqr = q3 - q1   
            low_thresh = q1 - 1.5*iqr
            hi_thresh = q3 + 1.5*iqr
            
            # drop in place
            if t == 'Hold':
                df.drop(df[(df.Hold > hi_thresh)].index, inplace=True)
                df.drop(df[(df.Hold < low_thresh)].index, inplace=True)
            if t == 'Flight':
                df.drop(df[(df.Flight > hi_thresh)].index, inplace=True)
                df.drop(df[(df.Flight < low_thresh)].index, inplace=True)     
      
        df.to_csv(wpath,index=False)
            
        
    return


def combineNQ(listDirs, fp):
    df = pd.DataFrame()
    for i in listDirs:
        forglob = os.path.join(i,fp)
        for g in glob.glob(forglob):
            gdf = pd.read_csv(g)
            df = df.append(gdf)
    df.to_csv('dfData/nqdf.csv', index=False)
    return
