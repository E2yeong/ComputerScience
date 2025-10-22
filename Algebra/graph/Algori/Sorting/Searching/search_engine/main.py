import os
from core.index_builder import build_index
from core.search_engine import search

def main():
    print("🔍 Mini Search Engine (Auto-Build Mode)")

    # index.json 없으면 자동 생성
    if not os.path.exists("index.json"):
        print("⚙️ Building index automatically...")
        build_index()

    while True:
        keyword = input("\nEnter keyword (or 'exit'): ").strip().lower()
        if keyword == "exit":
            print("👋 Exiting program.")
            break

        results = search(keyword)
        if results:
            print(f"✅ Found in {len(results)} file(s):")
            for file in results:
                print(f"  - {file}")
        else:
            print("❌ No results found.")

if __name__ == "__main__":
    main()