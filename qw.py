import pandas as pd
import os

def Import_Excel_pandas():
    empexceldata = pd.read_excel("Copia Cash Flow.xlsx"[['']])        
    dbframe = empexceldata
    print(dbframe)
    for dbframe in dbframe.itertuples():
        print(dbframe.Monto_Total)
        
z=Import_Excel_pandas()
       