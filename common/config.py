import time
import os
import os, sys
from pathlib import Path

class config():
    # DB接続情報
    #MCP2
    mcpConfig = {
                'user': 'mnvmuser',
                'password': 'mnvmuser',
                'host': 'vm03-pc21115.mycom.local',
                'port': '15433',
                'database': 'cp2_prod_mnvm_dms'
            }



    # クエリファイル格納先
    smsQueryPath = 'sql_exec'



    # 実行結果出力先
    exportPass = r'\\CPFS21\order01\sk-system_manager\99-データフォルダ\【04】コンソールデータ_バッヂ'

    # 旧ファイル出力先
    oldFilePass = r'\\CPFS21\order01\sk-system_manager\99-データフォルダ\【04】コンソールデータ_バッヂ\old'

    mail = {
        'host': 'mail.int.mynavi-agent.jp',
        'port': '25',
        'timeout': '60',
        'from': 'MAGシステム <mag-system@mynavi.jp>',
        'to': 'nishitsubo.satomi.qv@mynavi.jp',
        'to2': 'sahoda.tsubasa.oe@mynavi.jp',
        'to3': 'tsunegi.satoko.nr@mynavi.jp'
    }

    flag = {
        'test': False,  # False / True
        'batch': True,
        'produp': True,
        'stgup': True
    }


    # 定数
    LOG_FILE = 'MnvBatchExecuteTheSmsQuery'
    CUR_FILE = "MnvBatchExecuteTheSmsQuery"
    CUR_FILE_JP = "SMSコンソール出力バッチ"
    SUCESS_MAIL_TEMP = '/Template/Email/【汎用】処理完了.txt'
    ERROR_MAIL_TEMP = '/Template/Email/【汎用】エラー発生.txt'


class testConfig():
    # DB接続情報
    #MCP2
    mcpConfig = {
                'user': 'mnvmuser',
                'password': 'mnvmuser',
                'host': 'vm03-pc21115.mycom.local',
                'port': '15433',
                'database': 'cp2_prod_mnvm_dms'
            }



    # クエリファイル格納先
    # smsQueryPath = r'C:\Users\s12100400\develop\SMSバッチ\SQL\test'
    smsQueryPath = 'sql_exec'



    # 実行結果出力先
    # exportPass = r'C:\Users\s12100400\develop\SMSバッチ\CSV\test'
    exportPass = r'\\CPFS21\order01\sk-system_manager\99-データフォルダ\【04】コンソールデータ_バッヂ'

    oldFilePass = r'C:\Users\s12100400\develop\SMSバッチ\CSV\test\old'

    mail = {
        'host': 'mail.int.mynavi-agent.jp',
        'port': '25',
        'timeout': 60,
        'from': 'MAGシステム <mag-system@mynavi.jp>',
        # 'to': 'MAGシステム <mag-system@mynavi.jp>',
        'to': 'sahoda.tsubasa.oe@mynavi.jp'
        # 'to2': 'MAGシステム <mag-system@mynavi.jp>'
    }

    flag = {
        'test': False,  # False / True
        'batch': True,
        'produp': True,
        'stgup': True
    }


    # 定数
    LOG_FILE = 'MnvBatchExecuteTheSmsQuery'
    CUR_FILE = "MnvBatchExecuteTheSmsQuery"
    CUR_FILE_JP = "【TEST】SMSコンソール出力バッチ"
    SUCESS_MAIL_TEMP = '/Template/Email/【汎用】処理完了.txt'
    ERROR_MAIL_TEMP = '/Template/Email/【汎用】エラー発生.txt'

