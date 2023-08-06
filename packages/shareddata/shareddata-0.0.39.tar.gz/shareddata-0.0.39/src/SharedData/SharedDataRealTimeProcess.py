import os,time,sys
import pandas as pd
import numpy as np
from pathlib import Path

# print(sys.path)
# # ..venv/Scripts/python.exe
# path = str(Path(sys.executable).parents[2])
# sys.path.insert(0,path)

from SharedData.Logger import Logger
logger = Logger(__file__)
from SharedData.SharedData import SharedData
from SharedData.SharedDataAWSKinesis import KinesisStreamConsumer

database = 'MarketData'
streamname = os.environ['BASE_STREAM_NAME']+'-'+database.lower()
profilename = os.environ['REALTIME_PROFILENAME']
user = os.environ['USER_COMPUTER']
today = pd.Timestamp(pd.Timestamp.now().date())

Logger.log.info('Starting SharedData real time'+\
    ' subscription database:%s' % (database))

consumer = KinesisStreamConsumer(streamname,profilename)
shdata = SharedData(database,sync_frequency_days=0)

dfwatchdog = shdata['RT']['D1'][today]
dfwatchdog.loc[database,'watchdog'] = time.time()

Logger.log.info('SharedData real time'+\
    ' subscription database:%s STARTED!' % (database))
while True:
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
    dfwatchdog.loc[database,'watchdog'] = time.time()
    time.sleep(1)