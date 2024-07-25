import common.config as conf
import glob
import os

config = conf.config()

class fileControl():

    # ディレクトリ内のSQLファイルのパスをすべて取得
    def getFileList(self,queryPath):
        files = glob.glob(os.path.join(queryPath, '*.sql'))
        return files

    # SQLファイルの読み込み
    def leadQueryFile(self,path):
        try:
            with open(path, 'r', encoding='UTF-8') as f:
                sSql = f.read()
            return sSql
        except Exception as e:
            raise e

    # SQLファイル名から出力ファイル名を作成
    def getFileName(self,fileDate,queryPath):
        fileName  = fileDate + '_' + os.path.splitext(os.path.basename(queryPath))[0] + '.csv'
        return fileName

