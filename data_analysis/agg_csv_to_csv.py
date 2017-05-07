import sqlite3
import pandas as pd
import os

conn = sqlite3.connect('temp.db') # create a temp db file
data = pd.read_csv('data_full.csv')
sql = data.to_sql('data_data', conn, if_exists='append', index=False) # convert csv to sql

statement = """select time_start, cell_grp AS 'Region',
                  count(1) AS 'Total Connections', 
          round(sum(mb)/1000) AS 'what is this', 
          sum(case when mb <= 50 then 1 else 0 end) as '1-50',
          sum(case when mb > 50 and mb <= 100 then 1 else 0 end) as '50-100',
          sum(case when mb > 100 and mb <= 200 then 1 else 0 end) as '100-200',
          sum(case when mb > 200 then 1 else 0 end) as '>200'
              from data_data where time_start >= '2017-03-02 12:00:01'
              and time_start <= '2017-03-03 00:00:00'
              and id not in (155270403,51334913,179199746)
              group by time_start, cell_grp order by time_start"""



sql = pd.read_sql(statement, conn) # aggregate the data
sql.to_csv('aggregated_data_snippet.csv') # write to file 
conn.close()
os.remove('temp.db')
