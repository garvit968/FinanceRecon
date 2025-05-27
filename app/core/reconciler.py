import pandas as pd
from typing import List

def reconcile_files(file_path1: str, file_path2:str, on_column: List[str]):
    df1=pd.read_csv(file_path1)
    df2=pd.read_csv(file_path2)

    matched = pd.merge(df1,df2,on=on_column, how='inner')
    unmatched1 = df1.merge()