# core/tokenizer.py
import re

def tokenize(text: str):
    """
    텍스트를 전처리하고 단어 리스트로 반환한다.
    - 소문자 변환
    - 특수문자 제거
    - 공백 기준 분리
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    return [t for t in tokens if t.strip()]
