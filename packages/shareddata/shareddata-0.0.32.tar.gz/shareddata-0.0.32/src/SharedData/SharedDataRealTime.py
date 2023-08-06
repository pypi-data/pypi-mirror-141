import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

from SharedData.Logger import Logger
from SharedData.SharedData import SharedData
from SharedData.SharedDataAWSKinesis import KinesisStreamProducer

class SharedDataRealTime:
    
    producer = None
    consumer = None

    def __init__(self, database):
        if Logger.log is None:            
            Logger('SharedDataRealTime')
        
        Logger.log.debug('Initializing SharedDataRealTime %s,%s ...' % (database))
        
        self.database = database
        
        self.producer = KinesisStreamProducer
                
        Logger.log.debug('Initializing SharedData %s,%s DONE!' % (database))
