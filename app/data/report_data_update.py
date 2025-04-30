import sqlite3
import pandas as pd
from pathlib import Path

conn = sqlite3.connect('app/data/moneymarketfund_data.db', check_same_thread=False)
data_folder = Path('C:/Users/Toshiba/Desktop/')
file_to_open = data_folder/"report_data.csv"
csv_file = pd.read_csv(file_to_open)
df = pd.DataFrame(csv_file)
df.to_csv('app/data/report_data.csv', index=False)

report_file = 'report_data.csv'

df: pd.DataFrame = pd.read_csv(report_file, usecols=['report_id', 'week_number', 'firm_rate', 'firm_id', 'last_changed_date'])
# df['extraction_date'] = extraction_datetime
# df['is_public'] = True

df.to_sql('report_temp', conn, if_exists='replace', index=False)
conn.execute("""
    INSERT INTO report(report_id, week_number, firm_rate, firm_id, last_changed_date)
    SELECT
        report_temp.report_id,
        report_temp.week_number,
        report_temp.firm_rate,
        report_temp.firm_id,
        report_temp.last_changed_date
    FROM 
        report_temp
    WHERE NOT EXISTS (
        SELECT 1 FROM report WHERE report.report_id = report_temp.report_id)
""")
conn.execute('DROP TABLE IF EXISTS report_temp')
conn.commit()