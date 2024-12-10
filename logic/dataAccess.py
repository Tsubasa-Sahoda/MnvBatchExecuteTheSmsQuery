import psycopg2
import pandas
import traceback
import common.put_log as putLog
import time
import sys
from datetime import datetime as dTime
import common.config as conf

config = conf.testConfig()

LOG_FILE = config.LOG_FILE

log = None
logs = []


class dataAccess():
    def getData(self, psql: str, connection_config):

        dataframe = None
        try:
            with psycopg2.connect(**connection_config) as config:
                for _ in range(3):  # 最大3回実行
                    try:
                        # クエリを実行
                        dataframe = pandas.read_sql(sql=psql, con=config)
                        substitutedData = dataframe.fillna('')
                    except Exception as e:
                        log = '--【dataAccess】実行失敗の為繰り返し  {} : {}'.format(dTime.now())
                        putLog.writeLog(LOG_FILE, 'Info', log, logs)
                        log = traceback.format_exc()
                        putLog.writeLog(LOG_FILE, 'Info', log, logs)
                        # 60秒後に再実行
                        time.sleep(60)
                    else:
                        return substitutedData  # 失敗しなかった時はループを抜ける
                else:
                    log = '--【dataAccess】最大試行回数に達しました。処理を中断します  {} : {}'.format(dTime.now())
                    putLog.writeLog(LOG_FILE, 'Info', log, logs)
                    log = traceback.format_exc()
                    putLog.writeLog(LOG_FILE, 'Info', log, logs)
                    raise Exception

        except Exception as e:
            log = traceback.format_exc()
            putLog.writeLog(LOG_FILE, 'Info', log, logs)
            raise Exception

