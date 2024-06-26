import pandas as pd

si=pd.read_csv('results.csv')

print(len(si["URL"].unique()))