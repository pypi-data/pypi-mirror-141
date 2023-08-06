import os,time
import pandas as pd
import numpy as np

from SharedData.Logger import Logger
logger = Logger(__file__)
from SharedData.SharedData import SharedData
from SharedData.SharedDataAWSKinesis import KinesisStreamConsumer

database = 'MarketData'
streamname = os.environ['BASE_STREAM_NAME']+'-'+database.lower()
profilename = os.environ['REALTIME_PROFILENAME']
user = os.environ['USER_COMPUTER']

Logger.log.info('Starting SharedData real time subscription database:%s' % (database))

consumer = KinesisStreamConsumer(streamname,profilename)
shdata = SharedData(database)

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
                pass

    consumer.stream_buffer = []
    time.sleep(1)