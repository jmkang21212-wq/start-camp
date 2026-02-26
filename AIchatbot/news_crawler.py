"""
Google News RSS 기반 뉴스 수집 모듈
"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict
from urllib.parse import quote


class NewsCrawler:
    """Google News에서 뉴스를 수집하는 클래스"""
    
    def __init__(self, language: str = "kor"):
        """
        Args:
            language: 뉴스 언어 (기본값: 한국어)
        """
        self.language = language
        self.base_url = f"https://news.google.com/rss"
    
    def search_news(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        키워드로 뉴스 검색
        
        Args:
            keyword: 검색 키워드
            max_results: 최대 결과 수
            
        Returns:
            뉴스 정보 리스트
        """
        try:
            # URL 인코딩 처리 (한글/영문 모두 대응)
            encoded_keyword = quote(keyword, safe='')
            
            # Google News 검색 RSS URL
            search_url = f"{self.base_url}/search?q={encoded_keyword}&hl={self.language}"
            
            # RSS 피드 파싱
            feed = feedparser.parse(search_url)
            
            news_list = []
            for entry in feed.entries[:max_results]:
                news_item = {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "source": entry.get("source", {}).get("title", "Unknown Source")
                }
                news_list.append(news_item)
            
            return news_list
            
        except Exception as e:
            print(f"뉴스 검색 중 오류 발생: {e}")
            return []
    
    def get_latest_news(self, max_results: int = 10) -> List[Dict]:
        """
        최신 뉴스 조회
        
        Args:
            max_results: 최대 결과 수
            
        Returns:
            최신 뉴스 리스트
        """
        try:
            feed = feedparser.parse(self.base_url)
            
            news_list = []
            for entry in feed.entries[:max_results]:
                news_item = {
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "source": entry.get("source", {}).get("title", "Unknown Source")
                }
                news_list.append(news_item)
            
            return news_list
            
        except Exception as e:
            print(f"최신 뉴스 조회 중 오류 발생: {e}")
            return []


if __name__ == "__main__":
    # 테스트용 코드
    crawler = NewsCrawler(language="en")
    
    # 최신 뉴스 조회
    print("=== 최신 뉴스 ===")
    latest = crawler.get_latest_news(max_results=5)
    for news in latest:
        print(f"제목: {news['title']}")
        print(f"출처: {news['source']}")
        print(f"링크: {news['link']}\n")
    
    # 키워드 검색
    print("\n=== 'AI' 관련 뉴스 ===")
    ai_news = crawler.search_news(keyword="AI", max_results=5)
    for news in ai_news:
        print(f"제목: {news['title']}")
        print(f"출처: {news['source']}")
        print(f"링크: {news['link']}\n")
