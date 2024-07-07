def search_bible(book, chapter_verse):
    try:
        with open('創世記.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(f"{book} {chapter_verse}"):
                    return line
    except Exception as e:
        print(f"Error: {e}")
    return "該当する章節が見つかりません。"

book = "創世記"  # 入力された巻
chapter_verse = "1:1"  # 入力された章節
result = search_bible(book, chapter_verse)
print(result)
