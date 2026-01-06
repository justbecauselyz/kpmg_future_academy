import datetime
import os
import csv

def save_data(data_keyword, head, movie_lists):
    # 현재 날짜/시간 가져오기
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H")

    # 폴더/파일명 설정
    folder = f"{data_keyword}_data"
    filename = f"{data_keyword}_{timestamp}.csv"
    # "movie_datas/2025-11-21-12" 형태
    filepath = os.path.join(folder, filename)

    # 폴더 자동 생성
    os.makedirs(folder, exist_ok=True)

    # CSV 파일로 저장
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 영화제목 | 개봉일 | 예매율 | 예매매출액 | 관객수
        # 1차원 리스트 저장
        writer.writerow(head)
        # 2차원 list로 만들어서 저장(수집한 데이터)
        writer.writerows(movie_lists)
    print("CSV 저장완료:", filepath)