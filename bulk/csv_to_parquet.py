import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def csv_to_parquet(input_filename, output_filename: str):
    source_df = pd.read_csv(input_filename)

    source_table = pa.Table.from_pandas(source_df)

    pq.write_table(source_table, output_filename)


if __name__ == '__main__':
    csv_to_parquet("firms_data.csv","firms_data.parquet")
    csv_to_parquet("report_data.csv","report_data.parquet")