import os,time,sys
import pandas as pd
import numpy as np
from pathlib import Path

from SharedData.Logger import Logger
logger = Logger(__file__)
from SharedData.SharedData import SharedData
from SharedData.SharedDataAWSKinesis import KinesisStreamConsumer


try:
    if len(sys.argv)>=2:
        database = str(sys.argv[1])
    else:
        database = 'MarketData'

    SLEEP_TIME = 5

    streamname = os.environ['BASE_STREAM_NAME']+'-'+database.lower()
    profilename = os.environ['REALTIME_PROFILENAME']
    user = os.environ['USER_COMPUTER']

    Logger.log.info('Starting SharedData real time'+\
        ' subscription database:%s' % (database))

    consumer = KinesisStreamConsumer(streamname,profilename)
    shdata = SharedData(database,sync_frequency_days=0)

    Logger.log.info('SharedData real time'+\
        ' subscription database:%s STARTED!' % (database))

    today = pd.Timestamp(pd.Timestamp.now().date())
    lastdate = today
    while True:
        today = pd.Timestamp(pd.Timestamp.now().date())
        wd = shdata['RT/Watchdog']['D1']        
        if today!=lastdate:            
            wd[today] = wd[lastdate].copy()
            wd.tags[today].Write()
        dfwatchdog = wd[today]
        dfwatchdog.loc[database,'watchdog'] = time.time()

        consumer.consume()
        for msg in consumer.stream_buffer:
            if msg['sender'] != user:
                if msg['msgtype']=='df':
                    tag = pd.Timestamp(msg['tag'])
                    data = np.array(msg['data'])
                    df = shdata[msg['feeder']][msg['period']][tag]
                    df.loc[msg['idx'],msg['col']] = data
                elif msg['msgtype']=='ts':
                    data = np.array(msg['data'])
                    idx = pd.to_datetime(msg['idx'])
                    df = shdata[msg['feeder']][msg['period']][msg['tag']]
                    df.loc[idx,msg['col']] = data

        consumer.stream_buffer = []        
        time.sleep(SLEEP_TIME+np.random.rand()-0.5)
except Exception as e:        
    Logger.log.error('SharedData real time'+\
        ' subscription database:%s ERROR: %s!' % (database,str(e)))