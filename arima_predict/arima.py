import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# 데이터 로드
file_path = "monthly_genre_counts.csv"
data = pd.read_csv(file_path)

# 백의자리로 분류코드 변환
data['장르'] = (data['분류코드'] // 100) * 100

# 월별 등록도서수 집계
data['등록월'] = pd.to_datetime(data['등록월'])
genre_monthly_counts = data.groupby(['등록월', '장르'])['등록도서수'].sum().unstack(fill_value=0)

# 데이터 확인
print("Monthly Genre Counts:\n", genre_monthly_counts.head())

# 예측을 위한 함수 정의
def predict_genre_books_arima(genre_monthly_counts, periods=12):
    predictions = {}
    prediction_dates = pd.date_range(
        start=genre_monthly_counts.index[-1] + pd.DateOffset(months=1),
        periods=periods,
        freq='M'
    )

    for genre in genre_monthly_counts.columns:
        genre_data = genre_monthly_counts[genre]

        # 최소 데이터 길이 확인
        if len(genre_data) < 5:
            print(f"Not enough data for genre {genre}, skipping...")
            continue

        try:
            # ARIMA 모델 학습
            model = ARIMA(genre_data, order=(5, 1, 0))
            fit = model.fit()

            # 예측
            future = fit.forecast(steps=periods)
            predictions[genre] = np.round(future.values, 2)  # 예측 결과 소수점 둘째 자리로 반올림

            # 결과 시각화
            plt.figure(figsize=(10, 6))
            plt.plot(genre_data.index, genre_data, label="Actual", color="blue")
            plt.plot(
                prediction_dates,
                future,
                label="Forecast",
                linestyle="--",
                color="orange"
            )

            # 그래프의 y축 범위 설정 (예측값 포함)
            max_y = max(genre_data.max(), future.max()) * 1.2  # 최대값의 120%로 설정
            plt.ylim(0, max_y)

            plt.title(f"Genre {genre} Forecast")
            plt.legend()
            plt.show(block=False)  # 그래프 표시
            input("다음 그래프로 넘어가려면 Enter 키를 누르세요...")  # Enter 입력 대기
            plt.close()  # 창 닫기
        except Exception as e:
            print(f"Error with genre {genre}: {e}")
            continue

    # 예측 결과를 데이터프레임으로 반환
    prediction_df = pd.DataFrame(predictions, index=prediction_dates)
    prediction_df.index.name = "Date" 
    prediction_df.index = prediction_df.index.strftime('%Y-%m')

    return prediction_df

# 예측 실행
predicted_counts = predict_genre_books_arima(genre_monthly_counts)

# 예측 결과 저장
output_file = "predicted_genre_counts_fixed.csv"
predicted_counts.to_csv(output_file)
print(f"Predicted counts saved to {output_file}")

#+++++++++++++++++++=시도한것들...무시해도 됩니다++++++++++++++++++++
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from matplotlib import font_manager
# # # from statsmodels.tsa.arima.model import ARIMA
# # # import numpy as np

# # # # 한글 폰트 설정 (NanumGothic 폰트 사용 예시)
# # # font_path = "/Library/Fonts/NanumGothic.ttf"  # MacOS에서 NanumGothic 폰트 경로를 확인하고 수정
# # # font_prop = font_manager.FontProperties(fname=font_path)
# # # plt.rcParams['font.family'] = font_prop.get_name()

# # # # 데이터 불러오기
# # # df = pd.read_csv('monthly_genre_counts.csv')

# # # # 날짜 형식으로 변환
# # # df['등록월'] = pd.to_datetime(df['등록월'], format='%Y-%m')

# # # # 백번대 장르 필터링 (100, 200, ..., 900)
# # # df = df[df['분류코드'].isin([100, 200, 300, 400, 500, 600, 700, 800, 900])]

# # # # 년도와 월별로 장르별 등록도서수 합계
# # # df['년도_월'] = df['등록월'].dt.to_period('M')
# # # genre_counts = df.groupby(['년도_월', '분류코드'])['등록도서수'].sum().unstack(fill_value=0)

# # # # ARIMA 예측 함수 정의
# # # def forecast_arima(genre_data, steps=12):
# # #     # ARIMA 모델 피팅
# # #     model = ARIMA(genre_data, order=(5, 1, 0))
# # #     model_fit = model.fit()

# # #     # 예측
# # #     forecast = model_fit.forecast(steps=steps)
# # #     forecast_index = pd.date_range(start=genre_data.index[-1] + pd.Timedelta(days=1), periods=steps, freq='M')
# # #     forecast_series = pd.Series(forecast, index=forecast_index)

# # #     return forecast_series

# # # # 100번대 장르 예측
# # # genre_100_data = genre_counts[100]
# # # forecast_100 = forecast_arima(genre_100_data, steps=12)

# # # # 결과 시각화
# # # plt.figure(figsize=(12, 6))
# # # plt.plot(genre_100_data, label='실제 등록도서수', color='blue')
# # # plt.plot(forecast_100, label='예측 등록도서수', color='red', linestyle='--')
# # # plt.title('백번대 장르(100번대) 월별 등록도서수 예측')
# # # plt.xlabel('년도-월')
# # # plt.ylabel('등록도서수')
# # # plt.legend()
# # # plt.grid(True)
# # # plt.show()

# # # # 예측값 출력
# # # print(forecast_100)
# # import pandas as pd
# # import numpy as np
# # from statsmodels.tsa.arima.model import ARIMA
# # import matplotlib.pyplot as plt

# # # 데이터 로드
# # file_path = "monthly_genre_counts.csv"
# # data = pd.read_csv(file_path)

# # # 백의자리로 분류코드 변환
# # data['장르'] = (data['분류코드'] // 100) * 100

# # # 월별 등록도서수 집계
# # data['등록월'] = pd.to_datetime(data['등록월'])
# # genre_monthly_counts = data.groupby(['등록월', '장르'])['등록도서수'].sum().unstack(fill_value=0)

# # # 예측을 위한 함수 정의
# # def predict_genre_books_arima(genre_monthly_counts, periods=12):
# #     predictions = {}
# #     for genre in genre_monthly_counts.columns:
# #         # 장르별 데이터 추출
# #         genre_data = genre_monthly_counts[genre]

# #         # 시계열 모델 학습 및 예측
# #         model = ARIMA(genre_data, order=(5, 1, 0))  # (p, d, q) 값을 조정 가능
# #         fit = model.fit()

# #         # 예측
# #         future = fit.forecast(steps=periods)
# #         predictions[genre] = future

# #         # 결과 시각화
# #         plt.figure(figsize=(10, 6))
# #         plt.plot(genre_data.index, genre_data, label="Actual")
# #         plt.plot(pd.date_range(genre_data.index[-1], periods=periods + 1, freq='M')[1:], future, label="Forecast", linestyle="--")
# #         plt.title(f"Genre {genre} Forecast")
# #         plt.legend()
# #         plt.show()

# #     return pd.DataFrame(predictions)

# # # 예측 실행
# # predicted_counts = predict_genre_books_arima(genre_monthly_counts)

# # # 예측 결과 저장
# # output_file = "predicted_genre_counts_arima.csv"
# # predicted_counts.to_csv(output_file)
# # print(f"Predicted counts saved to {output_file}")
# import pandas as pd
# import numpy as np
# from pmdarima import auto_arima
# import matplotlib.pyplot as plt

# # 데이터 로드
# file_path = "monthly_genre_counts.csv"
# data = pd.read_csv(file_path)

# # 백의자리로 분류코드 변환
# data['장르'] = (data['분류코드'] // 100) * 100

# # 월별 등록도서수 집계
# data['등록월'] = pd.to_datetime(data['등록월'])
# genre_monthly_counts = data.groupby(['등록월', '장르'])['등록도서수'].sum().unstack(fill_value=0)

# # 전처리: 값이 매우 작은 경우 0으로 대체
# genre_monthly_counts = genre_monthly_counts.applymap(lambda x: max(x, 0.01))

# # 예측을 위한 함수 정의
# def predict_genre_books_arima_auto(genre_monthly_counts, periods=12):
#     predictions = {}
#     for genre in genre_monthly_counts.columns:
#         # 장르별 데이터 추출
#         genre_data = genre_monthly_counts[genre]

#         # 최적 파라미터 탐색 및 모델 학습
#         model = auto_arima(genre_data, seasonal=True, m=12, trace=True, error_action='ignore', suppress_warnings=True)
#         fit = model.fit(genre_data)

#         # 예측
#         future = fit.predict(n_periods=periods)
#         predictions[genre] = future

#         # 결과 시각화
#         plt.figure(figsize=(10, 6))
#         plt.plot(genre_data.index, genre_data, label="Actual")
#         plt.plot(pd.date_range(genre_data.index[-1], periods=periods + 1, freq='M')[1:], future, label="Forecast", linestyle="--")
#         plt.title(f"Genre {genre} Forecast")
#         plt.legend()
#         plt.show()

#     return pd.DataFrame(predictions, index=pd.date_range(start=genre_monthly_counts.index[-1], periods=periods, freq='M'))

# # 예측 실행
# predicted_counts = predict_genre_books_arima_auto(genre_monthly_counts)

# # 예측 결과 저장
# output_file = "predicted_genre_counts_arima_auto.csv"
# predicted_counts.to_csv(output_file)
# print(f"Predicted counts saved to {output_file}")

#=============================================
# import pandas as pd
# import numpy as np
# from statsmodels.tsa.arima.model import ARIMA
# import matplotlib.pyplot as plt

# # 데이터 로드
# file_path = "monthly_genre_counts.csv"
# data = pd.read_csv(file_path)

# # 백의자리로 분류코드 변환
# data['장르'] = (data['분류코드'] // 100) * 100

# # 월별 등록도서수 집계
# data['등록월'] = pd.to_datetime(data['등록월'])
# genre_monthly_counts = data.groupby(['등록월', '장르'])['등록도서수'].sum().unstack(fill_value=0)

# # 데이터 확인
# print("Monthly Genre Counts:\n", genre_monthly_counts.head())

# # 예측을 위한 함수 정의
# def predict_genre_books_arima(genre_monthly_counts, periods=12):
#     predictions = {}
#     for genre in genre_monthly_counts.columns:
#         genre_data = genre_monthly_counts[genre]

#         # 최소 데이터 길이 확인
#         if len(genre_data) < 5:
#             print(f"Not enough data for genre {genre}, skipping...")
#             continue

#         try:
#             # ARIMA 모델 학습
#             model = ARIMA(genre_data, order=(5, 1, 0))
#             fit = model.fit()

#             # 예측
#             future = fit.forecast(steps=periods)
#             predictions[genre] = future

#             # 결과 시각화
#             plt.figure(figsize=(10, 6))
#             plt.plot(genre_data.index, genre_data, label="Actual")
#             plt.plot(pd.date_range(genre_data.index[-1], periods=periods + 1, freq='M')[1:], future, label="Forecast", linestyle="--")
#             plt.title(f"Genre {genre} Forecast")
#             plt.legend()
#             plt.show()
#         except Exception as e:
#             print(f"Error with genre {genre}: {e}")
#             continue

#     # 결과를 데이터프레임으로 반환
#     prediction_df = pd.DataFrame(predictions, index=pd.date_range(start=genre_monthly_counts.index[-1], periods=periods, freq='M'))
#     return prediction_df

# # 예측 실행
# predicted_counts = predict_genre_books_arima(genre_monthly_counts)

# # 예측 결과 저장
# output_file = "predicted_genre_counts_fixed.csv"
# predicted_counts.to_csv(output_file)
# print(f"Predicted counts saved to {output_file}")
#========================================

# import pandas as pd
# import numpy as np
# from statsmodels.tsa.arima.model import ARIMA
# import matplotlib.pyplot as plt

# # 데이터 로드
# file_path = "monthly_genre_counts.csv"
# data = pd.read_csv(file_path)

# # 백의자리로 분류코드 변환
# data['장르'] = (data['분류코드'] // 100) * 100

# # 월별 등록도서수 집계
# data['등록월'] = pd.to_datetime(data['등록월'])
# genre_monthly_counts = data.groupby(['등록월', '장르'])['등록도서수'].sum().unstack(fill_value=0)

# # 데이터 확인
# print("Monthly Genre Counts:\n", genre_monthly_counts.head())

# # 예측을 위한 함수 정의
# def predict_genre_books_arima(genre_monthly_counts, periods=12):
#     predictions = {}
#     for genre in genre_monthly_counts.columns:
#         genre_data = genre_monthly_counts[genre]

#         # 최소 데이터 길이 확인
#         if len(genre_data) < 5:
#             print(f"Not enough data for genre {genre}, skipping...")
#             continue

#         try:
#             # ARIMA 모델 학습
#             model = ARIMA(genre_data, order=(5, 1, 0))
#             fit = model.fit()

#             # 예측
#             future = fit.forecast(steps=periods)
#             predictions[genre] = future

#             # 결과 시각화
#             plt.figure(figsize=(10, 6))
#             plt.plot(genre_data.index, genre_data, label="Actual")
#             plt.plot(pd.date_range(genre_data.index[-1], periods=periods + 1, freq='M')[1:], future, label="Forecast", linestyle="--")
#             plt.title(f"Genre {genre} Forecast")
#             plt.legend()
#             plt.show()
#         except Exception as e:
#             print(f"Error with genre {genre}: {e}")
#             continue

#     # 예측 결과를 데이터프레임으로 반환
#     if predictions:  # 예측 결과가 있는 경우
#         prediction_df = pd.DataFrame(predictions, index=pd.date_range(start=genre_monthly_counts.index[-1], periods=periods, freq='M'))
#     else:
#         prediction_df = pd.DataFrame(columns=genre_monthly_counts.columns, index=pd.date_range(start=genre_monthly_counts.index[-1], periods=periods, freq='M'))
#     return prediction_df

# # 예측 실행
# predicted_counts = predict_genre_books_arima(genre_monthly_counts)

# # 예측 결과 저장
# output_file = "predicted_genre_counts_fixed.csv"
# predicted_counts.to_csv(output_file)
# print(f"Predicted counts saved to {output_file}")
#=======================================================