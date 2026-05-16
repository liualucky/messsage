from pathlib import Path
import json, textwrap, os
base = Path('output/acupoint_app')
(base/'data').mkdir(parents=True, exist_ok=True)
(base/'assets').mkdir(parents=True, exist_ok=True)
(base/'templates').mkdir(parents=True, exist_ok=True)

json_data = {
  "內科": [
    {"病名": "頭痛", "主穴": ["頭維", "上星", "百會"], "配穴": ["風池", "天柱", "合谷", "足三里"]},
    {"病名": "偏頭痛", "主穴": ["風池", "頭維", "太陽"], "配穴": ["列缺", "陽陵泉", "丘墟"]},
    {"病名": "發熱", "主穴": ["風池", "大杼", "大椎"], "配穴": ["曲池", "後溪", "足三里"]},
    {"病名": "感冒", "主穴": ["風門", "大椎", "太陽"], "配穴": ["尺澤", "合谷", "外關", "足三里"]},
    {"病名": "咳嗽", "主穴": ["肺俞", "中府", "尺澤"], "配穴": ["列缺", "太淵", "足三里"]},
    {"病名": "高血壓", "主穴": ["百會", "風池", "曲池"], "配穴": ["太衝", "陽陵泉", "三陰交", "足三里"]},
    {"病名": "低血壓", "主穴": ["百會", "關元", "氣海"], "配穴": ["足三里", "脾俞", "腎俞"]},
    {"病名": "心悸", "主穴": ["內關", "膻中", "心俞"], "配穴": ["足三里"]},
    {"病名": "失眠", "主穴": ["神門", "內關", "百會"], "配穴": ["三陰交", "安眠"]},
    {"病名": "口腔炎", "主穴": ["頰車", "地倉", "下關"], "配穴": ["曲池", "合谷", "中脘", "足三里"]},
    {"病名": "便秘", "主穴": ["天樞", "神門", "支溝"], "配穴": ["大腸俞", "足三里"]},
    {"病名": "腹瀉", "主穴": ["天樞", "中脘", "關元"], "配穴": ["足三里", "脾俞", "大腸俞"]},
    {"病名": "胃痛", "主穴": ["中脘", "內關", "足三里"], "配穴": ["梁丘", "公孫"]},
    {"病名": "腹痛", "主穴": ["中脘", "天樞", "關元"], "配穴": ["足三里", "公孫"]},
    {"病名": "嘔吐", "主穴": ["身柱", "上脘", "內關"], "配穴": ["足三里"]},
  ],
  "外科": [
    {"病名": "肩痛", "主穴": ["肩髃", "肩貞", "曲池"], "配穴": ["外關", "合谷"]},
    {"病名": "腰痛", "主穴": ["腎俞", "大腸俞", "命門"], "配穴": ["委中", "崑崙"]},
    {"病名": "膝痛", "主穴": ["犢鼻", "內外膝眼", "足三里"], "配穴": ["陽陵泉", "陰陵泉"]},
  ],
  "兒科": [
    {"病名": "小兒疳積", "主穴": ["脾俞", "胃俞", "足三里"], "配穴": []},
    {"病名": "小兒遺尿", "主穴": ["關元", "中極", "腎俞"], "配穴": ["三陰交"]},
    {"病名": "小兒夜啼", "主穴": ["身柱", "百會", "中脘"], "配穴": []},
  ],
  "婦科": [
    {"病名": "月經痛", "主穴": ["關元", "中極", "三陰交"], "配穴": ["氣海", "足三里"]},
  ]
}
(base/'data'/'diseases.json').write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding='utf-8')

main_py = '''# -*- coding: utf-8 -*-
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "diseases.json")
ICON_FILE = os.path.join(BASE_DIR, "assets", "app.ico")

ALIASES = {
    "偏頭疼": "偏頭痛",
    "高血壓病": "高血壓",
    "血壓高": "高血壓",
    "發燒": "發熱",
    "感冒發燒": "感冒",
    "支氣管炎": "咳嗽",
    "牙痛": "口腔炎",
    "大便秘結": "便秘",
    "胃疼": "胃痛",
    "肚子痛": "腹痛",
    "肩周炎": "肩痛",
    "膝蓋痛": "膝痛",
    "體虛": "低血壓",
    "遺尿": "小兒遺尿",
    "夜啼": "小兒夜啼",
}

CATEGORY_ORDER = ["全部", "內科", "外科", "婦科", "兒科"]


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def flatten_data(data):
    items = []
    for category, diseases in data.items():
        for d in diseases:
            items.append({
                "分類": category,
                "病名": d["病名"],
                "主穴": d.get("主穴", []),
                "配穴": d.get("配穴", [])
            })
    return items


def normalize(text):
    text = (text or "").strip()
    return ALIASES.get(text, text)


def filter_items(items, category="", keyword=""):
    keyword = normalize(keyword)
    result = []
    for item in items:
        if category and category != "全部" and item["分類"] != category:
            continue
        name = item["病名"]
        if keyword and keyword not in name and keyword not in normalize(name):
            continue
        result.append(item)
    return result


def format_points(title, points):
    return f"{title}：{"、".join(points) if points else "無"}"


def update_list(event=None):
    category = category_var.get()
    keyword = search_var.get().strip()
    values = filter_items(all_items, category=category, keyword=keyword)
    listbox.delete(0, tk.END)
    for item in values:
        listbox.insert(tk.END, f'[{item["分類"]}] {item["病名"]}')
    current_results[:] = values
    if values:
        listbox.selection_set(0)
        show_detail(0)
    else:
        detail_var.set("未找到符合的病名。")


def show_detail(index=None):
    if index is None:
        sel = listbox.curselection()
        if not sel:
            return
        index = sel[0]
    if index < 0 or index >= len(current_results):
        return
    item = current_results[index]
    detail = [
        f"分類：{item['分類']}",
        f"病名：{item['病名']}",
        format_points("主穴", item['主穴']),
        format_points("配穴", item['配穴'])
    ]
    detail_var.set("\n".join(detail))


def on_list_select(event=None):
    show_detail()


def copy_detail():
    text = detail_var.get()
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("已複製", "已複製目前內容。")


def clear_search():
    search_var.set("")
    category_var.set("全部")
    update_list()


data = load_data()
all_items = flatten_data(data)
current_results = []

root = tk.Tk()
root.title("病名搜尋與主穴配穴查詢")
root.geometry("1020x620")
root.resizable(False, False)
try:
    root.iconbitmap(ICON_FILE)
except Exception:
    pass

style = ttk.Style()
style.theme_use("clam")
BG = "#F8F5F0"
ACCENT = "#B23A3A"
TEXT = "#2C2C2C"
PANEL = "#FFFFFF"
SELECT = "#F3D7B6"
root.configure(bg=BG)
style.configure("TFrame", background=BG)
style.configure("TLabel", background=BG, foreground=TEXT, font=("Microsoft JhengHei", 11))
style.configure("Title.TLabel", background=BG, foreground=ACCENT, font=("Microsoft JhengHei", 18, "bold"))
style.configure("Sub.TLabel", background=BG, foreground=TEXT, font=("Microsoft JhengHei", 12, "bold"))
style.configure("TButton", font=("Microsoft JhengHei", 11))
style.configure("Accent.TButton", background=ACCENT, foreground="white")
style.map("Accent.TButton", background=[("active", "#932E2E")])
style.configure("TCombobox", font=("Microsoft JhengHei", 11))

main = ttk.Frame(root, padding=16)
main.pack(fill="both", expand=True)

title = ttk.Label(main, text="病名搜尋 + 分類篩選 + 主穴 / 配穴顯示", style="Title.TLabel")
title.grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 14))

ttk.Label(main, text="病名搜尋：", font=("Microsoft JhengHei", 12)).grid(row=1, column=0, sticky="w")
search_var = tk.StringVar()
search_entry = ttk.Entry(main, textvariable=search_var, width=26, font=("Microsoft JhengHei", 12))
search_entry.grid(row=1, column=1, sticky="w", padx=(0, 12))
search_entry.bind("<KeyRelease>", update_list)

ttk.Label(main, text="病名分類：", font=("Microsoft JhengHei", 12)).grid(row=1, column=2, sticky="w")
category_var = tk.StringVar(value="全部")
category_combo = ttk.Combobox(main, textvariable=category_var, values=CATEGORY_ORDER, width=16, state="readonly")
category_combo.grid(row=1, column=3, sticky="w")
category_combo.bind("<<ComboboxSelected>>", update_list)

ttk.Button(main, text="清除", command=clear_search).grid(row=1, column=4, padx=8)

left = ttk.Frame(main)
left.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(18, 0))
right = ttk.Frame(main)
right.grid(row=2, column=2, columnspan=3, sticky="nsew", pady=(18, 0), padx=(20, 0))

main.grid_rowconfigure(2, weight=1)
main.grid_columnconfigure(1, weight=1)
main.grid_columnconfigure(3, weight=1)

# Left panel
left_title = ttk.Label(left, text="病名清單", style="Sub.TLabel")
left_title.pack(anchor="w")
list_frame = ttk.Frame(left)
list_frame.pack(fill="both", expand=True, pady=(8, 0))
scrollbar = ttk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")
listbox = tk.Listbox(list_frame, font=("Microsoft JhengHei", 12), height=22, yscrollcommand=scrollbar.set, bg=PANEL, selectbackground=SELECT)
listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox.yview)
listbox.bind("<<ListboxSelect>>", on_list_select)

# Right panel
right_title = ttk.Label(right, text="查詢結果", style="Sub.TLabel")
right_title.pack(anchor="w")
detail_var = tk.StringVar(value="請先選擇病名。")
detail_label = ttk.Label(right, textvariable=detail_var, font=("Microsoft JhengHei", 12), justify="left", wraplength=500)
detail_label.pack(anchor="nw", pady=(10, 12), fill="x")

btn_frame = ttk.Frame(right)
btn_frame.pack(anchor="w", pady=(8, 0))
ttk.Button(btn_frame, text="複製結果", style="Accent.TButton", command=copy_detail).pack(side="left", padx=(0, 8))
ttk.Button(btn_frame, text="顯示主穴配穴", command=update_list).pack(side="left")

tip = ttk.Label(main, text="操作方式：輸入病名關鍵字後即時篩選，或先選擇分類，再點選病名查看主穴與配穴。", font=("Microsoft JhengHei", 10))
tip.grid(row=3, column=0, columnspan=5, sticky="w", pady=(16, 0))

update_list()
root.mainloop()
'''
(base/'main.py').write_text(main_py, encoding='utf-8')

(base/'requirements.txt').write_text('pyinstaller\n', encoding='utf-8')
(base/'README.md').write_text(textwrap.dedent('''
# 病名搜尋與主穴配穴查詢

## 功能
- 病名搜尋
- 病名分類篩選
- 顯示主穴與配穴
- 可打包成 Windows exe

## 執行
```bash
python main.py
```

## 打包
```bash
pyinstaller --noconfirm --onefile --windowed main.py
```
''').strip() + '\n', encoding='utf-8')
(base/'build.bat').write_text('@echo off\npython -m pip install -r requirements.txt\npyinstaller --noconfirm --onefile --windowed main.py\npause\n', encoding='utf-8')

# create a simple placeholder ico note
(base/'assets'/'ICON_README.txt').write_text('請將自製 app.ico 放入此資料夾。可用 256x256 PNG 轉 ICO。', encoding='utf-8')

# zip it
import shutil
zip_path = shutil.make_archive('output/acupoint_app_complete', 'zip', root_dir='output', base_dir='acupoint_app')
print(zip_path)