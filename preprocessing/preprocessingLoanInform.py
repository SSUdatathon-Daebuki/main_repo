import pandas as pd

file_path = '대출정보.txt'

df = pd.read_csv(file_path, encoding='euc-kr', quotechar='"')


df['대출일시'] = pd.to_datetime(df['대출일시']) 
df['대출 년도'] = df['대출일시'].dt.year        

print(df[['도서ID', '대출 년도']])

df[['도서ID', '대출 년도']].to_csv('processed_data.csv', index=False, encoding='utf-8-sig')