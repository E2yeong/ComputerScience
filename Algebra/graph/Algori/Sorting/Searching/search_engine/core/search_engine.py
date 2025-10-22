# core/search_engine.py
import json
import os
from core.tokenizer import tokenize

_INDEX_CACHE = None

def load_index(index_file='index.json'):
    global _INDEX_CACHE
    if _INDEX_CACHE is None:
        with open(index_file, 'r', encoding='utf-8') as f:
            _INDEX_CACHE = json.load(f)
    return _INDEX_CACHE

def search_term(term: str, index: dict):
    term = term.lower()
    return set(index.get(term, []))

def search_all(terms, index: dict):
    """AND 검색: 모든 키워드를 포함하는 문서 교집합"""
    if not terms:
        return set()
    result = None
    for t in terms:
        docs = search_term(t, index)
        result = docs if result is None else (result & docs)
        if not result:
            break
    return result or set()

def search_any(terms, index: dict):
    """OR 검색: 키워드 중 하나라도 포함"""
    result = set()
    for t in terms:
        result |= search_term(t, index)
    return result

def read_file_text(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def make_snippet(text: str, terms, max_len=160):
    """간단 스니펫: 첫 매치 주변을 잘라 보여주고 매칭어 대문자로 표시"""
    low = text.lower()
    pos = -1
    hit = None
    for t in terms:
        p = low.find(t.lower())
        if p != -1 and (pos == -1 or p < pos):
            pos = p
            hit = t
    if pos == -1:
        snippet = text[:max_len].strip()
    else:
        start = max(0, pos - max_len // 4)
        end = min(len(text), pos + max_len // 4 * 3)
        snippet = text[start:end].strip()

    # 하이라이트(간단): 매칭어를 대문자 처리
    if hit:
        snippet = snippet.replace(hit, hit.upper()).replace(hit.capitalize(), hit.upper())
    return snippet.replace('\n', ' ')

def rank_results(files, terms, data_folder='data'):
    """간단 랭킹: 총 매치 카운트 / 문서 길이 보정"""
    scored = []
    for fn in files:
        path = os.path.join(data_folder, fn)
        try:
            txt = read_file_text(path)
        except Exception:
            continue
        low = txt.lower()
        term_hits = sum(low.count(t.lower()) for t in terms)
        length = max(50, len(txt))
        score = term_hits / length
        snippet = make_snippet(txt, terms)
        scored.append({
            "file": fn,
            "score": round(score, 6),
            "hits": term_hits,
            "snippet": snippet
        })
    scored.sort(key=lambda x: (x["score"], x["hits"]), reverse=True)
    return scored

def search_query(query: str, index_file='index.json', data_folder='data'):
    """
    쿼리 문법:
      - 기본: AND (예: "computer science")
      - OR 사용: "computer OR science"
    """
    index = load_index(index_file)
    raw = query.strip()
    if not raw:
        return []

    # 매우 심플한 파서: OR 기준 분리 → 없으면 AND
    if " OR " in raw.upper():
        parts = [p.strip() for p in raw.split("OR")]
        terms = []
        for p in parts:
            terms.extend(tokenize(p))
        files = search_any(terms, index)
    else:
        terms = tokenize(raw)
        files = search_all(terms, index)

    return rank_results(files, terms, data_folder=data_folder)

def trace_search(query, index_file='index.json'):
    import json, os
    if not query or not os.path.exists(index_file):
        return []
    with open(index_file, 'r', encoding='utf-8') as f:
        index = json.load(f)
    steps = []
    for word in index.keys():
        steps.append({
            "word": word,
            "match": word.lower() == query.lower()
        })
    return steps
