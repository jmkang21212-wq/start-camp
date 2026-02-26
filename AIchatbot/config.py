"""
프로젝트 설정 파일
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 설정 (SSAFY GMS 경유)
GMS_KEY = os.getenv("GMS_KEY")
OPENAI_MODEL = "gpt-5-nano"
OPENAI_BASE_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

# Google News 설정
GOOGLE_NEWS_LANG = os.getenv("GOOGLE_NEWS_LANG", "en")
GOOGLE_NEWS_RSS_URL = f"https://news.google.com/rss?hl={GOOGLE_NEWS_LANG}"

# 애플리케이션 설정
APP_TITLE = "AI 기사 검색 통합 챗봇"
APP_DESCRIPTION = "Google News와 GMS를 활용한 뉴스 검색 및 분석 챗봇"
