import streamlit as st
import numpy as np
import pickle
import os

# 현재 파일의 디렉토리 경로 설정
# ./ : 현재 디렉토리
base_path = os.path.dirname(__file__)

# 모델 로드 함수
@st.cache_resource  # 자원 캐싱 기능 
def load_model():
    model_path = os.path.join(base_path, "models", "iris_model_rfc.pkl")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

# 클래스별 이미지 경로 설정
# 윈도우에서만 가능한 코드
# def get_image_path(prediction):
#     if prediction == 0:
#         return "static/setosa.jpg"  # setosa 이미지 경로
#     elif prediction == 1:
#         return "static/versicolor.jpg"  # versicolor 이미지 경로
#     else:
#         return "static/virginica.png"   # virginica 이미지 

# 모든 os에서 가능한 코드
def get_image_path(prediction):
    if prediction == 0:
        return os.path.join(base_path, "static", "setosa.jpg")  # setosa 이미지 경로
    elif prediction == 1:
        return os.path.join(base_path, "static", "versicolor.jpg")  # versicolor 이미지 경로
    else:
        return os.path.join(base_path, "static", "virginica.png")  # virginica 이미지 

# 메인 실행 코드
# Streamlit 앱 구성
st.title("Iris 품종 예측")
st.write("꽃받침 길이, 너비, 꽃잎 길이, 너비를 입력하여 품종을 예측해보세요.")

# 이미지 로딩
img_path = os.path.join(base_path, "static", "flower1.jpg")

# 사용자 입력 받기
sepal_length = st.number_input("꽃받침 길이", 
            min_value=0.0, max_value=10.0, value=5.0)
sepal_width = st.number_input("꽃받침 너비", 
            min_value=0.0, max_value=10.0, value=3.0)
petal_length = st.number_input("꽃잎 길이", 
            min_value=0.0, max_value=10.0, value=4.0)
petal_width = st.number_input("꽃잎 너비", 
            min_value=0.0, max_value=10.0, value=1.0)


# 예측하기 버튼
if st.button("예측하기"):
    # 예측 버튼을 눌렀을 때
    btn_clicked = True
else:
    # 누르지 않았을 때
    btn_clicked = False

st.markdown("---")
st.subheader("예측 결과 출력")
if btn_clicked==True:
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    # 예측 수행
    prediction = model.predict(input_data)
    # 예측값을 터미널에 출력함(디버그용)
    print(prediction)
    predicted_class = prediction[0]
    # 예측된 클래스 이름
    class_name = ['Setosa', 'Versicolor', 'Virginica'][predicted_class]
    # 예측된 품종에 해당하는 이미지 출력
    # image_path = get_image_path(predicted_class)
    # st.image(image_path, caption=class_name)

    # 이미지 크기 고정
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.subheader(f"예측된 품종: {class_name}")
        # 예측된 품종에 해당하는 이미지 출력
        image_path = get_image_path(predicted_class)
        st.image(image_path, use_container_width=True, caption=class_name)


else:
    st.warning("값을 입력하고, 예측하기 버튼을 눌러 결과를 확인하세요.")