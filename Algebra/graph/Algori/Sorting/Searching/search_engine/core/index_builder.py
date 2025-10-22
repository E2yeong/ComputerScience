# core/index_builder.py
import os
import json
from core.tokenizer import tokenize

def build_index(data_folder='data', output_file='index.json'):
    """
    data/ 폴더의 모든 텍스트 파일을 읽고
    {단어: [파일목록]} 형태의 인덱스를 생성한다.
    """
    index = {}

    for filename in os.listdir(data_folder):
        if not filename.endswith('.txt'):
            continue
        path = os.path.join(data_folder, filename)

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            words = set(tokenize(text))  # 중복 제거
            for word in words:
                index.setdefault(word, []).append(filename)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Index built successfully. ({len(index)} unique words)")
