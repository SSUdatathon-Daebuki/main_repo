import pandas as pd

# 대출 정보 파일 경로 지정
file_path = '대출정보.txt'

"""
- 인코딩: euc-kr
- 문자열 구분자: "
"""
df = pd.read_csv(file_path, encoding='euc-kr', quotechar='"')

# '대출일시' 열을 datetime 형식으로 변환
df['대출일시'] = pd.to_datetime(df['대출일시'])

# 변환된 '대출일시'에서 연도 정보를 추출하여 '대출 년도' 열 추가
df['대출 년도'] = df['대출일시'].dt.year

# '도서ID'와 '대출 년도' 열을 csv 파일로 저장
df[['도서ID', '대출 년도']].to_csv('processed_data.csv', index=False, encoding='utf-8-sig')