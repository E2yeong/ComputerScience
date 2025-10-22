# web/app.py
import os
from flask import Flask, render_template, request
from core.search_engine import search_query
from core.index_builder import build_index
from core.search_engine import trace_search

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INDEX_FILE = os.path.join(BASE_DIR, 'index.json')
DATA_DIR = os.path.join(BASE_DIR, 'data')

app = Flask(__name__, template_folder='templates', static_folder='static')

# 서버 시작 시 인덱스 없으면 자동 생성
if not os.path.exists(INDEX_FILE):
    print("⚙️ Building index automatically...")
    build_index(data_folder=DATA_DIR, output_file=INDEX_FILE)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/visualize")
def visualize_page():
    from core.search_engine import trace_search
    q = request.args.get("q", "")
    steps = trace_search(q) if q else []  # 검색어가 없으면 빈 리스트
    print("🔍 Visualization query:", q)
    print("🔹 Steps length:", len(steps))
    return render_template("visualize.html", query=q, steps=steps)

@app.route("/search")
def search_page():
    q = request.args.get("q", "").strip()
    results = []
    if q:
        results = search_query(q, index_file=INDEX_FILE, data_folder=DATA_DIR)
    return render_template("results.html", query=q, results=results)

if __name__ == "__main__":
    app.run(debug=True)
