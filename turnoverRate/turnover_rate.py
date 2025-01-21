import pandas as pd
loan_data = pd.read_csv("processed_data.csv")  # 대출 정보
book_data = pd.read_csv("processed_bookInformation.csv", dtype={"출판년도": "str"})  # 도서 정보

# 작가, 제목, 출판년도로 대출 횟수 집계
merged_loans = pd.merge(loan_data, book_data, on="도서ID", how="inner")

# 작가, 제목, 출판년도 기준으로 대출 횟수 집계
loan_counts = merged_loans.groupby(["저자", "서명", "출판년도"]).size().reset_index(name="대출횟수")

# 작가, 제목, 출판년도로 소장 권수 집계-> 동일 기준으로 book_data에서 소장 권수 계산
book_counts = book_data.groupby(["저자", "서명", "출판년도"]).size().reset_index(name="소장권수")

# 4대출 데이터와 소장 데이터 병합
result = pd.merge(book_counts, loan_counts, on=["저자", "서명", "출판년도"], how="left")
# result = pd.merge(result, book_data[["저자", "서명", "출판년도", "분류코드"]], on=["저자", "서명", "출판년도"], how="left")
# 동일한 기준으로 도서 정보에서 분류코드 병합
book_metadata = book_data[["저자", "서명", "출판년도", "분류코드"]].drop_duplicates()
result = pd.merge(result, book_metadata, on=["저자", "서명", "출판년도"], how="left")

# 대출 기록이 없는 경우 대출횟수를 0으로 설정
result["대출횟수"] = result["대출횟수"].fillna(0)

# 장서회전율 계산
result["장서회전율"] = (result["대출횟수"] / result["소장권수"]).round(2)

# 장르별 장서회전율 계산
genre_rotation = result.groupby("분류코드")["장서회전율"].mean().reset_index(name="장르별_평균_장서회전율").round(2)

# 장서회전율이 낮은 도서 식별
# low_rotation_books = result[result["장서회전율"] < 1]  # 기준: 장서회전율 < 1


result.to_csv("merged_book_data_with_rotation.csv", index=False)  # 장서회전율 포함 전체 데이터
genre_rotation.to_csv("genre_rotation.csv", index=False)  # 장르별 평균 장서회전율
# low_rotation_books.to_csv("low_rotation_books.csv", index=False)  # 장서회전율이 낮은 도서 목록

