import json
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
items={i['item_id']:i for i in json.load(open('items.json'))}
cat={c['id']:c for c in json.load(open('catalog.json'))}
L=[json.loads(l) for l in open('results/claude.jsonl')]
F="Arial"; hdr=PatternFill("solid",fgColor="DCE6F1"); thin=Side(style="thin",color="BFBFBF"); B=Border(top=thin,bottom=thin,left=thin,right=thin)
hi=PatternFill("solid",fgColor="FFF2CC")
def sheet(ws,title,H,R,W,fill=None):
    ws.title=title
    for j,h in enumerate(H,1):
        c=ws.cell(1,j,h); c.font=Font(name=F,bold=True,size=10); c.fill=hdr; c.border=B; c.alignment=Alignment(wrap_text=True,vertical="center")
    for i,r in enumerate(R,2):
        for j,v in enumerate(r,1):
            c=ws.cell(i,j,v); c.font=Font(name=F,size=10); c.border=B; c.alignment=Alignment(wrap_text=True,vertical="top")
            if fill and fill(r): c.fill=hi
    for j,w in enumerate(W,1): ws.column_dimensions[get_column_letter(j)].width=w
    ws.freeze_panes="C2"; ws.auto_filter.ref=f"A1:{get_column_letter(len(H))}{len(R)+1}"
rows=[]; grp=defaultdict(list)
for x in L:
    it=items[x['item_id']]
    for d in x['distractors']:
        o=d['option']; pa=it['pct_all'][o]; pl=it['pct_low'][o]
        rows.append([x['item_id'],it['content_code'],o,pa,pl,d['student_work'],"是" if d['is_misconception'] else "否",d['reason'],d['mc_id'] or "",d['new_belief'],d['type'],d['confidence']])
        if d['is_misconception']: grp[d['mc_id'] or d['new_belief']].append((x['item_id'],o,pa,pl,d['type'],d['confidence']))
wb=Workbook()
sheet(wb.active,"逐選項分析",["題目","學習內容","選項","全體%","待加強%","推測的學生算法","是迷思","不是迷思的原因","目錄編號","新迷思（目錄沒有）","類型","信心"],rows,
      [8,9,5,7,8,46,6,12,10,30,6,6],fill=lambda r:r[6]=="是" and r[3]>=10)
sm=[]
for k,v in grp.items():
    inc=k in cat
    sm.append([k if inc else "（新）",cat[k]['belief'] if inc else k,v[0][4],len({a for a,*_ in v}),"、".join(f"{a} {o}" for a,o,*_ in v),max(x[2] for x in v),max(x[3] for x in v),"、".join(sorted({x[5] for x in v}))])
sm.sort(key=lambda r:(-r[3],-r[5]))
sheet(wb.create_sheet(),"迷思彙整",["目錄編號","學生想法","類型","出現題數","出現的題目與選項","最高全體%","最高待加強%","信心"],sm,[10,46,6,8,34,9,10,14],fill=lambda r:r[3]>=2)
wb.save("/mnt/user-data/outputs/P1.3_會考誘答分析_Claude_111-115.xlsx")
print(len(rows),len(sm),sum(1 for r in sm if r[0]!="（新）"),sum(1 for r in sm if r[0]=="（新）"),sum(1 for r in sm if r[3]>=2))
