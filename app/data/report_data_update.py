import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('moneymarketfund_data.db', check_same_thread=False)
extraction_datetime = datetime.now()
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