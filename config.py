import time
import os
import os, sys
from pathlib import Path


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
smsQueryPath = r'C:\Users\s12100400\develop\SMSバッチ\SQL\test'



# 実行結果出力先
exportPass = r'C:\Users\s12100400\develop\SMSバッチ\CSV\test'
