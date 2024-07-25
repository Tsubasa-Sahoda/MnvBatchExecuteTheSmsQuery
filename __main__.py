import pandas as pd
import traceback
import common.config as conf
import common.put_log as putLog
import logic.dataAccess as getdt
import logic.fileControl as flctrl
import logic.send_mail as mail
import os
import shutil

import time
import datetime
from datetime import datetime as dTime
from pathlib import Path

# 環境変数
# 本番
# config = conf.config()

# テスト
config = conf.testConfig()

fc = flctrl.fileControl()
dataAccess = getdt.dataAccess()

# 定数
LOG_FILE = config.LOG_FILE
CUR_FILE = config.CUR_FILE
CUR_FILE_JP = config.CUR_FILE_JP


log = None
logs = []
date_now = dTime.now()
today = datetime.date.today()
err_flg = False

# 実行年月日を文字列に変換
fileDate = today.strftime('%Y%m%d')

if __name__ == '__main__':
    try:
        log = '【処理開始】{} : {}'.format(CUR_FILE, date_now.strftime('%Y-%m-%d %H:%M:%S'))
        putLog.writeLog(LOG_FILE, 'Info', log, logs)

        # SQLの格納先を取得
        queryPath = config.smsQueryPath

        # DB接続情報を取得
        if queryPath == config.smsQueryPath:
            dbConfig = config.mcpConfig

        # 格納先のSQLファイルの情報をすべて取得
        paths = fc.getFileList(queryPath)

        # 出力先情報取得
        exportPass = config.exportPass

        # 旧出力ファイル格納先
        oldFilePass = config.oldFilePass

        list_file_name =  os.listdir(exportPass)

        log = '[旧ファイル移動]'
        putLog.writeLog(LOG_FILE, 'Info', log, logs)

        # oldフォルダの存在チェック
        os.makedirs(oldFilePass, exist_ok=True)

        # 出力先直下にある古いファイルを全てoldフォルダへ移動
        for i_file_name in list_file_name:

            join_path = os.path.join(exportPass,i_file_name)
            move_path = os.path.join(oldFilePass,i_file_name)

            if os.path.isfile(join_path):

                fileName = os.path.splitext(os.path.basename(join_path))[0]
                log = '--ファイル移動開始  {} : {}'.format(fileName, dTime.now())
                putLog.writeLog(LOG_FILE, 'Info', log, logs)

                shutil.move(join_path,move_path)

                log = '--ファイル移動完了  {} : {}'.format(fileName, dTime.now())
                putLog.writeLog(LOG_FILE, 'Info', log, logs)


        # SQLファイル数分ループ
        for path in paths:

            # 実行するSQLファイルを読み込み
            sSql = fc.leadQueryFile(path)

            exe_start = dTime.now()

            sqlName = os.path.splitext(os.path.basename(path))[0]

            log = '[SQL]'
            putLog.writeLog(LOG_FILE, 'Info', log, logs)

            log = '--SQL実行開始  {} : {}'.format(sqlName, exe_start)
            putLog.writeLog(LOG_FILE, 'Info', log, logs)

            # クエリ実行
            df_main = dataAccess.getData(sSql,dbConfig)

            # exe_diff = dTime.now() - exe_start
            log = '--SQL実行完了  {} : {}'.format(sqlName, dTime.now())
            putLog.writeLog(LOG_FILE, 'Info', log, logs)

            log = '--SQL実行時間  {} : {}'.format(sqlName, dTime.now() - exe_start)
            putLog.writeLog(LOG_FILE, 'Info', log, logs)


            # 実行結果をデータフレーム化
            df = pd.DataFrame(df_main)

            # ファイル出力（上書き）
            try:
                # 出力ファイル名の設定
                fileName = fc.getFileName(fileDate,path)

                log = '[CSV]'
                putLog.writeLog(LOG_FILE, 'Info', log, logs)

                write_start = dTime.now()
                log = '--CSV出力開始  {} : {}'.format(fileName, write_start, encoding='utf-8_sig')
                putLog.writeLog(LOG_FILE, 'Info', log, logs)

                # CSVファイル化
                df.to_csv(Path(exportPass, fileName), mode='w+', index = False, encoding='utf-8_sig')

                diff_time = dTime.now() - write_start

                log = '--CSV出力完了  {}: {}'.format(fileName, dTime.now())
                putLog.writeLog(LOG_FILE, 'Info', log, logs)

                data_count = df.shape[0]
                log = '--CSV出力件数  {} : {}'.format(fileName, data_count)
                putLog.writeLog(LOG_FILE, 'Info', log, logs)

                log = '--出力実行時間  {} : {}'.format(fileName, diff_time)
                putLog.writeLog(LOG_FILE, 'Info', log, logs)



            except Exception as e:
                log = '　　Exception Error: %s' % e
                putLog.writeLog(LOG_FILE, 'Exception', log, logs)
                log = '×-出力失敗'.format(fileName)
                putLog.writeLog(LOG_FILE, 'Error', log, logs)
                err_flg = True
                traceback.print_exc()

        log = "\n".join(logs)
        diff_time = dTime.now() - date_now
        log = '［所要時間］{} ： {}'.format(CUR_FILE, diff_time)
        putLog.writeLog(LOG_FILE, 'Info', log, logs)

        date_now = dTime.now()
        log = '【処理終了】{} ： {}'.format(CUR_FILE, date_now.strftime('%Y-%m-%d %H:%M:%S'))
        putLog.writeLog(LOG_FILE, 'Info', log, logs)
        if err_flg:
            #異常終了時
            mail.sendEmail_ProcAbend(CUR_FILE_JP, log)
        else:
            #正常終了時
            mail.sendEmail_ProcEnd(CUR_FILE_JP, log)

    except TypeError:
        traceback.print_exc()
    except ValueError:
        traceback.print_exc()
    except Exception:
        print("------------------------------------------main_Exception----------------------------------------------")
        traceback.print_exc()
