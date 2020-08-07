import pandas as pd
df = pd.read_csv('test.csv')
# print(df.head())
item_code = 1
new_record = 1
for index, row in df.iterrows():
    print(row['Department'])
