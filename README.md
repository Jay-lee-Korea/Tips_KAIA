# TIPS 운영사 대시보드 (Streamlit)

## 📌 프로젝트 개요
이 프로젝트는 TIPS 운영사 데이터를 분석하고 시각화하는 Streamlit 대시보드입니다.

## 🛠️ 실행 방법 (로컬 실행)
아래 명령어를 실행하여 필요한 패키지를 설치한 후, Streamlit 앱을 실행할 수 있습니다.

```bash
# 가상환경 생성 (선택 사항)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# 필수 라이브러리 설치
pip install -r requirements.txt
pip install koreanize-matplotlib

# Streamlit 실행
streamlit run app.py

