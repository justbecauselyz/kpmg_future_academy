import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 웹캠 설정
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=2,             # 최대 인식할 손의 개수
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # 성능 향상을 위해 이미지를 읽기 전용으로 변경 및 RGB 변환
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # 랜드마크 추적 수행
        results = hands.process(image)

        # 이미지를 다시 그리기 모드로 변경 및 BGR 변환
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 랜드마크 그리기
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27: # ESC 키로 종료
            break

cap.release()  # 카메라 자원 해제
cv2.destroyAllWindows()  # 앱 종료