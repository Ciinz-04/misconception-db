"""用程式驗算：把推測的錯誤規則寫成函式，代入會考原題，看算出來是否剛好等於該誘答選項。
只用 Python 標準庫：多項式用 {次數: 係數}，根式用 (有理數部分, 根號係數, 根號內)。"""
from fractions import Fraction as Fr
import math
R = []
def check(item, opt, mc, desc, got, option):
    ok = (abs(got - option) < 1e-9) if isinstance(got, float) or isinstance(option, float) else got == option
    R.append((item, opt, mc, desc, show(got), show(option), ok))
def show(v):
    if isinstance(v, dict): return " + ".join(f"{c}x^{d}" for d, c in sorted(v.items(), reverse=True) if c)
    if isinstance(v, tuple): return f"{v[0]} + {v[1]}√{v[2]}"
    return str(v)
def P(**kw): return {int(k[1:]): v for k, v in kw.items() if v}
def add(*ps):
    out = {}
    for p in ps:
        for d, c in p.items(): out[d] = out.get(d, 0) + c
    return {d: c for d, c in out.items() if c}
def neg(p): return {d: -c for d, c in p.items()}

# 114-02 (5x²−2x) − (4−3x)
A = P(d2=5, d1=-2); t1, t2 = P(d0=4), P(d1=-3)
check("114-02", "B", "正答", "每一項都變號", add(A, neg(t1), neg(t2)), P(d2=5, d1=1, d0=-4))
check("114-02", "C", "NG-04", "括號前是負號，去括號完全不變號", add(A, t1, t2), P(d2=5, d1=-5, d0=4))
check("114-02", "D", "EQ-07b", "只改第一項的符號", add(A, neg(t1), t2), P(d2=5, d1=-5, d0=-4))
check("114-02", "A", "EQ-06", "4 − 3x 當成 1x（不同類項合併），再相減", add(A, neg(P(d1=4 - 3))), P(d2=5, d1=-3))

# 111-05 9/22 + 11/18 − (23/22 − 7/18)
def op_wise(p, q, sign):   # 錯誤規則：分子和分子、分母和分母各自照運算符號計算
    return (p[0] + sign * q[0], p[1] + sign * q[1])
inner = op_wise((23, 22), (7, 18), -1)               # 23/22 − 7/18 → 16/4
left = op_wise((9, 22), (11, 18), +1)                # 9/22 + 11/18 → 20/40
n, d = op_wise(left, inner, -1)                       # 20/40 − 16/4 → 4/36
check("111-05", "C", "FR-08", "分子、分母各自照運算符號計算（括號內也一樣）", Fr(n, d), Fr(1, 9))
check("111-05", "C", "FR-08（另一種寫法）", "先拆括號，再把所有分子、分母分別加總", Fr(9 + 11 - 23 + 7, 22 + 18 + 22 + 18), Fr(1, 9))
# 113-01 3/7 − (−1/4)
check("113-01", "C", "FR-08", "分子加分子、分母加分母", Fr(3 + 1, 7 + 4), Fr(4, 11))
check("113-01", "B", "新：減去負數時負號可以忽略", "3/7 − 1/4", Fr(3, 7) - Fr(1, 4), Fr(5, 28))

# 112-01 (−3)³
check("112-01", "B", "PM-02", "次方當成乘以指數：(−3)×3", -3 * 3, -9)
check("112-01", "D", "新：負數的次方一定是正的", "|(−3)³|", abs((-3) ** 3), 27)

# 112-04 √135
def pull_out_without_root(n, f): return (0, f, n // f)       # 根號內的因數 f 直接提出，不開方
def simplify_root(n):
    a = max(k for k in range(1, int(math.isqrt(n)) + 1) if n % (k * k) == 0); return (0, a, n // (a * a))
check("112-04", "C", "正答", "135 = 9×15，9 開方得 3", simplify_root(135), (0, 3, 15))
check("112-04", "B", "新：根號內的因數直接提出不開方", "135 = 27×5，提出 27", pull_out_without_root(135, 27), (0, 27, 5))
check("112-04", "D", "新：根號內的因數直接提出不開方", "135 = 9×15，提出 9", pull_out_without_root(135, 9), (0, 9, 15))

# 114-01 7¹⁰ × 7² ÷ 7⁴
check("114-01", "B", "新：指數照運算符號計算", "10 × 2 ÷ 4", Fr(10 * 2, 4), 5)
check("114-01", "D", "新：相除時指數也相加", "10 + 2 + 4", 10 + 2 + 4, 16)

# 111-10 (x−2)² = 3，a > b，求 2a + b
def two_a_plus_b(h, r):   # 根為 h ± r（r 為 (根號係數, 根號內) 或整數）
    if isinstance(r, tuple): return (3 * h, r[0], r[1])          # 2(h+√) + (h−√) = 3h + √
    return 2 * (h + r) + (h - r)
check("111-10", "C", "正答", "x − 2 = ±√3 → x = 2 ± √3", two_a_plus_b(2, (1, 3)), (6, 1, 3))
check("111-10", "A", "QE-05", "開平方只加 ± 不加根號：x − 2 = ±3", two_a_plus_b(2, 3), 9)
check("111-10", "D", "EQ-08a", "移項不變號：x = −2 ± √3", two_a_plus_b(-2, (1, 3)), (-6, 1, 3))
check("111-10", "B", "QE-05＋EQ-08a", "兩個錯誤疊加：x = −2 ± 3", two_a_plus_b(-2, 3), -3)

# 111-16 緩降機：每層 3 公尺，八樓到一樓
floors_ok, floors_bug = 8 - 1, 8
check("111-16", "A", "正答", "7 層 × 3 + 1.6 − 0.4 − 0.5", Fr(floors_ok*3) + Fr(16, 10) - Fr(4, 10) - Fr(5, 10), Fr(217, 10))
check("111-16", "C", "FR-05a", "八樓到一樓算成 8 層", Fr(floors_bug*3) + Fr(16, 10) - Fr(4, 10) - Fr(5, 10), Fr(247, 10))
check("111-16", "B", "EQ-17", "漏掉 0.4 和 0.5", Fr(floors_ok*3) + Fr(16, 10), Fr(226, 10))

# 114-09 20 個停車位、下車區夾在中間
check("114-09", "A", "正答", "20×200 + 19×150", 20*200 + 19*150, 6850)
check("114-09", "B", "FR-05a", "下車區算成 20 個", 20*200 + 20*150, 7000)

# 115-17 2700 億度，每年增加前一年的 2.5%，2024～2030
yrs = 2030 - 2023
check("115-17", "A", "正答", "複利：2700 × 1.025^年數", 2700 * 1.025 ** yrs, 2700 * 1.025 ** 7)
check("115-17", "C", "新：百分比成長當成固定增量", "線性：2700 + 年數 × 2700 × 0.025", 2700 + yrs * 2700 * 0.025, 2700 + 7 * 2700 * 0.025)
check("115-17", "B", "FR-05a", "2024～2030 算成 8 年", 2700 * 1.025 ** (yrs + 1), 2700 * 1.025 ** 8)

# 112-21 吊橋：小維 84 步、阿良 60 步交會，阿良再走 70 步到西橋頭
check("112-21", "D", "正答", "比例：60 × 84 ÷ 70", Fr(60*84, 70), 72)
check("112-21", "A", "新：比例問題用差來算", "60 − (84 − 70)", 60 - (84 - 70), 46)
check("112-21", "B", "EQ-03", "比例寫反：60 × 70 ÷ 84", Fr(60*70, 84), 50)

# 112-12 盒玩：動物 6 款喜歡 2 款，汽車 5 款喜歡 1 款
check("112-12", "A", "正答", "2/6 × 1/5", Fr(2, 6) * Fr(1, 5), Fr(1, 15))
check("112-12", "D", "新：兩個獨立事件把個數合起來算", "(2+1)/(6+5)", Fr(2 + 1, 6 + 5), Fr(3, 11))

# 111-11 遊戲機：售價比預算多 1200，打 8 折後比預算少 200
def solve_linear(p, q, r, s):   # 解 p·b + q = r·b + s
    return Fr(s - q) / Fr(p - r)
k = Fr(4, 5)
check("111-11", "C", "正答", "0.8(b + 1200) = b − 200", solve_linear(k, k * 1200, 1, -200), 5800)
check("111-11", "A", "EQ-03", "「少 200」寫成「多 200」：0.8(b + 1200) = b + 200", solve_linear(k, k * 1200, 1, 200), 3800)
check("111-11", "B", "EQ-17", "漏掉「少 200」：0.8(b + 1200) = b", solve_linear(k, k * 1200, 1, 0), 4800)
check("111-11", "D", "EQ-03（乘錯對象）", "8 折乘在預算上：b + 1200 = 0.8(b − 200)，再去掉負號", abs(solve_linear(1, 1200, k, -k * 200)), 6800)

if __name__ == "__main__":
    for r in R: print(("✓" if r[6] else "✗"), r[0], r[1], r[2], "｜", r[3], "→", r[4], "＝ 選項", r[5])
    print(f"{sum(r[6] for r in R)}/{len(R)} 相符")
