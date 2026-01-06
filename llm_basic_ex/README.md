# llm_basic_ex
생성형 AI API 활용 실습

# 가상환경 목록 확인
```
conda env list
```

# eda_env 가상환경 활성화
```
conda activate eda_env
```

# jupyter lab 실행: 현재 디렉토리를 base 폴더로 실행
```
jupyter lab
```

# 현재 디렉토리를 base 폴더로 해서 vs-code 실행
```
code .
```

# jupyter lab에 가상환경 연동하기
- Jupyter 노트북에서 파이썬 코드를 실행할 수 있는 파이썬 커널
```
pip install ipykernel
```
- jupyter lab에 가상환경(llm_env) 등록하기
```
python -m ipykernel install --user --name llm_env
```

# 새로운 가상환경 만들기
```
conda create -n llm_env python=3.10
```

# 가상환경 활성화
```
conda activate llm_env
```

# OpenAI GPT 모델 API 사용방법 실습
## 라이브러리 설치
```
pip install openai
```
## OpenAI 토큰 계산
```
pip install tiktoken
```

# google LLM 모델 API 사용방법 실습
```
pip install google-genai

```

# Hugging Face API 사용방법 실습
```
pip install -U transformers datasets evaluate accelerate timm
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install matplotlib
pip install diffusers
pip install huggingface_hub[all]
```


# 문제해결
## 오디오 파일 생성 문제해결
```
Windows에서 FFmpeg 설치
1. Chocolatey 설치  
- Chcolatey가 설치되어 있지 않다면 다음 단계를 따라 설치
    1) 관리자 권한으로 PowerShell 열기
    2) https://chocolatey.org/install 에서 설치 코드 복사 후 설치
    3) Chocolatey 설치가 완료되면, 다음 명령어로 FFmpeg 설치
        - choco install ffmpeg
    4) vs-code, 터미널 모두 닫았다가 다시 시작
```
## docx 파일 생성 문제해결
```
pip install python-docx
```