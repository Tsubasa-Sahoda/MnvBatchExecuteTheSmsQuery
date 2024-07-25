import psycopg2
import pandas
import traceback
import config

class dataAccess():
    def getData(self,psql: str,connection_config):

        dataframe=None
        try:
            with psycopg2.connect(**connection_config) as config:
                # クエリを実行
                dataframe = pandas.read_sql(sql=psql, con=config)
                substitutedData = dataframe.fillna('')

            return substitutedData
        except Exception as e:
            raise e

