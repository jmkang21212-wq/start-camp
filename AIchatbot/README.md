# 🤖 AI 기사 검색 통합 챗봇

Google News와 GMS (GPT 5 - nano)를 활용한 뉴스 검색 및 분석 챗봇입니다.

## 📋 필수 개발 환경

- Python 3.8+
- Python 가상환경
- Streamlit
- GMS (GPT 5 - nano)
- Google News (RSS 기반)

## 🚀 설치 및 실행

### 1. 가상환경 생성
```bash
python -m venv venv
```

### 2. 가상환경 활성화
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일에서 다음을 수정하세요:
```
GMS_API_KEY=your_actual_api_key_here
```

### 5. 애플리케이션 실행
```bash
streamlit run main.py
```

## 📁 프로젝트 구조

```
AIchatbot/
├── main.py              # Streamlit 메인 애플리케이션
├── news_crawler.py      # Google News RSS 수집 모듈
├── chatbot.py           # GMS API 챗봇 모듈
├── config.py            # 프로젝트 설정
├── .env                 # 환경 변수 (API Key 등)
├── .gitignore           # Git 무시 파일
├── requirements.txt     # 필수 패키지 목록
└── README.md            # 프로젝트 문서
```

## 🔐 API Key 관리

⚠️ **주의:** 절대로 코드에 API Key를 직접 작성하지 마세요.

1. `.env` 파일에 API Key를 저장합니다.
2. `config.py`에서 `python-dotenv`로 로드합니다.
3. `.gitignore`에 `.env`를 추가하여 버전 관리에서 제외합니다.

## 🎯 주요 기능

- 📰 **뉴스 검색**: Google News RSS를 통한 실시간 뉴스 검색
- 🔍 **키워드 검색**: 특정 키워드로 관련 뉴스 검색
- 📊 **뉴스 분석**: GMS AI를 활용한 뉴스 분석 및 요약
- 💬 **AI 챗봇**: 자유로운 대화 및 질의응답

## 📝 사용법

1. **뉴스 검색**
   - "최신 뉴스" 또는 "키워드 검색" 선택
   - 결과에서 뉴스 확인

2. **뉴스 분석**
   - 검색 결과에서 "📊 분석" 버튼 클릭
   - AI가 뉴스를 분석하고 요약

3. **챗봇 대화**
   - 자유로운 질문과 대화
   - 대화 초기화 가능

## 🔧 개발 단계

- [x] 1단계: 프로젝트 초기화
- [ ] 2단계: Python 가상환경 설정
- [ ] 3단계: 환경 변수 관리
- [ ] 4단계: Google News 모듈 완성
- [ ] 5단계: GMS API 통합
- [ ] 6단계: Streamlit UI 구성
- [ ] 7단계: 테스트 및 최적화

## 📞 트러블슈팅

### API Key 오류
```
❌ GMS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.
```
**해결:** `.env` 파일에서 `GMS_API_KEY`를 설정하세요.

### 뉴스 검색 실패
- 인터넷 연결 확인
- RSS 피드 URL 확인
- feedparser 라이브러리 설치 확인

## 📄 라이선스

MIT License

## 👨‍💻 개발자

강재민

---

**다음 단계:** 2단계 Python 가상환경 설정으로 진행하세요!
