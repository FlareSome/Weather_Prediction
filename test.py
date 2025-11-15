import pandas as pd

df = pd.read_csv("raw_data.csv")
print(df.head(20))
print(df.tail(20))
print(df.dtypes)
