######################################################################
#  put_log.py
#
#＜処理内容＞
#  ログファイルを出力する
#
#＜修正履歴＞
#  2022.01.05 : 新規作成
#
######################################################################
import os
import yaml
from logging import config as logconf, getLogger
from datetime import datetime as dt
import common.config as Conf

# 環境変数
conf = Conf.config()

# FLG_TEST = conf.FLAG['test'] # テストフラグ

# LOG出力準備
LOG_FILE = os.getcwd() + '/conf/log_config.yaml'
logconf.dictConfig(yaml.safe_load(open(LOG_FILE).read()))

# 初期化
logger = getLogger()


##---------------------------------------------------------
## ログファイルに書き込む
##---------------------------------------------------------
def writeLog(file: str, type: str, log: str, logs: list) -> list:

	logger = getLogger(file)

	if type == 'Error':
		logger.error(log)
	elif type == 'Exception':
		logger.exception(log)
	else:
		logger.info(log)

	print(log) #if(FLG_TEST) else None

	logs.append(log)

	return logs


##===================================================================
if __name__ == "__main__":

	logs = []

	log = '【処理開始】'
	writeLog('schtasks', 'Info', log, logs)

	log = '【処理終了】'
	writeLog('schtasks', 'Info', log, logs)

	print(logs)