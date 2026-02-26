"""
OpenAI API (SSAFY GMS 경유)를 사용한 챗봇 모듈
"""
from openai import OpenAI
from typing import List, Dict
import config
import os
import logging
import httpx

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AIchatbot:
    """OpenAI API를 활용한 AI 챗봇"""
    
    def __init__(self):
        """챗봇 초기화"""
        # GMS Key 가져오기
        gms_key = os.environ.get('GMS_KEY')
        
        if not gms_key:
            raise ValueError("❌ GMS_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        
        # OpenAI 클라이언트 초기화 (GMS base_url 사용)
        try:
            self.client = OpenAI(
                base_url='https://gms.ssafy.io/gmsapi/api.openai.com/v1',
                api_key=gms_key,
                timeout=30.0
            )
        except TypeError:
            # httpx 버전 호환성 문제 시 기본 설정으로 재시도
            import httpx
            self.client = OpenAI(
                base_url='https://gms.ssafy.io/gmsapi/api.openai.com/v1',
                api_key=gms_key,
                http_client=httpx.Client(timeout=30.0)
            )
        
        self.model = config.OPENAI_MODEL
        self.conversation_history: List[Dict] = []
    
    def _validate_api_key(self) -> bool:
        """API 키 유효성 검사"""
        if not os.environ.get('GMS_KEY'):
            raise ValueError("❌ GMS_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return True
    
    def chat(self, user_message: str, include_history: bool = True) -> str:
        """
        사용자 메시지에 응답
        
        Args:
            user_message: 사용자 입력
            include_history: 대화 히스토리 포함 여부
            
        Returns:
            AI 응답
        """
        logger.debug(f"[CHAT] 사용자 입력: {user_message}")
        try:
            self._validate_api_key()
            
            # 대화 히스토리 업데이트
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # OpenAI API 호출
            messages = self.conversation_history if include_history else [
                {"role": "user", "content": user_message}
            ]
            
            logger.debug(f"[CHAT] 대화 히스토리: {messages}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_completion_tokens=4096
            )
            
            ai_response = response.choices[0].message.content
            logger.info(f"[CHAT] AI 응답: {ai_response}")
            
            # 대화 히스토리에 추가
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except ValueError as ve:
            logger.error(f"[CHAT] 설정 오류: {str(ve)}")
            return f"설정 오류: {str(ve)}"
        except Exception as e:
            logger.error(f"[CHAT] API 요청 실패: {str(e)}")
            return f"API 요청 실패: {str(e)}"
    
    def analyze_news(self, news_title: str, news_summary: str) -> str:
        """
        뉴스 분석
        
        Args:
            news_title: 뉴스 제목
            news_summary: 뉴스 요약
            
        Returns:
            뉴스 분석 결과
        """
        analysis_prompt = f"""
다음 뉴스를 분석하고 핵심 포인트를 요약해주세요:

제목: {news_title}
요약: {news_summary}

요청사항:
1. 뉴스의 주요 내용을 한 문장으로 요약
2. 핵심 영향력 분석
3. 추가 정보나 의견
"""
        return self.chat(analysis_prompt, include_history=False)
    
    def reset_conversation(self):
        """대화 히스토리 초기화"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """대화 히스토리 반환"""
        return self.conversation_history
    
    def should_search_news(self, user_message: str) -> bool:
        """
        사용자 메시지가 뉴스 검색 요청인지 판단
        
        Args:
            user_message: 사용자 입력
            
        Returns:
            뉴스 검색 여부
        """
        logger.debug(f"[NEWS_CHECK] 뉴스 검색 여부 확인: {user_message}")
        try:
            detection_prompt = f"""
사용자의 다음 메시지가 뉴스 검색 요청인지 판단하세요.
뉴스 검색 요청이면 "YES"만 응답하고, 일반 대화면 "NO"만 응답하세요.

뉴스 검색 요청의 예:
- "AI 관련 뉴스 찾아줘"
- "최근 기술 뉴스 알려줘"
- "비트코인 뉴스 있어?"
- "스포츠 뉴스 보여줄래?"
- "인공지능 뉴스 10개 찾아"
- "한국 경제 뉴스 뭐 있어?"

일반 대화의 예:
- "안녕하세요"
- "어떻게 지내세요?"
- "파이썬이 뭔가요?"

사용자 메시지: {user_message}

응답 (YES 또는 NO):
"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": detection_prompt}],
                max_completion_tokens=4096
            )
            
            ai_response = response.choices[0].message.content.strip().upper()
            logger.debug(f"[NEWS_CHECK] 상세 응답: '{ai_response}'")
            is_news = "YES" in ai_response
            logger.info(f"[NEWS_CHECK] 뉴스 검색 판단: {is_news} (응답: {ai_response})")
            
            return is_news
            
        except Exception as e:
            logger.error(f"[NEWS_CHECK] 뉴스 검색 판단 실패: {str(e)}")
            # API 오류 시 기본값으로 NO 반환
            return False
    
    def extract_news_keyword(self, user_message: str) -> str:
        """
        사용자 메시지에서 뉴스 검색 키워드 추출
        
        Args:
            user_message: 사용자 입력
            
        Returns:
            추출된 키워드
        """
        logger.debug(f"[KEYWORD] 키워드 추출 시작: {user_message}")
        try:
            extraction_prompt = f"""
사용자의 메시지에서 뉴스 검색 키워드를 추출하세요.
** 중요: 가능하면 한국어로 추출하세요. **
키워드만 한 개 반환하세요.

예시:
- "AI 뉴스 찾아줘" → AI
- "비트코인 최신 뉴스" → 비트코인
- "스포츠 뉴스 보여줄래?" → 스포츠
- "로봇 관련 뉴스 있어?" → 로봇
- "파이썬으로 뭐할 수 있어?" → (뉴스 검색 불필요)

사용자 메시지: {user_message}

키워드:
"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": extraction_prompt}],
                max_completion_tokens=4096
            )
            keyword = response.choices[0].message.content.strip()
            logger.debug(f"[KEYWORD] 상세 응답: '{keyword}'")
            logger.info(f"[KEYWORD] 추출된 키워드: {keyword}")
            
            return keyword if keyword and len(keyword) < 50 else ""
            
        except Exception as e:
            logger.error(f"[KEYWORD] 키워드 추출 실패: {str(e)}")
            return ""


if __name__ == "__main__":
    # 테스트용 코드
    try:
        logger.info("[INIT] 챗봇 테스트 시작...")
        bot = AIchatbot()
        logger.info("[INIT] 챗봇 초기화 완료")
        
        # 간단한 대화 테스트
        response = bot.chat("안녕하세요!")
        print(f"봇 응답: {response}")
        logger.info("[INIT] 테스트 완료")
        
    except ValueError as e:
        logger.error(f"[INIT] 설정 오류: {e}")
        print(f"설정 오류: {e}")