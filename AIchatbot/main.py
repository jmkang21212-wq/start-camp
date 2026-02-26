"""
Streamlit 메인 애플리케이션
ChatGPT/Gemini 스타일의 통합 뉴스 검색 챗봇
"""
import streamlit as st
from news_crawler import NewsCrawler
from chatbot import AIchatbot
import config
import logging
from datetime import datetime

# 로깅 설정
logger = logging.getLogger(__name__)


def initialize_session_state():
    """Streamlit 세션 상태 초기화"""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = AIchatbot()
    
    if "crawler" not in st.session_state:
        st.session_state.crawler = NewsCrawler(language="kor")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = {}
    
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None


def get_related_topics(keyword):
    """키워드와 관련된 주제 3개 생성 (간단한 방식)"""
    try:
        # 간단한 주제 생성 (AI 호출 없음)
        topics_dict = {
            "ai": ["인공지능 기술", "머신러닝", "딥러닝"],
            "인공지능": ["AI 기술", "머신러닝", "자연어처리"],
            "기술": ["소프트웨어", "하드웨어", "클라우드"],
            "뉴스": ["속보", "시사", "시황"],
            "금융": ["주식", "코인", "투자"],
            "정치": ["정부", "의회", "선거"],
            "스포츠": ["축구", "야구", "농구"],
            "엔터": ["영화", "드라마", "음악"],
            "게임": ["온라인게임", "모바일게임", "e스포츠"],
        }
        
        # 키워드 소문자화
        keyword_lower = keyword.lower()
        
        # 키워드와 일치하는 주제가 있으면 반환
        for key in topics_dict.keys():
            if key in keyword_lower:
                return topics_dict[key]
        
        # 매칭되는 주제가 없으면 주제 추가 생성
        return [f"{keyword} 뉴스", f"{keyword} 관련", f"{keyword} 동향"]
    except Exception as e:
        logger.error(f"[TOPIC] 주제 생성 실패: {str(e)}")
        return [keyword, f"{keyword} 관련", f"{keyword} 뉴스"]


def display_news_by_topic(keyword):
    """주제별 뉴스를 귀여운 표 디자인으로 표시"""
    logger.info(f"[NEWS] '{keyword}' 관련 주제별 뉴스 검색 시작")
    
    # 메인 제목
    st.markdown(f"## 📰 '{keyword}' 관련 뉴스")
    
    # 관련 주제 3개 생성
    topics = get_related_topics(keyword)
    
    # 각 주제별로 뉴스 검색
    for topic in topics:
        st.subheader(f"🔷 {topic}")
        
        news_list = st.session_state.crawler.search_news(topic, max_results=5)
        
        if news_list:
            # 마크다운 테이블 생성
            table_data = "| # | 📌 제목 | � 출처 | 📅 날짜 | 🔗 |\n"
            table_data += "|:---:|---|---|---|---|\n"
            
            for idx, news in enumerate(news_list, 1):
                # 테이블 행 추가
                table_data += f"| {idx} | {news['title'][:50]} | {news['source'][:15]} | {news['published'][:10]} | "
                table_data += f'<a href="{news["link"]}" target="_blank" style="text-decoration: none;"><button style="background: #667eea; color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer; font-size: 12px;">읽기</button></a> |\n'
            
            st.markdown(table_data, unsafe_allow_html=True)
        else:
            st.info(f"'{topic}' 관련 뉴스가 없습니다.")
        
        st.divider()  # 주제 간 구분선


def main():
    """메인 애플리케이션"""
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 사이드바: 대화 히스토리 관리 (ChatGPT 스타일)
    with st.sidebar:
        # 새 대화 시작 버튼 (미니멀 디자인)
        st.markdown("""
        <style>
        .new-chat-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 16px;
            background: #f0f0f0;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
            text-align: center;
            color: #333;
            text-decoration: none;
        }
        .new-chat-btn:hover {
            background: #e8e8e8;
            border-color: #d0d0d0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("➕ 새 대화", use_container_width=True, key="new_chat"):
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            if st.session_state.messages:  # 현재 대화가 있으면 저장
                st.session_state.conversation_history[session_id] = st.session_state.messages
            st.session_state.current_session_id = None
            st.session_state.messages = []
            st.session_state.chatbot.reset_conversation()
            st.rerun()
        
        # 저장된 대화 목록
        if st.session_state.conversation_history:
            st.markdown("**이전 대화**")
            st.markdown("")  # 간격
            
            for session_id in reversed(sorted(st.session_state.conversation_history.keys())):
                session_messages = st.session_state.conversation_history[session_id]
                
                if session_messages:
                    # 첫 사용자 메시지를 제목으로
                    user_messages = [m for m in session_messages if m["role"] == "user"]
                    if user_messages:
                        preview = user_messages[0].get("content", "대화")[:20]
                        date_time = session_id[:4] + "-" + session_id[4:6] + "-" + session_id[6:8] + " " + session_id[9:11] + ":" + session_id[11:13]
                        
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            if st.button(f"💬 {preview}...", use_container_width=True, key=f"session_{session_id}"):
                                st.session_state.current_session_id = session_id
                                st.session_state.messages = session_messages
                                st.rerun()
                        with col2:
                            if st.button("🗑️", key=f"delete_{session_id}"):
                                del st.session_state.conversation_history[session_id]
                                st.rerun()
        else:
            st.markdown("")
            st.markdown("---")
            st.markdown('<div style="text-align: center; color: #999; font-size: 12px; margin-top: 20px;">새 대화를 시작하세요</div>', unsafe_allow_html=True)
    
    # 메인 영역
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"🤖 {config.APP_TITLE}")
    
    st.markdown(f"*{config.APP_DESCRIPTION}*")
    st.divider()
    
    # 대화 히스토리 표시
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # 뉴스 검색 결과인 경우
                if message.get("is_news") and message.get("keyword"):
                    display_news_by_topic(message["keyword"])
                    st.markdown("---")
                    st.markdown("### 🎯 AI 뉴스 분석")
                    # AI 분석 부분만 표시
                    analysis_text = message["content"].split("\n\n", 1)[1] if "\n\n" in message["content"] else message["content"]
                    st.markdown(analysis_text)
                else:
                    st.markdown(message["content"])
    
    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요... (예: 'AI 뉴스 찾아줘' 또는 '안녕하세요')")
    
    if user_input:
        # 사용자 메시지 저장
        logger.debug(f"[USER_INPUT] 사용자 입력: {user_input}")
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 현재 세션에도 저장
        if st.session_state.current_session_id:
            st.session_state.conversation_history[st.session_state.current_session_id] = st.session_state.messages
        
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # AI 응답 생성을 위한 컨테이너
        response_container = st.container()
        
        with st.spinner("처리 중입니다..."):
            # 1. 뉴스 검색 여부 판단
            is_news_search = st.session_state.chatbot.should_search_news(user_input)
            
            if is_news_search:
                # 2. 키워드 추출
                keyword = st.session_state.chatbot.extract_news_keyword(user_input)
                
                if keyword:
                    # 3. 뉴스 검색
                    news_list = st.session_state.crawler.search_news(keyword, max_results=10)
                    
                    if news_list:
                        # AI 응답 시작 (직접 표시)
                        with st.chat_message("assistant"):
                            # 뉴스 테이블 표시
                            display_news_by_topic(keyword)
                            
                            # AI 분석 표시
                            st.markdown("---")
                            st.markdown("### 🎯 AI 뉴스 분석")
                            
                            # 뉴스 내용을 텍스트로 변환
                            news_content = "\n".join([
                                f"- {news['title']}: {news.get('summary', '')[:100]}"
                                for news in news_list[:5]
                            ])
                            
                            # AI에게 뉴스 분석 요청
                            analysis_prompt = f"""
사용자가 '{keyword}'에 대한 뉴스를 요청했습니다.

검색된 뉴스 요약:
{news_content}

위 뉴스들을 바탕으로 '{keyword}'의 최근 동향을 한국어로 설명해주세요.

응답 형식:
1. 🔥 **핵심 요약**: 한 문장으로 간단히
2. 💡 **주요 이슈 3가지**: 각각을 정렬 리스트로, 이모지 활용
3. 📈 **영향력 분석**: 긍정적/부정적 영향
4. 🔮 **앞으로의 전망**: 3~5문장

모든 텍스트에 이모지와 **볼드체**를 적절히 활용해서 재미있고 흥미롭게 작성해주세요.
"""
                            
                            ai_analysis = st.session_state.chatbot.chat(analysis_prompt, include_history=False)
                            st.markdown(ai_analysis)
                        
                        full_response = f"'{keyword}' 관련 뉴스 10개를 찾았습니다.\n\n{ai_analysis}"
                        
                        # 뉴스 메타데이터와 함께 메시지 저장
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": full_response,
                            "is_news": True,
                            "keyword": keyword
                        })
                    else:
                        error_msg = f"죄송합니다. '{keyword}' 관련 뉴스를 찾을 수 없습니다."
                        with st.chat_message("assistant"):
                            st.markdown(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    error_msg = "죄송합니다. 검색 키워드를 추출할 수 없습니다. 다시 시도해주세요."
                    with st.chat_message("assistant"):
                        st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            else:
                # 일반 대화
                response = st.session_state.chatbot.chat(user_input)
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 현재 세션에 저장
        if st.session_state.current_session_id:
            st.session_state.conversation_history[st.session_state.current_session_id] = st.session_state.messages


if __name__ == "__main__":
    main()
