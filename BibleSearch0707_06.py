import tkinter as tk
from tkinter import ttk
from tkinter import font

books = ["創世記", "出エジプト記", "レビ記", "民数記", "申命記"]
book_files = {
    "創世記": "創世記.txt",
    "出エジプト記": "出エジプト記.txt",
    "レビ記": "レビ記.txt",
    "民数記": "民数記.txt",
    "申命記": "申命記.txt"
}

class BibleApp:
    def __init__(self, master):
        self.master = master
        master.title("聖書検索")
        large_font = font.Font(size=16)

        self.book_label = tk.Label(master, text="巻:", font=large_font)
        self.book_label.grid(row=0, column=0)
        self.book_combobox = ttk.Combobox(master, values=books, font=large_font)
        self.book_combobox.grid(row=0, column=1)
        self.book_combobox.config(width=20)

        self.verse_label = tk.Label(master, text="章節:", font=large_font)
        self.verse_label.grid(row=1, column=0)
        self.verse_entry = tk.Entry(master, font=large_font)
        self.verse_entry.grid(row=1, column=1)
        self.verse_entry.config(width=20)

        self.search_button = tk.Button(master, text="検索", command=self.search, font=large_font)
        self.search_button.grid(row=2, column=0, columnspan=2, sticky='ew')

        self.from_label = tk.Label(master, text="", font=large_font)
        self.from_label.grid(row=3, column=0)
        self.to_label = tk.Label(master, text="", font=large_font)
        self.to_label.grid(row=3, column=1)

        self.result_text = tk.Text(master, height=20, width=100, font=large_font)
        self.result_text.grid(row=4, column=0, columnspan=2)

    def search(self):
        book = self.book_combobox.get()
        verse = self.verse_entry.get()
        if book in book_files:
            with open(book_files[book], "r", encoding="utf-8") as file:
                lines = file.readlines()
            
            if '-' in verse:
                start_verse, end_verse = verse.split('-')
            else:
                start_verse = end_verse = verse

            try:
                start_chapter, start_verse = map(int, start_verse.split(':'))
                end_chapter, end_verse = map(int, end_verse.split(':'))
            except ValueError:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "無効な章節形式です。")
                return

            # ラベルの更新
            self.from_label.config(text=f"{start_chapter}:{start_verse} から")
            self.to_label.config(text=f"{end_chapter}:{end_verse}")

            result = ""
            collecting = False

            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0 and ':' in parts[0]:
                    try:
                        chapter_verse = parts[0]
                        chapter, verse_num = map(int, chapter_verse.split(':'))
                    except ValueError:
                        continue  # 無効な行をスキップ

                    if chapter == start_chapter and verse_num == start_verse:
                        collecting = True
                    
                    if collecting:
                        result += line.strip() + "\n"
                    
                    if chapter == end_chapter and verse_num == end_verse:
                        result += line.strip() + "\n"
                        collecting = False

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)

root = tk.Tk()
app = BibleApp(root)
root.mainloop()
