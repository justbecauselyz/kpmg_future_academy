import random
import time
import pymysql
import datetime
from dotenv import load_dotenv
import os
from pygame import mixer
mixer.init()
load_dotenv(override=True)

# MySQL 설정
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
USER = os.getenv("USER")
PASSWD = os.getenv("PASSWD")
DB1 = os.getenv("DB1") #DB1 = wordgame_db
DB2 = os.getenv("DB2") #DB2 = os.getenv("DB2")

def wordLoad():
    words = []
    try:
        with open('./data/word.txt', 'r') as f:
            for word in f:
                words.append(word.strip())
    except FileNotFoundError:
        print("word.txt 파일이 없습니다.")
        exit()
    return words

def getTime(start, end):
    exe_time = end - start
    exe_time = format(exe_time, ".3f")
    return exe_time

def get_nickname():
    """게임 시작 전 닉네임 입력"""
    print("\n" + "=" * 50)
    while True:
        nickname = input("닉네임을 입력하세요 (2-10자): ").strip()
        if 2 <= len(nickname) <= 10:
            print(f"환영합니다, {nickname}님! 🎮")
            return nickname
        else:
            print("❌ 닉네임은 2-10자 사이로 입력해주세요.")

def game_run(words, nickname):
    print("\n" + "=" * 50)
    input(f"{nickname}님, 준비되셨나요? Press Enter Key!")
    print("=" * 50)
    
    game_cnt = 1
    corr_cnt = 0
    total_score = 0
    base_score_per_question = 10

    start = time.time()
    while game_cnt <= 5:
        random.shuffle(words)
        que_word = random.choice(words)

        print()
        print("=" * 50)
        print(f"*Question # {game_cnt}")
        print(f"플레이어: {nickname} | 현재 점수: {total_score}점 | 정답 수: {corr_cnt}")
        print("=" * 50)
        print(que_word)

        input_word = input()
        print()

        if str(que_word).strip() == str(input_word).strip():
            mixer.music.load('./assets/good.wav')
            mixer.music.play()
            print("✅ Pass!")
            corr_cnt += 1
        else:
            mixer.music.load('./assets/bad.wav')
            mixer.music.play()
            print("❌ Wrong!")

        game_cnt += 1
        end = time.time()

    exe_time_float = float(getTime(start, end))

    is_perfect = (corr_cnt == 5)
    if is_perfect:
        print("\n" + "=" * 50)
        print("🎊🎊🎊 PERFECT SCORE! 🎊🎊🎊")
        print("💎 만점 보너스: 점수 2배 적용! 💎")
        print(f"💰 {total_score}점 → {total_score + 10}점")
        print("=" * 50)
        total_score = total_score + 10

    ttime_bonus_earned = False
    if exe_time_float <= 50.0:
        time_bonus = 300
        print("\n" + "=" * 50)
        print("⚡⚡⚡ TIME BONUS! ⚡⚡⚡")
        print(f"⏱️ {exe_time_float}초 - 50초 이하 완료!")
        print(f"💰 시간 보너스 +{time_bonus}점 획득!")
        print("=" * 50)
        total_score += time_bonus
        time_bonus_earned = True

    return corr_cnt, getTime(start, end)

def inputDB(corr_cnt, exe_time):
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB1, charset='utf8')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_records1(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nickname VARCHAR(50),
                corr_cnt INT,
                record VARCHAR(255),
                total_score INT,
                is_perfect BOOLEAN,
                time_bonus BOOLEAN,
                regdate DATETIME
            )
        ''')

        cursor.execute(
            "INSERT INTO game_records1(corr_cnt, record, regdate) VALUES (%s, %s, %s)",
            (corr_cnt, exe_time, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )

        conn.commit()
    except pymysql.MySQLError as err:
        print(f"DB Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.open:
            conn.close()

def getDB():
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB1, charset='utf8')
        cursor = conn.cursor()

        print("\n" + "=" * 95)
        print("🏆 TOP 10 랭킹 (점수순) 🏆")
        print("=" * 95)
        print("순위\t닉네임\t\t점수\t정답수\t만점\t시간보너스\t시간\t\t게임일시")
        print("-" * 95)
        
        cursor.execute("""
            SELECT * FROM game_records1 
            ORDER BY total_score DESC, record ASC 
            LIMIT 10
        """)
        rows = cursor.fetchall()

        for rank, row in enumerate(rows, 1):
            regdate = row[7].strftime('%Y-%m-%d %H:%M:%S')
            perfect_mark = "💎" if row[5] else "-"
            time_bonus_mark = "⚡" if row[6] else "-"
            nickname = row[1][:10]  # 닉네임 최대 10자
            print(f"{rank}\t{nickname}\t\t{row[4]}\t{row[2]}\t{perfect_mark}\t{time_bonus_mark}\t\t{row[3]}\t{regdate}")

    except pymysql.MySQLError as err:  # ⭐ 이 부분이 빠졌을 가능성
        print(f"DB Error: {err}")
    finally:  # ⭐ 이 부분도 빠졌을 가능성
        if cursor:
            cursor.close()
        if conn and conn.open:
            conn.close()

def get_player_stats(nickname):
    """특정 플레이어의 통계 조회"""
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB1, charset='utf8')
        cursor = conn.cursor()

        # 해당 닉네임의 게임 기록 조회
        cursor.execute("""
            SELECT COUNT(*) as game_count, 
                   MAX(total_score) as best_score,
                   AVG(total_score) as avg_score,
                   SUM(CASE WHEN is_perfect = TRUE THEN 1 ELSE 0 END) as perfect_count
            FROM game_records1 
            WHERE nickname = %s
        """, (nickname,))
        
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            print("\n" + "=" * 50)
            print(f"📊 {nickname}님의 통계")
            print("=" * 50)
            print(f"총 게임 수: {result[0]}회")
            print(f"최고 점수: {result[1]}점")
            print(f"평균 점수: {int(result[2])}점")
            print(f"만점 달성: {result[3]}회")
            print("=" * 50)

    except pymysql.MySQLError as err:
        print(f"DB Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.open:
            conn.close()

if __name__ == '__main__':
    print("=" * 50)
    print("🎮 단어 타이핑 게임 - 만점 & 시간 보너스 🎮")
    print("=" * 50)
    print("📌 규칙:")
    print("- 정답 1개당: 100점")
    print("- 🌟 만점(5/5): 최종 점수 2배! 🌟")
    print("- ⏱️ 50초 이하 완료: +300점! ⏱️")
    print("=" * 50)

    nickname = get_nickname()
    get_player_stats(nickname)
    words = wordLoad()
    corr_cnt, exe_time, total_score, is_perfect, time_bonus_earned = game_run(words, nickname)

    inputDB(nickname, corr_cnt, exe_time, total_score, is_perfect, time_bonus_earned)
    
    print("\n" + "=" * 50)
    print(f"🎯 {nickname}님의 게임 결과")
    print("=" * 50)
    
    if is_perfect:
        print("🎊 결과: 완벽한 만점! PERFECT!")
    elif corr_cnt >= 3:
        print("✅ 결과: 합격")
    else:
        print("❌ 결과: 불합격")
    
    print(f"총 점수: {total_score}점")
    print(f"정답 개수: {corr_cnt}/5")
    print(f"만점 보너스: {'적용 💎' if is_perfect else '미적용'}")
    print(f"시간 보너스: {'적용 ⚡' if time_bonus_earned else '미적용'}")
    print(f"게임 시간: {exe_time}초")
    print("=" * 50)
    
    getDB()
    print("=" * 95)