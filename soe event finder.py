# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:55:10 2024

@author: ananthakrishnan.m
"""

import pandas as pd
import datetime as dt
from scada_fetcher import fetchPntHistData

configExcelPath = "NEWProcessed_Output.xlsx"
sampleFreqSecs = 60
# startDatestr = "18-11-2024 09:00:00"
# startDt = dt.datetime.strptime(startDatestr,"%d-%m-%Y %H:%M:%S")
# endDatestr = "18-11-2024 21:00:00"
# endDt = dt.datetime.strptime(endDatestr,"%d-%m-%Y %H:%M:%S")
sht="Sheet1"
resDataDf = pd.DataFrame()
resStatusDf = pd.DataFrame()
genNames = []
print(f"{sht} report is being generated")
    # get pnts
    # TODO handle duplicate points in config sheet
pntsDf = pd.read_excel(configExcelPath, sheet_name=sht)
reportDf = pd.DataFrame()
# df1= pd.DataFrame()
for itr in range(pntsDf.shape[0]):
        startDt=pntsDf['Start Time'].iloc[itr]
        #startDt = dt.datetime.strptime(startDatestr,"%d-%m-%Y %H:%M:%S")
        endDt =pntsDf['End Time'].iloc[itr]
       # endDt = dt.datetime.strptime(endDatestr,"%d-%m-%Y %H:%M:%S")
        pnt = pntsDf.iloc[itr, 4]
        pntName = pntsDf.iloc[itr, 3]
        print('{0} - {1}'.format(itr+1, pnt))
        pntData = fetchPntHistData(pnt, startDt, endDt, 'snap', sampleFreqSecs)
        if len(pntData) > 0:
            tsList = [dt.datetime.strptime(t['timestamp'].replace('T',' '), "%Y-%m-%d %H:%M:%S") for t in pntData]
            samplsList = [t['dval'] for t in pntData]
            statusList = [t['status'] for t in pntData]
            samplsDf = pd.DataFrame({"time{0}".format(itr+1):tsList, pntName:samplsList})
            resDataDf = pd.concat([resDataDf, samplsDf],axis=1)
            statusDf = pd.DataFrame({"time{0}".format(itr+1):tsList, pntName:statusList})
            resStatusDf = pd.concat([resStatusDf, statusDf],axis=1)
  
        #     pntData = [{pntName: s["dval"], "Timestamp": dt.datetime.strptime(
        #         s['timestamp'].replace('T', ' '), "%Y-%m-%d %H:%M:%S")} for s in pntData]
        #     pntDataDf = pd.DataFrame(pntData).set_index("Timestamp")
        # else:
        #     pntDataDf = pd.DataFrame(columns=[pntName])
        # reportDf = reportDf.merge(
        #     pntDataDf, how="outer", left_index=True, right_index=True)
dumpFilename = r'{0}_{1}.xlsx'.format(sht, dt.datetime.strftime(startDt, "%d_%m_%Y"))

with pd.ExcelWriter(dumpFilename) as writer:
    resDataDf.to_excel(writer, index = False, sheet_name='data')
    resStatusDf.to_excel(writer, index = False, sheet_name='status')
    
for i in range(1,resDataDf.shape[1],2):
    k=int((i+1)/2-1)
    if((resDataDf.iloc[0, i]>-0.5 and resDataDf.iloc[0, i]<0.5) and (resDataDf.iloc[-1, i]<-0.5 or resDataDf.iloc[-1, i]>0.5)):
        print(pntsDf.iloc[k,2]+" came to service at "+str(pntsDf.iloc[k,5]))
    elif((resDataDf.iloc[0, i]<-0.5 or resDataDf.iloc[0, i]>0.5) and (resDataDf.iloc[-1, i]>-0.5 and resDataDf.iloc[-1, i]<0.5)):
        print(pntsDf.iloc[k,2]+" outage taken at "+str(pntsDf.iloc[k,5]))
#        print(pntsDf.iloc[i-1,2]+"outage taken at"+(pntsDf.iloc[i-1,5]))