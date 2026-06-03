import re
import matplotlib.pyplot as plt
from collections import defaultdict

# ここにアップロードされたテキスト全体を貼り付けてください（変数 raw_text）
raw_text = """# Paste the full text extracted from the uploaded file here"""

# 正規化
raw_text = raw_text.replace('〜','~').replace('（','(').replace('）',')').replace('　',' ').replace('１','1').replace('３','3').replace('６','6').replace('９','9')

lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()!='']
current = None
records = []  # list of (type, answer_line)

for ln in lines:
    if ln in ['本人','知人','経験なし','NR']:
        current = ln
        continue
    if current is None:
        continue
    # 回答行はセミコロン区切りを含む行を対象
    if ';' in ln or 'Instagram' in ln or 'YouTube' in ln or 'X' in ln or '旧Twitter' in ln or '𝕏' in ln:
        records.append((current, ln))

# X使用時間カテゴリ判定関数
def classify_x(ans_line):
    s = ans_line.replace(' ', '')
    # 旧Twitter / 𝕏 / X の表記ゆれを検出
    # 例: 𝕏(旧Twitter)(使用しない) や 𝕏(旧Twitter) (1時間未満) など
    # 括弧内の時間表現を探す
    m = re.search(r'(?:𝕏|X|旧Twitter|旧Twitter).*?\\(([^)]+)\\)', s)
    if not m:
        # 𝕏の記載が無ければ「使用していない」とみなす
        return '使用していない'
    t = m.group(1)
    if '使用しない' in t or '使用していない' in t:
        return '使用していない'
    if '未満' in t:
        return '1時間未満'
    # それ以外（1〜3時間等）は1時間以上に分類
    return '1時間以上'

# 集計
cats = ['使用していない','1時間未満','1時間以上']
groups = ['本人','知人','全体']
counts = {g: {c:0 for c in cats} for g in groups}

total_parsed = 0
for typ, ans in records:
    cat = classify_x(ans)
    if typ in ['本人','知人']:
        counts[typ][cat] += 1
    counts['全体'][cat] += 1
    total_parsed += 1

# 割合計算（%）
perc = {}
for g in groups:
    s = sum(counts[g].values())
    if s == 0:
        perc[g] = {c:0 for c in cats}
    else:
        perc[g] = {c: counts[g][c] / s * 100 for c in cats}

# プロット（隣接棒）
import numpy as np
labels = groups
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(9,6))
for i,c in enumerate(cats):
    ax.bar(x + i*width, [perc[g][c] for g in labels], width, label=c)
ax.set_xticks(x + width)
ax.set_xticklabels(labels)
ax.set_ylabel('割合 (%)')
ax.set_title('X使用時間の割合（本人・知人・全体）')
ax.legend()
plt.tight_layout()
plt.show()

# 集計結果の表示
print('解析に使用した回答数（判定可能な行）:', total_parsed)
print('件数（カテゴリ別）:', counts)
print('割合（%）:', perc)
