import pandas as pd

# 데이터 불러오기
book_data_raw = pd.read_csv("단행본(도서)정보.txt", encoding="euc-kr", dtype={"등록일자": "str", "분류코드": "str"})
book_data_processed = pd.read_csv("processed_bookInformation.csv", dtype={"등록일자": "str", "분류코드": "str"})

# 열 이름 정리 (공백 제거)
book_data_raw.columns = book_data_raw.columns.str.strip()  # 앞뒤 공백 제거
book_data_processed.columns = book_data_processed.columns.str.strip()

# 등록일자 형식 변환 (문자열을 날짜 형식으로 변환)
book_data_raw["등록일자"] = pd.to_datetime(book_data_raw["등록일자"], errors="coerce")  # 오류 발생 시 NaT 처리

# 등록일자에서 년도-월 추출 (등록월)
book_data_raw["등록월"] = book_data_raw["등록일자"].dt.to_period("M")  # 월별로 period형으로 변환

# `processed_bookInformation.csv`와 `단행본(도서)정보.txt`를 `도서ID` 기준으로 병합
merged_data = pd.merge(book_data_raw, book_data_processed[["도서ID", "분류코드"]], on="도서ID", how="left")

# `분류코드_x`와 `분류코드_y`가 있을 경우, `분류코드_y`를 선택하여 새로운 컬럼을 만들거나, 두 열을 합쳐서 처리합니다.
merged_data["분류코드"] = merged_data["분류코드_y"]  # '분류코드_y'가 유효하다면 이 값을 사용

# # 병합 후 열 목록 확인
# print("병합 후 열 목록:", merged_data.columns)

# 월별 & 장르별 도서 수 집계
monthly_genre_counts = merged_data.groupby(["등록월", "분류코드"]).size().reset_index(name="등록도서수")

# 장르별 월평균 등록 도서 수 계산
genre_monthly_avg = monthly_genre_counts.groupby("분류코드")["등록도서수"].mean().reset_index(name="월평균_등록도서수")

# # 결과 출력
# print("월별 & 장르별 등록 도서 수:")
# print(monthly_genre_counts)

# print("\n장르별 월평균 등록 도서 수:")
# print(genre_monthly_avg)

# 결과 저장
monthly_genre_counts.to_csv("monthly_genre_counts.csv", index=False)  # 월별 & 장르별 도서 수
# genre_monthly_avg.to_csv("genre_monthly_avg.csv", index=False)  # 장르별 월평균 등록 도서 수

