import cv2

# 이미지 읽기
image = cv2.imread('./images/yujeong.jpg')

# 이미지를 회색조로 변환
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이미지 저장
cv2.imwrite('./images/yujeong.jpg', gray_image)

# 이미지 표시
cv2.imshow('Gray Image', gray_image)

# 아무키나 누를때까지 기다림
cv2.waitKey(0)
cv2.destroyAllWindows()
